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