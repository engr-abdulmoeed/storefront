from rest_framework.decorators import api_view
from rest_framework.response import Response
from store.models import Product, Collection
from store.serializers import ProductSerializer, CollectionSerialzier
from django.shortcuts import get_object_or_404


@api_view()
def product_list(request):
    queryset = Product.objects.all().select_related('collection')
    serializer = ProductSerializer(
        queryset, many=True, context={'request': request})
    return Response(serializer.data)


@api_view()
def product_detail(request, id):
    product = get_object_or_404(Product, pk=id)
    serializer = ProductSerializer(product)
    return Response(serializer.data)


@api_view()
def collection_detail(request, pk):
    collection = get_object_or_404(Collection, pk=pk)
    serializer = CollectionSerialzier(collection)
    return Response(serializer.data)
