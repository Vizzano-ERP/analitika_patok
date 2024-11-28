from typing import List

from .views import ProductView,ProductDetail
from .patokview import ProductionLineViewSet,ProductionLineDetail
from .patokadata import PatokAnalyticsView
from .hourly import Hourly,ClockView
from .patokish import PatokDailyIshViewSet
from django.urls import path, URLPattern, URLResolver
from rest_framework import routers
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
clock = router.register('clock', ClockView)

urlpatterns = [
    path('product/', ProductView.as_view(), name='product'),
    path('patokish/', PatokDailyIshViewSet.as_view(), name='patokish'),
    path('patok/', ProductionLineViewSet.as_view(), name='patok'),
    path('patok/<int:pk>/', ProductionLineDetail.as_view(), name='patok_detail'),
    path('product/<int:pk>/', ProductDetail.as_view(), name='product_detail'),
    path('patokanalytics/', PatokAnalyticsView.as_view(), name='patokanalytics'),
    path('hourly/', Hourly.as_view(), name='hourly'),
]
urlpatterns += router.urls


