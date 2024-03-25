from typing import Any
from django.contrib import admin
from django.db.models.query import QuerySet
from django.http import HttpRequest
from store.models import Collection, OrderItem, Product, Customer, Order
from django.db.models import Count
from django.utils.html import format_html, urlencode
from django.urls import reverse


class InventoryFilter(admin.SimpleListFilter):
    title = 'inventory'
    parameter_name = 'inventory'

    def lookups(self, request, model_admin) -> list[tuple[Any, str]]:
        return [('<10', 'Low')]

    def queryset(self, request: Any, queryset: QuerySet[Product]) -> QuerySet[Product] | None:
        if self.value() == '<10':
            return queryset.filter(inventory__lt=10)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    autocomplete_fields = ['collection']
    prepopulated_fields = {'slug': ['title']}
    list_display = ['title', 'unit_price',
                    'inventory_status', 'collection_title']
    list_editable = ['unit_price']
    list_per_page = 10
    list_select_related = ['collection']
    list_filter = ['collection', 'last_update', InventoryFilter]
    actions = ['clear_inventory']
    search_fields = ['title']

    def collection_title(self, product):
        return product.collection.title

    @admin.display(ordering='inventory')
    def inventory_status(self, product):
        if product.inventory < 10:
            return 'Low'
        else:
            return 'OK'

    @admin.action(description='Clear Inventory')
    def clear_inventory(self, request, queryset: QuerySet[Product]):
        updated_count = queryset.update(inventory=0)
        self.message_user(
            request, f'{updated_count} products were successfully updated.')


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'membership', 'orders_count']
    list_editable = ['membership']
    list_per_page = 10
    ordering = ['first_name', 'last_name']
    search_fields = ['first_name__istartswith', 'last_name__istartswith']

    @admin.display(ordering='orders_count')
    def orders_count(self, customer):
        url = reverse('admin:store_order_changelist') + '?' + \
            urlencode({'customer__id': str(customer.id)})
        return format_html('<a href="{}">{}</a>', url, customer.orders_count)

    def get_queryset(self, request: HttpRequest) -> QuerySet[Customer]:
        return super().get_queryset(request).annotate(orders_count=Count('order'))


class OrderItemInline(admin.TabularInline):
    autocomplete_fields = ['product']
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'placed_at', 'customer']
    autocomplete_fields = ['customer']
    inlines = [OrderItemInline]


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    search_fields = ['title']
    list_display = ['title', 'products_count']

    @admin.display(ordering='products_count')
    def products_count(self, collection):
        url = reverse('admin:store_product_changelist') + '?' + \
            urlencode({'collection__id': str(collection.id)})
        return format_html('<a href="{}">{}</a>', url, collection.products_count)

    def get_queryset(self, request: HttpRequest) -> QuerySet[Collection]:
        return super().get_queryset(request).annotate(products_count=Count('product'))
