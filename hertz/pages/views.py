from django.shortcuts import render

def home(request):
    return render(request, 'pages/home.html', {'title': 'Головна'})

def rizdvo(request):
    return render(request, 'pages/rizdvo.html', {'title': 'Різдво'})

def obzhynky(request):
    return render(request, 'pages/obzhynky.html', {'title': 'Обжинки'})

def kupala(request):
    return render(request, 'pages/kupala.html', {'title': 'Івана Купала'})

def velykden(request):
    return render(request, 'pages/velykden.html', {'title': 'Великдень'})

def pobut(request):
    return render(request, 'pages/pobut.html', {'title': 'Речі побуту'})

def checkout(request):
    return render(request, 'pages/checkout.html')