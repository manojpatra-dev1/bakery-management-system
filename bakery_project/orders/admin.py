from django.contrib import admin
from .models import Product, Order, OrderItem

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'price', 'is_available', 'created_at']
    search_fields = ['name']
    list_filter = ['is_available']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer_name', 'customer_phone', 'status', 'total_price', 'created_at']
    search_fields = ['customer_name', 'customer_phone']
    list_filter = ['status', 'created_at']

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'product', 'quantity', 'price_at_time']
    search_fields = ['order__customer_name']