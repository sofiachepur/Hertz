from django.shortcuts import render, redirect
from .models import Product, Subscriber


def home(request):
    return render(request, 'pages/home.html')


def rizdvo(request):
    products = Product.objects.filter(category__name="Різдво")
    return render(request, 'pages/rizdvo.html', {'products': products})


def kupala(request):
    products = Product.objects.filter(category__name="Купала")
    return render(request, 'pages/kupala.html', {'products': products})


def obzhynky(request):
    products = Product.objects.filter(category__name="Обжинки")
    return render(request, 'pages/obzhynky.html', {'products': products})


def velykden(request):
    products = Product.objects.filter(category__name="Великдень")
    return render(request, 'pages/velykden.html', {'products': products})


def pobut(request):
    products = Product.objects.filter(category__name="Побут")
    return render(request, 'pages/pobut.html', {'products': products})


def products(request):
    products = Product.objects.all()
    return render(request, 'pages/products.html', {'products': products})


def emailSub(request):
    if request.method == "POST":
        email = request.POST.get("email")

        if email:
            Subscriber.objects.get_or_create(email=email)

    return redirect('home')

from django.shortcuts import redirect, get_object_or_404
from .models import Product


def add_to_cart(request, product_id):
    cart = request.session.get('cart', {})

    product = get_object_or_404(Product, id=product_id)

    product_id = str(product_id)

    current_quantity = cart.get(product_id, 0)

    # перевірка залишку товару
    if current_quantity < product.quantity:
        cart[product_id] = current_quantity + 1

    request.session['cart'] = cart
    request.session.modified = True

    return redirect('cart')


def cart(request):
    cart = request.session.get('cart', {})

    products = []
    total = 0

    for product_id, qty in cart.items():

        product = Product.objects.get(id=product_id)

        product.cart_quantity = qty
        product.total_price = product.price * qty

        total += product.total_price

        products.append(product)

    return render(request, 'pages/cart.html', {
        'products': products,
        'total': total
    })

from django.shortcuts import redirect, get_object_or_404
from .models import Product


def increase_quantity(request, product_id):
    cart = request.session.get('cart', {})

    product_id = str(product_id)
    product = get_object_or_404(Product, id=product_id)

    current = cart.get(product_id, 0)

    if current < product.quantity:
        cart[product_id] = current + 1

    request.session['cart'] = cart
    request.session.modified = True

    return redirect('cart')


def decrease_quantity(request, product_id):
    cart = request.session.get('cart', {})

    product_id = str(product_id)

    if product_id in cart:
        cart[product_id] -= 1

        if cart[product_id] <= 0:
            del cart[product_id]

    request.session['cart'] = cart
    request.session.modified = True

    return redirect('cart')


def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})

    product_id = str(product_id)

    if product_id in cart:
        del cart[product_id]

    request.session['cart'] = cart
    request.session.modified = True

    return redirect('cart')

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    return render(request, 'pages/product_detail.html', {
        'product': product
    })


from django.shortcuts import render, redirect
from .models import Order, OrderItem, Product

from .models import Order, OrderItem, Product

from django.shortcuts import render, redirect
from .models import Product, Order, OrderItem


def checkout(request):
    cart = request.session.get('cart', {})

    products = []
    total = 0

    for product_id, qty in cart.items():
        product = Product.objects.get(id=product_id)
        product.cart_quantity = qty
        product.total_price = product.price * qty

        total += product.total_price
        products.append(product)

    if request.method == "POST":

        order = Order.objects.create(
            name=request.POST.get('customer_name') or '',
            phone=request.POST.get('customer_phone') or '',
            address=request.POST.get('customer_address') or '',
            receiver_name=request.POST.get('receiver_name'),
            receiver_phone=request.POST.get('receiver_phone'),
            email=request.POST.get('customer_email'),
            comment=request.POST.get('comment'),
            delivery_method=request.POST.get('delivery'),
            payment_method=request.POST.get('payment'),
            total_price=total
        )

        for product in products:
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=product.cart_quantity,
                price=product.price
            )

            product.quantity -= product.cart_quantity
            product.save()

        request.session['cart'] = {}

        return redirect('/checkout?success=1')

    return render(request, 'pages/checkout.html', {
        'products': products,
        'total': total
    })


from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.conf import settings
from .models import Product, Order, OrderItem, Subscriber
import base64, hashlib, json


LIQPAY_PUBLIC_KEY  = 'sandbox_i46947698415'
LIQPAY_PRIVATE_KEY = 'sandbox_0HHrHOFXUafmKOJAseJTchYqHqfbQzL4uCCJpn87'


def _liqpay_signature(data_b64):
    raw = LIQPAY_PRIVATE_KEY + data_b64 + LIQPAY_PRIVATE_KEY
    return base64.b64encode(hashlib.sha1(raw.encode()).digest()).decode()


def _liqpay_form(order_id, amount, description, server_url, result_url):
    params = {
        "version":     "3",
        "public_key":  LIQPAY_PUBLIC_KEY,
        "action":      "pay",
        "amount":      str(amount),
        "currency":    "UAH",
        "description": description,
        "order_id":    str(order_id),
        "server_url":  server_url,
        "result_url":  result_url,
        "sandbox":     "1",
    }
    data_b64  = base64.b64encode(json.dumps(params).encode()).decode()
    signature = _liqpay_signature(data_b64)
    return {"data": data_b64, "signature": signature}


def home(request):
    return render(request, 'pages/home.html')

def rizdvo(request):
    products = Product.objects.filter(category__name="Різдво")
    return render(request, 'pages/rizdvo.html', {'products': products})

def kupala(request):
    products = Product.objects.filter(category__name="Купала")
    return render(request, 'pages/kupala.html', {'products': products})

def obzhynky(request):
    products = Product.objects.filter(category__name="Обжинки")
    return render(request, 'pages/obzhynky.html', {'products': products})

def velykden(request):
    products = Product.objects.filter(category__name="Великдень")
    return render(request, 'pages/velykden.html', {'products': products})

def pobut(request):
    products = Product.objects.filter(category__name="Побут")
    return render(request, 'pages/pobut.html', {'products': products})

def products_view(request):
    products = Product.objects.all()
    return render(request, 'pages/products.html', {'products': products})

def emailSub(request):
    if request.method == "POST":
        email = request.POST.get("email")
        if email:
            Subscriber.objects.get_or_create(email=email)
    return redirect('home')

def add_to_cart(request, product_id):
    cart       = request.session.get('cart', {})
    product    = get_object_or_404(Product, id=product_id)
    product_id = str(product_id)
    current    = cart.get(product_id, 0)
    if current < product.quantity:
        cart[product_id] = current + 1
    request.session['cart'] = cart
    request.session.modified = True
    return redirect('cart')

def cart(request):
    cart_data = request.session.get('cart', {})
    products  = []
    total     = 0
    for product_id, qty in cart_data.items():
        product               = Product.objects.get(id=product_id)
        product.cart_quantity = qty
        product.total_price   = product.price * qty
        total                += product.total_price
        products.append(product)
    return render(request, 'pages/cart.html', {'products': products, 'total': total})

def increase_quantity(request, product_id):
    cart       = request.session.get('cart', {})
    product_id = str(product_id)
    product    = get_object_or_404(Product, id=product_id)
    current    = cart.get(product_id, 0)
    if current < product.quantity:
        cart[product_id] = current + 1
    request.session['cart'] = cart
    request.session.modified = True
    return redirect('cart')

def decrease_quantity(request, product_id):
    cart       = request.session.get('cart', {})
    product_id = str(product_id)
    if product_id in cart:
        cart[product_id] -= 1
        if cart[product_id] <= 0:
            del cart[product_id]
    request.session['cart'] = cart
    request.session.modified = True
    return redirect('cart')

def remove_from_cart(request, product_id):
    cart       = request.session.get('cart', {})
    product_id = str(product_id)
    if product_id in cart:
        del cart[product_id]
    request.session['cart'] = cart
    request.session.modified = True
    return redirect('cart')

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'pages/product_detail.html', {'product': product})


def checkout(request):
    cart = request.session.get('cart', {})
    products = []
    total    = 0

    for product_id, qty in cart.items():
        product               = Product.objects.get(id=product_id)
        product.cart_quantity = qty
        product.total_price   = product.price * qty
        total                += product.total_price
        products.append(product)

    if request.method == "POST":
        order = Order.objects.create(
            name            = request.POST.get('customer_name')    or '',
            phone           = request.POST.get('customer_phone')   or '',
            address         = request.POST.get('customer_address') or '',
            receiver_name   = request.POST.get('receiver_name'),
            receiver_phone  = request.POST.get('receiver_phone'),
            email           = request.POST.get('customer_email'),
            comment         = request.POST.get('comment'),
            delivery_method = request.POST.get('delivery'),
            payment_method  = request.POST.get('payment'),
            total_price     = total,
            payment_status  = 'pending',
            delivery_city=request.POST.get('delivery_city') or '',
            delivery_branch=request.POST.get('delivery_branch') or '',
        )

        for product in products:
            OrderItem.objects.create(
                order    = order,
                product  = product,
                quantity = product.cart_quantity,
                price    = product.price,
            )
            product.quantity -= product.cart_quantity
            product.save()

        request.session['cart'] = {}

        if request.POST.get('payment') == 'Оплата картою':
            liqpay_data = _liqpay_form(
                order_id    = order.id,
                amount      = total,
                description = f'Замовлення #{order.id}',
                server_url  = request.build_absolute_uri('/liqpay/callback/'),
                result_url  = request.build_absolute_uri('/checkout?success=1'),
            )
            return render(request, 'pages/liqpay_redirect.html', {'liqpay_data': liqpay_data})

        return redirect('/checkout?success=1')

    return render(request, 'pages/checkout.html', {'products': products, 'total': total})


@csrf_exempt
def liqpay_callback(request):
    if request.method != 'POST':
        return HttpResponse(status=405)

    data      = request.POST.get('data', '')
    signature = request.POST.get('signature', '')

    if _liqpay_signature(data) != signature:
        return HttpResponse('bad signature', status=400)

    decoded  = json.loads(base64.b64decode(data).decode())
    status   = decoded.get('status')
    order_id = decoded.get('order_id')

    try:
        order = Order.objects.get(id=order_id)
        if status in ('success', 'sandbox'):
            order.payment_status = 'paid'
        elif status == 'failure':
            order.payment_status = 'failed'
        order.save()
    except Order.DoesNotExist:
        pass

    return HttpResponse('OK')