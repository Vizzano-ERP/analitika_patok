from rest_framework.viewsets import ModelViewSet
from .models import PatokDailyIsh,PatokDailyProducts
from .serializers import PatokDailyIshSerializer,PatokDailyIshProductsSerializer
from rest_framework import status
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema


class PatokDailyIshViewSet(ModelViewSet):
    queryset = PatokDailyIsh.objects.all()
    serializer_class = PatokDailyIshSerializer

    @swagger_auto_schema(
        operation_description="Mahsulotni o'chirish",
        responses={
            204: 'Mahsulot muvaffaqiyatli o\'chirildi.',
            400: 'Mahsulotni o\'chirish mumkin emas, chunki u DailyProductionProduct\'da ishlatilmoqda',
        }
    )
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        # Agar bu mahsulot boshqa joyda ishlatilgan bo'lsa, uni o'chirishga ruxsat berilmaydi
        if instance.dailyproductionproduct_set.exists():
            return Response(
                {"error": "This product is used in DailyProductionProduct"},
                status=status.HTTP_400_BAD_REQUEST
            )
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()
        # super().destroy(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        data_daily_product = request.data.pop('daily_production_product')
        daily_product_serializer = PatokDailyIshProductsSerializer(data=data_daily_product)
        request.data['daily_production_product'] = daily_product_serializer
        self.serializer_class(data=request.data).is_valid(raise_exception=True)
        self.serializer_class(data=request.data).save()
        return Response(status=status.HTTP_201_CREATED)
    