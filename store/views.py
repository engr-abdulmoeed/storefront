from rest_framework.decorators import api_view
from rest_framework.response import Response
from store.models import Product
from store.serializers import ProductSerializer
from rest_framework import status
from django.shortcuts import get_object_or_404


@api_view()
def product_list(request):
    queryset = Product.objects.all()
    serializer = ProductSerializer(queryset, many=True)
    return Response(serializer.data)


@api_view()
def product_detail(request, id):
    product = get_object_or_404(Product, pk=id)
    serializer = ProductSerializer(product)
    return Response(serializer.data)
