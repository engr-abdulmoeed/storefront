from store.views import ProductViewSet, CollectionViewSet, ReviewViewSet
from rest_framework_nested.routers import DefaultRouter, NestedDefaultRouter


router = DefaultRouter()
router.register('products', ProductViewSet, basename='products')
router.register('collections', CollectionViewSet)

products_router = NestedDefaultRouter(router, 'products', lookup='product')
products_router.register('reviews', ReviewViewSet, basename='product-reviews')

urlpatterns = router.urls + products_router.urls
