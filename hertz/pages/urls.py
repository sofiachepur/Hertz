from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('rizdvo/', views.rizdvo, name='rizdvo'),
    path('obzhynky/', views.obzhynky, name='obzhynky'),
    path('kupala/', views.kupala, name='kupala'),
    path('velykden/', views.velykden, name='velykden'),
    path('pobut/', views.pobut, name='pobut'),
    path('subscribe/', views.emailSub, name='subscribe'),
    path('products/', views.products, name='products'),
        path(
            'cart/add/<int:product_id>/',
            views.add_to_cart,
            name='add_to_cart'
        ),
        path('cart/', views.cart, name='cart'),
    path('cart/increase/<int:product_id>/', views.increase_quantity, name='increase_quantity'),
    path('cart/decrease/<int:product_id>/', views.decrease_quantity, name='decrease_quantity'),
    path('cart/remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),

path('checkout/', views.checkout, name='checkout'),
path('products/', views.products, name='products'),
path('liqpay/callback/', views.liqpay_callback, name='liqpay_callback'),
]

