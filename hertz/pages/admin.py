from django.contrib import admin
from .models import Order, OrderItem, Product, Category, Subscriber


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_filter   = ['payment_status', 'delivery_method']
    search_fields = ['name', 'phone', 'email']
    list_display = ['id', 'name', 'phone', 'delivery_method', 'delivery_city', 'payment_method', 'payment_status',
                    'order_status', 'created_at']
    list_editable = ['payment_status', 'order_status']
    inlines       = [OrderItemInline]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'quantity', 'category']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ['email', 'created_at']