from django.urls import path
from store.views import product_list, product_detail, collection_detail


urlpatterns = [
    path('product/', product_list),
    path('product/<int:id>/', product_detail),
    path('collection/<int:pk>/', collection_detail, name='collection-detail')
]
