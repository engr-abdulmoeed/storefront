from django.shortcuts import render
from django.db.models import Q, F
from django.http import HttpResponse
from store.models import Product


def say_hello(request):
    queryset = Product.objects.filter(inventory=F('unit_price'))
    
    return render(request, 'hello.html', {'name': 'Moeed', 'products': list(queryset)})
