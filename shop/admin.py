from django.contrib import admin

# Register your models here.
from django.contrib import admin

from .models import Category, Perfume, Cart, Cartitems

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'category_id', 'slug', 'featured_product', 'icon', 'gender']

admin.site.register(Category, CategoryAdmin)


class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description', 'discount', 'image', 'price', 'slug', 'inventory', 'top_deal', 'flash_sales']

admin.site.register(Perfume, ProductAdmin)



class CartAdmin(admin.ModelAdmin):
    list_display = ['id']

admin.site.register(Cart, CartAdmin)


class CartItemAdmin(admin.ModelAdmin):
    list_display = ['cart', 'perfume', 'quantity']

admin.site.register(Cartitems, CartItemAdmin)


