from .views import ProductView,ProductDetail
from .patokview import ProductionLineViewSet,ProductionLineDetail
# from .patokanaliz import  PatokAnalyticsView
from .patokadata import PatokAnalyticsView
from .patokish import PatokDailyIshViewSet
from django.urls import path

urlpatterns = [
    path('product/', ProductView.as_view(), name='product'),
    path('patokish/', PatokDailyIshViewSet.as_view(), name='patokish'),
    path('patok/', ProductionLineViewSet.as_view(), name='patok'),
    path('patok/<int:pk>/', ProductionLineDetail.as_view(), name='patok_detail'),
    path('product/<int:pk>/', ProductDetail.as_view(), name='product_detail'),
    path('patokanalytics/', PatokAnalyticsView.as_view(), name='patokanalytics'),
]

