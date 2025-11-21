from django.contrib import admin
from ShopifyApp.models import Product,Category,Cart,CartItem

# Register your models here.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # fields=['name','discription']
    # exclude=('name','discription')
    list_display=['name','discription']


# @admin.register(Category)
# class Category(admin.ModelAdmin):
#     fields=['name']
#     exclude=['name']
#     list_display=['name']


# admin.site.register(Product)
admin.site.register(Category)

admin.site.register(Cart)
admin.site.register(CartItem)





