from rest_framework import serializers
from .models import Product, ProductionLine, DailyProduction, DailyProductionProduct, ProductionHourlyRecord


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'time_per_unit']
