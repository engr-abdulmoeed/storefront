from django.urls import path
from store.views import ProductViewSet, CollectionViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('products', ProductViewSet)
router.register('collections', CollectionViewSet)

urlpatterns = router.urls
