from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Sum, F, Q
from django.utils import timezone
from datetime import timedelta
from .models import (
    Product, ProductionLine, PatokDailyIsh,
    PatokDailyProducts, SoatlikProductPatok
)
from .serializers import (
    ProductSerializer, ProductionLineSerializer,
    PatokDailyIshSerializer, PatokDailyIshProductsSerializer,
    SoatlikProductPatokSerializer, SoatlikProductPatokCreateUpdateSerializer
)

class ProductViewSet(viewsets.ModelViewSet):
    """
    Mahsulotlar uchun ViewSet
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name', 'time_per_unit']
    ordering = ['name']

    @action(detail=True, methods=['get'])
    def production_stats(self, request, pk=None):
        """Mahsulot ishlab chiqarish statistikasi"""
        product = self.get_object()
        today = timezone.now().date()
        last_week = today - timedelta(days=7)

        # Oxirgi 7 kunlik statistika
        daily_stats = PatokDailyProducts.objects.filter(
            product=product,
            created_at__date__gte=last_week
        ).values('created_at__date').annotate(
            total_produced=Sum('real_ish'),
            total_expected=Sum('kutilayotgan')
        ).order_by('created_at__date')

        return Response({
            'product_name': product.name,
            'daily_stats': daily_stats
        })

class ProductionLineViewSet(viewsets.ModelViewSet):
    """
    Patoklar uchun ViewSet
    """
    queryset = ProductionLine.objects.all()
    serializer_class = ProductionLineSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']

    @action(detail=True, methods=['get'])
    def efficiency_report(self, request, pk=None):
        """Patok samaradorligi hisoboti"""
        patok = self.get_object()
        today = timezone.now().date()

        daily_production = PatokDailyIsh.objects.filter(
            production_line=patok,
            created_at__date=today
        ).first()

        if daily_production:
            return Response({
                'patok_name': patok.name,
                'workers_today': daily_production.workers_count,
                'total_minutes': daily_production.total_minutes,
                'products': PatokDailyIshProductsSerializer(
                    daily_production.productlar.all(), 
                    many=True
                ).data
            })
        return Response({'message': 'Bugun uchun ma\'lumot topilmadi'})

class PatokDailyIshViewSet(viewsets.ModelViewSet):
    """
    Kunlik ishlab chiqarish uchun ViewSet
    """
    queryset = PatokDailyIsh.objects.all()
    serializer_class = PatokDailyIshSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['production_line', 'created_at']
    ordering_fields = ['created_at', 'workers_count']
    ordering = ['-created_at']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        daily_ish = serializer.save()
        
        # Mahsulotlarni qo'shish
        products_data = request.data.get('products', [])
        for product_data in products_data:
            product = Product.objects.get(id=product_data['product'])
            kutilayotgan = (daily_ish.total_minutes / product.time_per_unit)
            
            PatokDailyProducts.objects.create(
                daily_ish=daily_ish,
                product=product,
                kutilayotgan=kutilayotgan,
                real_ish=product_data.get('real_ish', 0)
            )
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['get'])
    def daily_report(self, request, pk=None):
        """Kunlik hisobot"""
        daily_ish = self.get_object()
        products = daily_ish.productlar.all()
        
        total_expected = sum(p.kutilayotgan for p in products)
        total_actual = sum(p.real_ish for p in products)
        
        efficiency = (total_actual / total_expected * 100) if total_expected else 0
        
        return Response({
            'date': daily_ish.created_at.date(),
            'production_line': daily_ish.production_line.name,
            'workers': daily_ish.workers_count,
            'total_minutes': daily_ish.total_minutes,
            'efficiency': round(efficiency, 2),
            'products': PatokDailyIshProductsSerializer(products, many=True).data
        })

class SoatlikProductPatokViewSet(viewsets.ModelViewSet):
    """
    Soatlik mahsulot patok uchun ViewSet
    """
    queryset = SoatlikProductPatok.objects.all()
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['product', 'patok']
    ordering_fields = ['created_at', 'quantity']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return SoatlikProductPatokCreateUpdateSerializer
        return SoatlikProductPatokSerializer

    def get_queryset(self):
        queryset = super().get_queryset().select_related('product', 'patok')
        
        # Qo'shimcha filtrlar
        date = self.request.query_params.get('date')
        if date:
            queryset = queryset.filter(created_at__date=date)
            
        return queryset

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Patokda shu mahsulot borligini tekshirish
        existing = SoatlikProductPatok.objects.filter(
            product=serializer.validated_data['product'],
            patok=serializer.validated_data['patok']
        ).first()
        
        if existing:
            return Response(
                {'detail': 'Bu mahsulot ushbu patokda allaqachon mavjud'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'])
    def patok_stats(self, request):
        """Patok bo'yicha statistika"""
        patok_id = request.query_params.get('patok')
        if not patok_id:
            return Response(
                {'detail': 'Patok ID si ko\'rsatilmagan'},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        stats = SoatlikProductPatok.objects.filter(patok_id=patok_id).select_related(
            'product'
        ).values(
            'product__name'
        ).annotate(
            total_quantity=Sum('quantity')
        )
        
        return Response(stats)

    @action(detail=False, methods=['get'])
    def product_stats(self, request):
        """Mahsulot bo'yicha statistika"""
        product_id = request.query_params.get('product')
        if not product_id:
            return Response(
                {'detail': 'Mahsulot ID si ko\'rsatilmagan'},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        stats = SoatlikProductPatok.objects.filter(product_id=product_id).select_related(
            'patok'
        ).values(
            'patok__name'
        ).annotate(
            total_quantity=Sum('quantity')
        )
        
        return Response(stats)