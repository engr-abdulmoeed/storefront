from django.urls import path
from store.views import ProductViewSet, CollectionViewSet


urlpatterns = [
    path('products/', ProductViewSet.as_view()),
    path('products/<int:pk>/', ProductViewSet.as_view()),
    path('collections/', CollectionViewSet.as_view()),
    path('collections/<int:pk>/', CollectionViewSet.as_view(),
         name='collection-detail')
]
