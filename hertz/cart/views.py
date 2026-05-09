from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from .utils import add_to_cart


def add_to_cart_view(request, product_id):
    add_to_cart(request.session, product_id)

    return JsonResponse({
        'success': True,
        'message': 'Товар додано в кошик'
    })

from django.shortcuts import render

def checkout(request):
    cart = request.session.get('cart', {})
    return render(request, 'cart/checkout.html', {'cart': cart})