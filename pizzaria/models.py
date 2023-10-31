import uuid

from django.db import models


class Order(models.Model):
    # In this example, I'll use UUIDs for primary keys
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    customer = models.CharField(max_length=256, blank=False, null=False)

    address = models.CharField(max_length=512, blank=True, null=False)


class Box(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    color = models.CharField(
        max_length=32, default="white", blank=False, null=False
    )


class Topping(models.Model):
    name = models.CharField(
        primary_key=True,
        max_length=64
    )


class Pizza(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    menu_id = models.ForeignKey(
        "pizzaria.Pizza",
        on_delete=models.SET_NULL,
        related_name="+",
        null=True
    )

    order = models.ForeignKey(
        "pizzaria.Order",
        on_delete=models.CASCADE,
        related_name="pizzas",
        null=False
    )

    SIZE_CHOICES = (
        ('S', 'Small'),
        ('M', 'medium'),
        ('L', 'Large'),
        ('xl', 'X-Large')
    )

    size = models.CharField(
        max_length=32,
        choices=SIZE_CHOICES,
        blank=False,
        null=False
    )

    extra_toppings = models.ManyToManyField(
        "pizzaria.Topping",
        related_name="+"
    )

    remove_toppings = models.ManyToManyField(
        "pizzaria.Topping",
        related_name="+"
    )

    @property
    def toppings(self):
        toppings = []

        if self.menu_id is not None:
            toppings += self.menu_id.toppings
        toppings += self.extra_toppings

        for topping in self.remove_toppings:
            try:
                toppings.remove(topping)
            except ValueError:
                pass  # don't worry about removing absent toppings

class GreetingCard(models.Model):
    message = models.CharField(max_length=256, blank=True, null=False)

class GreetingCardInstance(models.Model):
	# a ForeignKey to the GreetingCard this expands on
	card = models.ForeignKey(
		'pizzaria.GreetingCard',
		on_delete=models.CASCADE,
		related_name='instances',
		null=False
	)

	# a ForeignKey to another GreetingCardInstance
	on_instance = models.ForeignKey(
		'pizzaria.GreetingCardInstance',
		on_delete=models.CASCADE,
		related_name='modified_by',
		null=True
	)

	# a private field to store local data
	_message = models.CharField(max_length=256, blank=True, null=True)

	@property
	def message(self):
		# return the locally defined value, if there is one
		if self.message is not None:
			return self.message

		# otherwise, if this edits another instance...
		elif self.on_instance is not None:
			# delegate to that message property
			return self.on_instance.message

		# if all else fails, get the message from the card
		return self.card.message

	@message.setter
	def _(self, value):
		# store the value locally
		self._message = value

	@message.deleter
	def _(self):
		# delete the value locally only
		del self._message

class PizzaMenuItem(models.Model):
    name = models.CharField(
        primary_key=True,
        max_length=128
    )

    box = models.OneToOneField(
        "pizzaria.Box",
        on_delete=models.SET_NULL,
        related_name="contents",
        null=True
    )

    toppings = models.ManyToManyField(
        "pizzaria.Topping",
        related_name='+'
    )
