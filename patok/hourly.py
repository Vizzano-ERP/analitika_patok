from .serializers import HourlyProductPatokSerializer
from .models import PatokDailyIsh
from .models import SoatlikProductPatok,Product,ProductionLine,PatokDailyProducts,SoatlikProductPatok
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from datetime import datetime
from django.db import transaction
from .serializers import ClockSerializer
from .models import Clock
from django.db.models import Sum
class ClockView(ModelViewSet):
    serializer_class = ClockSerializer
    queryset = Clock.objects.all()
class Hourly(APIView):
    serializer_class = HourlyProductPatokSerializer

    @transaction.atomic
    def post(self, request):
        try :

        
            data = request.data
            sana = data.get('date') or str(datetime.now().date())
            
            clock_id = data.get('clock_id')
            patok_id = data.get('patok_id')
            product_id = data.get('product_id')
            quantity = data.get('quantity', 1)
            comment = data.get('comment', None)
            sub_query = SoatlikProductPatok.objects.filter(patok_id=patok_id,product_id=product_id,clock_id=clock_id,created_at__date=sana)
            if sub_query.exists():
                soatlik_product = SoatlikProductPatok.objects.get(patok_id=patok_id,product_id=product_id,clock_id=clock_id,created_at__date=sana)
                soatlik_product.quantity = quantity
                soatlik_product.save()
                data = {}
                real_ish = SoatlikProductPatok.objects.filter(created_at__date=sana,patok_id=patok_id,product_id=product_id).aggregate(Sum('quantity'))['quantity__sum'] or 0
                data = {}
                print(real_ish)
                data['real_ish'] = real_ish
                return Response(data,status=status.HTTP_201_CREATED)
            elif sub_query.exists() == False:
                
                sana_date = datetime.strptime(sana,'%Y-%m-%d').date()
                daily_ish = PatokDailyIsh.objects.get(created_at__date=sana_date,production_line=patok_id)
                products = daily_ish.productlar.get(product=product_id)

                soatlik_product = SoatlikProductPatok.objects.create(
                    patok_id = patok_id,
                    product_id = product_id,
                    clock_id = clock_id,
                    patokdailyish_id = daily_ish.id,
                    patokproducts_id = products.id,
                    quantity = quantity,
                    comment = comment

                )
                queery = SoatlikProductPatok.objects.filter(created_at__date=sana_date,patok_id=patok_id,product_id=product_id)
                real_ish = queery.aggregate(Sum('quantity'))['quantity__sum']
                # print(real_ish)
                soatlik_product.save()
                data = {}
                data['clock_id'] = clock_id                
                data['comment'] = comment
                data['real_ish'] = real_ish
                return Response(data,status=status.HTTP_201_CREATED) 
            else:
                return Response({'error':'Bunday ma\'lumot topilmadi'},status=status.HTTP_400_BAD_REQUEST)          
        except Exception as e:
            return Response({'error':str(e)},status=status.HTTP_400_BAD_REQUEST)
    


    def get(self,request):
        date = request.query_params.get('date')
        patok_id = request.query_params.get('patok_id')
        print(patok_id,date,'patok_id,date')
        if patok_id is None:
            return Response({'error':'Patok id kiritilmagan'},status=status.HTTP_400_BAD_REQUEST    )
        if date is None:
            date = datetime.now().date()
        else:
            date = datetime.strptime(date,'%Y-%m-%d').date()

        try:
            queryset = PatokDailyIsh.objects.get(created_at__date=date,production_line=patok_id)
            soats  = SoatlikProductPatok.objects.filter(patokdailyish=queryset.id)
            data_list = []
            for soat in soats:
                data_list.append({
                    'clock':{
                        'id':soat.clock.id,
                        'name':soat.clock.clock
                    },
                    'quantity':soat.quantity,
                    'comment':soat.comment
                })
            return Response(data_list,status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error':str(e)},status=status.HTTP_400_BAD_REQUEST)