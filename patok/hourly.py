from .serializers import HourlyProductPatokSerializer
from .models import PatokDailyIsh
from .models import SoatlikProductPatok,Product,ProductionLine,PatokDailyProducts,SoatlikProductPatok
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from datetime import datetime

class Hourly(APIView):
    serializer_class = HourlyProductPatokSerializer

    def post(self, request):
        data = request.data
        sana = data.get('sana')  # format: "YYYY-MM-DD"
        clock_id = data.get('clock_id')
        patok_id = data.get('patok_id')
        product_id = data.get('product_id')
        quantity = data.get('quantity', 1) 
        sana_date = datetime.strptime(sana,'%Y-%m-%d').date()

        daily_ish = PatokDailyIsh.objects.get(created_at__date=sana_date,production_line=patok_id)
        products = daily_ish.productlar.get(product=product_id)
        products.real_ish += quantity
        products.save()

        soatlik_product = SoatlikProductPatok.objects.create(
           patok_id = patok_id,
           product_id = product_id,
           clock_id = clock_id,
           patokdailyish_id = daily_ish.id,
           patokproducts_id = products.id,
           quantity = quantity

        )
        soatlik_product.save()
        data = {}
        data['patok_id'] = patok_id
        data['product_id'] = product_id
        data['clock_id'] = clock_id
        data['quantity'] = quantity
        data['sana'] = sana
        return Response(data,status=status.HTTP_201_CREATED)
    
    def get(self,request):
        queryset = SoatlikProductPatok.objects.all()
        serializer = HourlyProductPatokSerializer(queryset,many=True)
        return Response(serializer.data)