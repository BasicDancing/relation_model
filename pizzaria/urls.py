from django.urls import include, path
from rest_framework import routers

from pizzaria.views import (OrderViewSet, PizzaMenuItemViewSet, PizzaViewSet,
                            ToppingViewSet)

router = routers.DefaultRouter()
router.register("orders", OrderViewSet, "orders")
router.register("pizzas", PizzaViewSet, "pizzas")
router.register("toppings", ToppingViewSet, "toppings")
router.register("menu", PizzaMenuItemViewSet, "menu")

urlpatterns = [
    path("pizzaria/", include(router.urls))
]