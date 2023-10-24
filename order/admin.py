from django.contrib import admin
from .models import Order, OrderItem

# Register your models here.
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'created_at', 'status'] 
admin.site.register(Order, OrderAdmin)


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'perfume', 'price', 'quantity']

admin.site.register(OrderItem, OrderItemAdmin)
