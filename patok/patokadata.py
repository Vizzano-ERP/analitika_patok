from django.db.models import Sum, F, Q, ExpressionWrapper, FloatField, Avg, Count
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from datetime import datetime, timedelta
from django.db.models.functions import TruncDate, TruncWeek, TruncMonth, TruncYear
from .models import PatokDailyIsh, PatokDailyProducts

class PatokAnalyticsView(APIView):
    """
    Patok ishlab chiqarish hisoboti uchun view
    Turli vaqt oraliqlarida hisobot olish mumkin
    """
    



    def get(self,request):
        try:
            start_date_str = request.query_params.get('start_date')
            end_date_str = request.query_params.get('end_date')
            print(start_date_str, end_date_str)
            
            if end_date_str and start_date_str:
                queryset = PatokDailyIsh.objects.filter(created_at__date__gte=start_date_str, created_at__date__lte=end_date_str)
            elif start_date_str:
                queryset = PatokDailyIsh.objects.filter(created_at__date=start_date_str)
            else:
                queryset = PatokDailyIsh.objects.all()
            queryset = queryset.select_related(
                'production_line'
            ).prefetch_related(
                'productlar__product'
            )
            analytics = {}  
            analytics = {}
            for item in queryset:
                day = str(item.created_at.date()) # Kunni aniqlash
                if day not in analytics:
                    analytics[day] = []  # Kun uchun bo'sh ro'yxat

                # Patok ma'lumotlarini yaratish
                product = item.productlar.all().first()
                patok_entry = {
                    'patok': item.production_line.name,
                    'patok_id': item.production_line.id,
                    'workers_count': item.workers_count,
                    'total_minutes': item.total_minutes,
                    'products': [
                        {
                            'product_name': product.product.name,
                            'product_id': product.product.id,
                            'product_time':product.product.time_per_unit,
                            'kutilayotgan': product.kutilayotgan,
                            'real_ish': product.real_ish,
                        }
                    ]
                }
                analytics[day].append(patok_entry)
                
            analytics_list = [
                {
                    "date": day,
                    "patoks": patok_list
                }
                for day, patok_list in analytics.items()
            ]

            return Response(analytics_list, status=status.HTTP_200_OK)


              
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)