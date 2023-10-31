from rest_framework import serializers

from pizzaria.functions import attempt_json_deserialize
from pizzaria.models import (Box, GreetingCard, GreetingCardInstance, Order,
                             Pizza, PizzaMenuItem, Topping)


class BoxSerializer(serializers.ModelSerializer):
    class Meta:
        model = Box
        fields = ['id', 'color']


class OrderSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'customer', 'address']


class ToppingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topping
        fields = ['name']

class PizzaSerializer(serializers.ModelSerializer):
    order = OrderSummarySerializer(read_only=True)
    toppings = ToppingSerializer(read_only=True, many=True)
    box = BoxSerializer(source='menu_item.box', read_only=True)

    class Meta:
        model = Pizza
        fields = ['id', 'order', 'box', 'menu_item', 'toppings', 'size']

    def create(self, validated_data):
        request = self.context['request']

        menu_item_pk = request.data.get('menu_item')
        menu_item_pk = attempt_json_deserialize(menu_item_pk)
        if menu_item_pk is not None:
            validated_data['menu_item_id'] = menu_item_pk

        order_pk = request.data.get('order')
        order_pk = attempt_json_deserialize(order_pk, expect_type=str)
        validated_data['order_id'] = order_pk

        extra_toppings_data = request.data.get('extra_toppings')
        extra_toppings_data = attempt_json_deserialize(extra_toppings_data, expect_type=list)
        validated_data['extra_toppings'] = extra_toppings_data

        remove_toppings_data = request.data.get('remove_toppings')
        remove_toppings_data = attempt_json_deserialize(remove_toppings_data, expect_type=list)
        validated_data['remove_toppings'] = remove_toppings_data

        instance = super().create(validated_data)

        return instance

    def update(self, instance, validated_data):
        request = self.context['request']

        menu_item_pk = request.data.get('menu_item')
        menu_item_pk = attempt_json_deserialize(menu_item_pk)
        if menu_item_pk is not None:
            validated_data['menu_item_id'] = menu_item_pk

        order_pk = request.data.get('order')
        order_pk = attempt_json_deserialize(order_pk, expect_type=str)
        validated_data['order_id'] = order_pk

        extra_toppings_data = request.data.get('extra_toppings')
        extra_toppings_data = attempt_json_deserialize(extra_toppings_data, expect_type=list)
        validated_data['extra_toppings'] = extra_toppings_data

        remove_toppings_data = request.data.get('remove_toppings')
        remove_toppings_data = attempt_json_deserialize(remove_toppings_data, expect_type=list)
        validated_data['remove_toppings'] = remove_toppings_data

        instance = super().update(instance, validated_data)

        return instance

class PizzaSummarySerializer(serializers.ModelSerializer):
    box = BoxSerializer(read_only=True)

    class Meta:
        model = Pizza
        fields = ['id', 'box', 'toppings']


class OrderDetailSerializer(serializers.ModelSerializer):
    pizzas = PizzaSummarySerializer(read_only=True, many=True)

    class Meta:
        model = Order
        fields = ['id', 'customer', 'address', 'pizzas']

class PizzaMenuItemSerializer(serializers.ModelSerializer):
    box = BoxSerializer(read_only=True)
    toppings = ToppingSerializer(read_only=True, many=True)

    class Meta:
        model = PizzaMenuItem
        fields = ['name', 'box', 'toppings']

    def create(self, validated_data):
        request = self.context['request']

        box_data = request.data.get('box')
        box_data = attempt_json_deserialize(box_data, expect_type=dict)
        box = Box.objects.create(**box_data)
        validated_data['box'] = box

        toppings_data = request.data.get('toppings')
        toppings_data = attempt_json_deserialize(toppings_data, expect_type=list)
        toppings_objs = [Topping.objects.create(**data) for data in toppings_data]
        validated_data['toppings'] = toppings_objs

        instance = super().create(validated_data)

        return instance

    def update(self, instance, validated_data):
        request = self.context['request']

        box_data = request.data.get('box')
        box_data = attempt_json_deserialize(box_data, expect_type=dict)
        box = Box.objects.create(**box_data)
        validated_data['box'] = box

        toppings_data = request.data.get('toppings')
        toppings_ids = attempt_json_deserialize(toppings_data, expect_type=list)
        validated_data['toppings'] = toppings_ids

        instance = super().update(instance, validated_data)

        return instance

class GreetingCardSerializer(serializers.ModelSerializer):
	class Meta:
		model = GreetingCard
		fields = ['message']

class GreetingCardInstanceSerializer(serializers.ModelSerializer):
	message = serializers.CharField(max_length=256)

	class Meta:
		model = GreetingCardInstance
		fields = ['message']