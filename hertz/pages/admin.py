from django.contrib import admin
from .models import Subscriber

admin.site.register(Subscriber)

from django.contrib import admin
from .models import Product, Category

admin.site.register(Product)
admin.site.register(Category)