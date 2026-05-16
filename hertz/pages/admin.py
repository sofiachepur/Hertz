from django.contrib import admin
from .models import (
    Order,
    OrderItem,
    Product,
    Category,
    Subscriber,
    ProductType
)


# ── ADMIN TITLE ──

admin.site.site_header = "Hertz Admin"
admin.site.site_title = "Hertz"
admin.site.index_title = "Панель керування"


# ── ORDER ITEMS INLINE ──

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


# ── ORDERS ──

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    list_filter = [
        'payment_status',
        'delivery_method'
    ]

    search_fields = [
        'name',
        'phone',
        'email'
    ]

    list_display = [
        'id',
        'name',
        'phone',
        'delivery_method',
        'delivery_city',
        'payment_method',
        'payment_status',
        'order_status',
        'created_at'
    ]

    list_editable = [
        'payment_status',
        'order_status'
    ]

    inlines = [OrderItemInline]


# ── PRODUCTS ──

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = [
        'id',
        'title',
        'price',
        'quantity',
        'category',
        'product_type',
    ]

    list_filter = [
        'category',
        'product_type',
    ]

    search_fields = [
        'title',
        'description',
    ]

    list_editable = [
        'price',
        'quantity',
    ]

    ordering = ['title']


# ── CATEGORY ──

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    list_display = ['name']

    search_fields = ['name']


# ── PRODUCT TYPES ──

@admin.register(ProductType)
class ProductTypeAdmin(admin.ModelAdmin):

    list_display = ['name']

    search_fields = ['name']


# ── SUBSCRIBERS ──

@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):

    list_display = [
        'email',
        'created_at'
    ]

    search_fields = [
        'email'
    ]