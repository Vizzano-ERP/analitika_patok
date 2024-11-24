from .serializers import HourlyProductPatokSerializer
from .models import PatokDailyIsh
from .models import SoatlikProductPatok,Product,ProductionLine,PatokDailyProducts
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class Hourly(APIView):
    serializer_class = HourlyProductPatokSerializer

    def post(self, request):
        serializer = HourlyProductPatokSerializer(data=request.data)
        if serializer.is_valid():
            date = serializer.validated_data['date']    
            product_id = serializer.validated_data['product']
            product = Product.objects.get(id=product_id)
            patok = ProductionLine.objects.get(id=serializer.validated_data['production_line'])
            quantity = serializer.validated_data['quantity']
            product = PatokDailyProducts.objects.get(
                product=product,
                patok=patok,
            )
            product.real_ish += quantity
            product.save()
            soatlik_product_patok = SoatlikProductPatok.objects.create(
                product=product,
                quantity=quantity,
                clock=date,
                patok=patok,

            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)