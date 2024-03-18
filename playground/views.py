from django.shortcuts import render
from django.http import HttpResponse
from store.models import Product


def say_hello(request):
    queryset = Product.objects.filter(title__icontains='coffee')
    
    return render(request, 'hello.html', {'name': 'Moeed', 'products': list(queryset)})
