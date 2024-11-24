from rest_framework import serializers
from django.db.models import Sum, F, ExpressionWrapper, FloatField
from django.utils import timezone
from datetime import datetime, time
from .models import Product, ProductionLine, PatokDailyIsh, PatokDailyProducts, SoatlikProductPatok

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 
                  'name', 
                  'time_per_unit', 
                  'created_at', 
                  'updated_at']
        

class ProductionLineSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductionLine
        fields = [
            'id', 
            'name', 
            'worker_time_per_day',
            'created_at',
            'updated_at'
        ]

class PatokDailyIshProductsSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_time = serializers.IntegerField(source='product.time_per_unit', read_only=True)
    

    class Meta:
        model = PatokDailyProducts
        fields = [
            'id',
            'product',
            'product_name',
            'product_time',
            'kutilayotgan',
            'real_ish',
            'created_at',
            'updated_at'
            
        ]
        read_only_fields = ['kutilayotgan']

   
class PatokDailyIshSerializer(serializers.ModelSerializer):
    production_line_detail = ProductionLineSerializer(source='production_line', read_only=True)
    productlar = PatokDailyIshProductsSerializer(many=True)
    
    
    class Meta:
        model = PatokDailyIsh
        fields = [
            'id',
            'production_line',
            'production_line_detail',
            'workers_count',
            'total_minutes',
            'productlar',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['total_minutes']



    def validate_workers_count(self, value):
        if value <= 0:
            raise serializers.ValidationError("Ishchilar soni 0 dan katta bo'lishi kerak")
        return value

class SoatlikProductPatokSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    patok = ProductionLineSerializer()
    class Meta:
        model = SoatlikProductPatok
        fields = [
            'id',
            'product',
            'patok',
            'quantity',
            'created_at',
            'updated_at'
        ]

    
class SoatlikProductPatokCreateUpdateSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), required=True)
    patok = serializers.PrimaryKeyRelatedField(queryset=ProductionLine.objects.all(), required=True)
    class Meta:
        model = SoatlikProductPatok
        fields = ['product', 'patok', 'quantity','created_at','updated_at']



   
class PatokbyDate(serializers.Serializer):
    date = serializers.ListField(child=serializers.DateField())

    def validate_date(self, value):
        # datetimeligni tekshirish kerak 
        for date in value:
            if date > timezone.now().date():
                raise serializers.ValidationError("Kun bugundan katta bo'lishi mumkin emas")
        return value
    


from rest_framework import serializers
from datetime import datetime
class PatokishSerializer(serializers.Serializer):
    production_line = serializers.IntegerField()
    workers_count = serializers.IntegerField()
    productlar = serializers.ListField(child=serializers.IntegerField(),required=True)

    def validate(self, attrs):
        now = datetime.now()
        patok_id = attrs['production_line']
        if PatokDailyIsh.objects.filter(production_line=patok_id, created_at__date=now.date()).exists():
            raise serializers.ValidationError("Bu patok uchun kunlik ish mavjud")
        if attrs['workers_count'] <= 0:
            raise serializers.ValidationError("Ishchilar soni 0 dan katta bo'lishi kerak")
        if len(attrs['productlar']) == 0:
            raise serializers.ValidationError("Mahsulotlar ro'yxati bo'sh bo'lishi mumkin emas")
        return attrs
