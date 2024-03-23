from django.shortcuts import render
from store.models import Product, Order, OrderItem, Customer
from django.db.models import F, Func, Value
from django.db.models.functions import Concat


def say_hello(request):
    # queryset = Customer.objects.annotate(full_name=Func(
    #     F('first_name'), Value(' '), F('last_name'), function='CONCAT'))

    queryset = Customer.objects.annotate(
        full_name=Concat('first_name', Value(' '), 'last_name', ))

    return render(request, 'hello.html', {'name': 'Moeed', 'customers': list(queryset)})
