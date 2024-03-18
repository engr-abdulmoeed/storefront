from django.shortcuts import render
from store.models import Product, OrderItem


def say_hello(request):
    ordered_products = OrderItem.objects.values_list('product__title', flat=True).order_by('product__title').distinct()

    return render(request, 'hello.html', {'name': 'Moeed', 'product_titles': list(ordered_products)})
