from django.http import HttpRequest
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from store.models import Product, Collection
from store.serializers import ProductSerializer, CollectionSerialzier
from django.shortcuts import get_object_or_404
from rest_framework import status
from django.db.models import Count


class ProductList(ListCreateAPIView):
    queryset = Product.objects.select_related('collection').all()
    serializer_class = ProductSerializer

    def get_serializer_context(self):
        return {'request': self.request}


class ProductDetail(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def delete(self, request: HttpRequest, pk: int) -> Response:
        product = get_object_or_404(Product, pk=pk)
        if product.orderitems.count() > 0:
            return Response(data='Product can not be deleted because it is associated with an OrderItem', status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response('Product Deleted', status=status.HTTP_204_NO_CONTENT)


class CollectionList(ListCreateAPIView):
    queryset = Collection.objects.annotate(
        products_count=Count('products')).all()
    serializer_class = CollectionSerialzier


class CollectionDetail(RetrieveUpdateDestroyAPIView):
    queryset = Collection.objects.annotate(
        products_count=Count('products')).all()
    serializer_class = CollectionSerialzier

    def delete(self, request: HttpRequest, pk: int) -> Response:
        collection = get_object_or_404(Collection.objects.annotate(
            products_count=Count('products')).all(), pk=pk)
        if collection.products.count() > 0:
            return Response(data='Collection can not be deleted because it includes one or more product.', status=status.HTTP_405_METHOD_NOT_ALLOWED)
        collection.delete()
        return Response('Collection Deleted', status=status.HTTP_204_NO_CONTENT)
