from django.contrib import admin
from store.models import Collection, Product, Customer


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'unit_price']


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'membership']
    list_editable = ['membership']
    list_per_page = 10
    ordering = ['first_name', 'last_name']


admin.site.register(Collection)
