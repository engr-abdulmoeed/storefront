from django.urls import path
from store.views import ProductList, ProductDetail, CollectionDetail, CollectionList


urlpatterns = [
    path('products/', ProductList.as_view()),
    path('products/<int:id>/', ProductDetail.as_view()),
    path('collections/', CollectionList.as_view()),
    path('collections/<int:pk>/', CollectionDetail.as_view(),
         name='collection-detail')
]
