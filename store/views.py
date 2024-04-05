from django.http import HttpRequest
from rest_framework.decorators import api_view
from rest_framework.response import Response
from store.models import Product, Collection
from store.serializers import ProductSerializer, CollectionSerialzier
from django.shortcuts import get_object_or_404
from rest_framework import status
from django.db.models import Count


@api_view(['GET', 'POST'])
def product_list(request: HttpRequest):
    if request.method == 'GET':
        queryset = Product.objects.all().select_related('collection')
        serializer = ProductSerializer(queryset, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def product_detail(request: HttpRequest, id):
    product = get_object_or_404(Product, pk=id)
    if request.method == 'GET':
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = ProductSerializer(instance=product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    elif request.method == 'DELETE':
        if product.orderitems.count() > 0:
            return Response(data='Product can not be deleted because it is associated with an OrderItem', status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response('Product Deleted', status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def collection_list(request: HttpRequest):
    if request.method == 'GET':
        queryset = Collection.objects.annotate(
            products_count=Count('product')).all()
        serializer = CollectionSerialzier(queryset, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = CollectionSerialzier(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def collection_detail(request: HttpRequest, pk):
    collection = get_object_or_404(Collection.objects.annotate(
        products_count=Count('products')).all(), pk=pk)
    if request.method == 'GET':
        serializer = CollectionSerialzier(collection)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = CollectionSerialzier(
            instance=collection, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    elif request.method == 'DELETE':
        if collection.products.count() > 0:
            return Response(data='Collection can not be deleted because it includes one or more product.', status=status.HTTP_405_METHOD_NOT_ALLOWED)
        collection.delete()
        return Response('Collection Deleted', status=status.HTTP_204_NO_CONTENT)
