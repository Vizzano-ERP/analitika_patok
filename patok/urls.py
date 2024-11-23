from rest_framework.routers import DefaultRouter
from .views import (
    ProductViewSet, ProductionLineViewSet,
    PatokDailyIshViewSet, SoatlikProductPatokViewSet
)

router = DefaultRouter()
router.register('products', ProductViewSet)
router.register('production-lines', ProductionLineViewSet)
router.register('daily-production', PatokDailyIshViewSet)
router.register('hourly-production', SoatlikProductPatokViewSet)

urlpatterns = router.urls