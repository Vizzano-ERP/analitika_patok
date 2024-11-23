from .serializers import ProductionLineSerializer
from rest_framework.viewsets import ModelViewSet
from .models import ProductionLine
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import status
from rest_framework.response import Response

class PatokVIew(ModelViewSet):
    queryset = ProductionLine.objects.all()
    serializer_class = ProductionLineSerializer

    @swagger_auto_schema(
        operation_description="Mahsulotni o'chirish",
        responses={
            204: 'Mahsulot muvaffaqiyatli o\'chirildi.',
            400: openapi.Response(
                description="Mahsulotni o'chirish mumkin emas, chunki u DailyProductionProduct'da ishlatilmoqda",
                examples={"error": "This product is used in DailyProductionProduct"}
            ),
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


