from django.contrib import admin
from .models import Category, Product, ProductImage, CurrencyRates


# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "sku"]


admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage)
admin.site.register(CurrencyRates)
