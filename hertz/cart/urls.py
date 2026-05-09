from django.urls import path
from .views import add_to_cart_view

urlpatterns = [
    path('add/<int:product_id>/', add_to_cart_view, name='add_to_cart'),
]