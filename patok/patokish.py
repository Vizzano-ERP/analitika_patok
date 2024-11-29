from django.db.models import Sum , F,Q,ExpressionWrapper,FloatField
from django.utils import timezone
from rest_framework import serializers
from .models import PatokDailyProducts,PatokDailyIsh,Product,ProductionLine
from .serializers import PatokDailyIshProductsSerializer,PatokDailyIshSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import PatokishSerializer

class PatokDailyIshViewSet(APIView): 
    serializer_class = PatokishSerializer 
    
    def post(self, request): 
        print(request.data) 
        serializer = PatokishSerializer(data=request.data) 
        
        if serializer.is_valid(): 
            try: 
                porductts = serializer.validated_data['productlar'] 
                patok_Id = serializer.validated_data['production_line'] 
                patok = ProductionLine.objects.get(id=patok_Id) 
                worker_time = patok.worker_time_per_day 
                workers_count = serializer.validated_data['workers_count'] 
                umimiy_minut = worker_time * workers_count 
                products = [] 
                
                # Process each product
                for product_id in porductts: 
                    product = Product.objects.get(id=product_id) 
                    product_time = product.time_per_unit 
                    kutilayotgan = umimiy_minut / product_time 
                    real_ish = 0 
                    
                    # Create PatokDailyProducts entry
                    patok_product = PatokDailyProducts.objects.create( 
                        product=product, 
                        kutilayotgan=kutilayotgan, 
                        real_ish=real_ish 
                    ) 
                    products.append(patok_product.id) 
                
                # Create PatokDailyIsh entry
                patok_daily_ish = PatokDailyIsh.objects.create( 
                    production_line=patok, 
                    workers_count=workers_count, 
                    total_minutes=umimiy_minut 
                ) 
                patok_daily_ish.productlar.set(products) 
                patok_daily_ish.save() 
                
                # Fetch the current statistics for the created PatokDailyIsh
                total_minutes = patok_daily_ish.workers_count * patok_daily_ish.production_line.worker_time_per_day
                response_data = {
                    "production_line_data": {
                        "id": patok_daily_ish.production_line.id,
                        "name": patok_daily_ish.production_line.name,
                        "worker_time_per_day": patok_daily_ish.production_line.worker_time_per_day,
                        "created_at": patok_daily_ish.production_line.created_at,
                        "updated_at": patok_daily_ish.production_line.updated_at
                    },
                    "workers_count": patok_daily_ish.workers_count,
                    # "total_minutes": patok_daily_ish.total_minutes,
                    'total_minutes': total_minutes,
                    'real_ish': patok_daily_ish.productlar.all().aggregate(Sum('real_ish'))['real_ish__sum'],
                    'expected_products': patok_daily_ish.productlar.all().aggregate(Sum('kutilayotgan'))['kutilayotgan__sum'],
                    'products_count': patok_daily_ish.soatlikproductpatok_set.all().aggregate(Sum('quantity'))['quantity__sum'],
                    "products": [
                        {
                            "product_id": product.product.id,
                            "product_name": product.product.name,
                            "kutilayotgan": total_minutes / product.product.time_per_unit,
                            "real_ish": product.real_ish,
                        } 
                        for product in patok_daily_ish.productlar.all()
                    ]
                }
                
            except Exception as e: 
                return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST) 
            
            # Return the response
            return Response(response_data, status=status.HTTP_201_CREATED) 
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PatokDailyIshDetail(APIView):
    serializer_class = PatokishSerializer
    def get_object(self,pk):
        try:
            return PatokDailyIsh.objects.get(pk=pk)
        except PatokDailyIsh.DoesNotExist:
            return Response({'detail':'Bunday id lik patok daily ish topilmadi'},status=status.HTTP_404_NOT_FOUND)
    def get(self,request,pk):
        patok_daily_ish = self.get_object(pk)
        serializer = PatokishSerializer(patok_daily_ish)
        return Response(serializer.data)
  

    

