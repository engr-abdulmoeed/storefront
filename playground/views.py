from django.shortcuts import render
from django.db.models import Q, F
from django.http import HttpResponse
from store.models import Product


def say_hello(request):
    # 0, 1, 2, 3, 4
    queryset = Product.objects.all()[:5]
    # 5, 6, 7, 8, 9
    queryset = Product.objects.all()[5:10]

    return render(request, 'hello.html', {'name': 'Moeed', 'products': list(queryset)})
