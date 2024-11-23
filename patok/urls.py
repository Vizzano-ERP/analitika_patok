from django.urls import path, include
from rest_framework.routers import DefaultRouter
from  .product import ProductViewSet

router = DefaultRouter()
router.register('products', ProductViewSet)

urlpatterns = [
    path('', include(router.urls)),
]