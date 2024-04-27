from django.http import HttpRequest
from rest_framework.response import Response
from rest_framework.views import APIView
from store.models import Product, Collection
from store.serializers import ProductSerializer, CollectionSerialzier
from django.shortcuts import get_object_or_404
from rest_framework import status
from django.db.models import Count


class ProductList(APIView):
    def get(self, request: HttpRequest) -> Response:
        queryset = Product.objects.all().select_related('collection')
        serializer = ProductSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request: HttpRequest) -> Response:
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ProductDetail(APIView):
    def get(self, request: HttpRequest, id: int) -> Response:
        product = get_object_or_404(Product, pk=id)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def put(self, request: HttpRequest, id: int) -> Response:
        product = get_object_or_404(Product, pk=id)
        serializer = ProductSerializer(instance=product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request: HttpRequest, id: int) -> Response:
        product = get_object_or_404(Product, pk=id)
        if product.orderitems.count() > 0:
            return Response(data='Product can not be deleted because it is associated with an OrderItem', status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response('Product Deleted', status=status.HTTP_204_NO_CONTENT)


class CollectionList(APIView):
    def get(self, request: HttpRequest) -> Response:
        queryset = Collection.objects.annotate(
            products_count=Count('product')).all()
        serializer = CollectionSerialzier(queryset, many=True)
        return Response(serializer.data)

    def post(self, request: HttpRequest) -> Response:
        serializer = CollectionSerialzier(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CollectionDetail(APIView):
    def get(self, request: HttpRequest, pk: int) -> Response:
        collection = get_object_or_404(Collection.objects.annotate(
            products_count=Count('products')).all(), pk=pk)
        serializer = CollectionSerialzier(collection)
        return Response(serializer.data)

    def put(self, request: HttpRequest, pk: int) -> Response:
        collection = get_object_or_404(Collection.objects.annotate(
            products_count=Count('products')).all(), pk=pk)
        serializer = CollectionSerialzier(
            instance=collection, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request: HttpRequest, pk: int) -> Response:
        collection = get_object_or_404(Collection.objects.annotate(
            products_count=Count('products')).all(), pk=pk)
        if collection.products.count() > 0:
            return Response(data='Collection can not be deleted because it includes one or more product.', status=status.HTTP_405_METHOD_NOT_ALLOWED)
        collection.delete()
        return Response('Collection Deleted', status=status.HTTP_204_NO_CONTENT)
