from django.db.models import Sum, F, Q, ExpressionWrapper, FloatField, Avg, Count
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from datetime import datetime, timedelta
from django.db.models.functions import TruncDate, TruncWeek, TruncMonth, TruncYear
from .models import PatokDailyIsh, PatokDailyProducts

# class PatokAnalyticsView(APIView):
#     """
#     Patok ishlab chiqarish hisoboti uchun view
#     Turli vaqt oraliqlarida hisobot olish mumkin
#     """
    
#     def _validate_dates(self, start_date_str: str, end_date_str: str = None) -> tuple:
#         """Sanalarni tekshirish va datetime formatiga o'tkazish"""
#         try:
#             start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            
#             if end_date_str:
#                 end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
#                 if end_date < start_date:
#                     raise ValueError("Tugash sanasi boshlanish sanasidan oldin bo'lishi mumkin emas")
#             else:
#                 end_date = timezone.now().date() + timedelta(days=1)
                
#             return start_date, end_date
            
#         except ValueError as e:
#             raise ValueError(f"Sana formati noto'g'ri: {str(e)}")

#     def get(self, request):
#         try:
#             # Query parametrlarini olish
#             start_date_str = request.query_params.get('start_date')
#             end_date_str = request.query_params.get('end_date')
#             report_type = request.query_params.get('report_type', 'daily')  # daily, weekly, monthly, yearly, custom
#             patok_id = request.query_params.get('patok_id')
            
#             # Agar start_date berilmagan bo'lsa, bugungi kunni olish
#             if not start_date_str:
#                 if report_type == 'daily':
#                     start_date = timezone.now().date()
#                 elif report_type == 'weekly':
#                     start_date = timezone.now().date() - timedelta(days=7)
#                 elif report_type == 'monthly':
#                     start_date = timezone.now().date() - timedelta(days=30)
#                 elif report_type == 'yearly':
#                     start_date = timezone.now().date() - timedelta(days=365)
#                 else:
#                     start_date = timezone.now().date()
#             else:
#                 start_date, end_date = self._validate_dates(start_date_str, end_date_str)

#             # Hisobot turi bo'yicha groupby funksiyasini tanlash
#             if report_type == 'daily':
#                 trunc_func = TruncDate('created_at')
#             elif report_type == 'weekly':
#                 trunc_func = TruncWeek('created_at')
#             elif report_type == 'monthly':
#                 trunc_func = TruncMonth('created_at')
#             elif report_type == 'yearly':
#                 trunc_func = TruncYear('created_at')
#             else:  # custom
#                 trunc_func = TruncDate('created_at')

#             # Asosiy queryset
#             queryset = PatokDailyIsh.objects.filter(
#                 created_at__date__gte=start_date,
#                 created_at__date__lt=end_date if end_date_str else timezone.now().date() + timedelta(days=1)
#             )

#             # Patok bo'yicha filterlash
#             if patok_id:
#                 queryset = queryset.filter(production_line_id=patok_id)

#             # Hisobot ma'lumotlarini yig'ish
#             from django.db.models import Prefetch
#             analytics = queryset.annotate(
#                 date=trunc_func
#             ).values(
#                 'date',
#                 'production_line__name'
#             ).annotate(
#                 workers_count=Sum('workers_count'),
#                 total_minutes=Sum('total_minutes'),
#                 total_products=Sum('productlar__real_ish'),
#                 expected_products=Sum('productlar__kutilayotgan'),
#                 products_count=Count('productlar'),
#                 efficiency=ExpressionWrapper(
#                     F('total_products') * 100.0 / F('expected_products'),
#                     output_field=FloatField()
#                 )
                

#             ).order_by('date', 'production_line__name')

#             # Umumiy statistika
#             total_stats = queryset.aggregate(
#                 total_workers=Sum('workers_count'),
#                 total_minutes_all=Sum('total_minutes'),
#                 total_products_all=Sum('productlar__real_ish'),
#                 total_expected_all=Sum('productlar__kutilayotgan'),
#                 avg_efficiency=ExpressionWrapper(
#                     Sum('productlar__real_ish') * 100.0 / Sum('productlar__kutilayotgan'),
#                     output_field=FloatField()
#                 )
#             )

#             # Mahsulotlar bo'yicha statistika
#             products_stats = queryset.values(
#                 'productlar__product__name'
#             ).annotate(
#                 total_produced=Sum('productlar__real_ish'),
#                 total_expected=Sum('productlar__kutilayotgan'),
#                 efficiency=ExpressionWrapper(
#                     F('total_produced') * 100.0 / F('total_expected'),
#                     output_field=FloatField()
#                 )
#             ).order_by('-total_produced')

#             response_data = {
#                 'report_type': report_type,
#                 'start_date': start_date,
#                 'end_date': end_date if end_date_str else timezone.now().date(),
#                 'total_statistics': total_stats,
#                 'products_statistics': products_stats,
#                 'daily_statistics': analytics
#             }

#             return Response(response_data)

#         except ValueError as e:
#             return Response(
#                 {'detail': str(e)}, 
#                 status=status.HTTP_400_BAD_REQUEST
#             )
#         except Exception as e:
#             return Response(
#                 {'detail': str(e)}, 
#                 status=status.HTTP_500_INTERNAL_SERVER_ERROR
#             )


# class PatokAnalyticsView(APIView):
#     """
#     Patok ishlab chiqarish hisoboti uchun view
#     Turli vaqt oraliqlarida hisobot olish mumkin
#     """
    
#     def _validate_dates(self, start_date_str: str, end_date_str: str = None) -> tuple:
#         """Sanalarni tekshirish va datetime formatiga o'tkazish"""
#         try:
#             start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            
#             if end_date_str:
#                 end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
#                 if end_date < start_date:
#                     raise ValueError("Tugash sanasi boshlanish sanasidan oldin bo'lishi mumkin emas")
#             else:
#                 end_date = timezone.now().date() + timedelta(days=1)
                
#             return start_date, end_date
            
#         except ValueError as e:
#             raise ValueError(f"Sana formati noto'g'ri: {str(e)}")

#     def get(self, request):
#         try:
#             # Query parametrlarini olish
#             start_date_str = request.query_params.get('start_date')
#             end_date_str = request.query_params.get('end_date')
#             report_type = request.query_params.get('report_type', 'daily')  # daily, weekly, monthly, yearly, custom
#             patok_id = request.query_params.get('patok_id')
            
#             # Agar start_date berilmagan bo'lsa, bugungi kunni olish
#             if not start_date_str:
#                 if report_type == 'daily':
#                     start_date = timezone.now().date()
#                 elif report_type == 'weekly':
#                     start_date = timezone.now().date() - timedelta(days=7)
#                 elif report_type == 'monthly':
#                     start_date = timezone.now().date() - timedelta(days=30)
#                 elif report_type == 'yearly':
#                     start_date = timezone.now().date() - timedelta(days=365)
#                 else:
#                     start_date = timezone.now().date()
#             else:
#                 start_date, end_date = self._validate_dates(start_date_str, end_date_str)

#             # Hisobot turi bo'yicha groupby funksiyasini tanlash
#             if report_type == 'daily':
#                 trunc_func = TruncDate('created_at')
#             elif report_type == 'weekly':
#                 trunc_func = TruncWeek('created_at')
#             elif report_type == 'monthly':
#                 trunc_func = TruncMonth('created_at')
#             elif report_type == 'yearly':
#                 trunc_func = TruncYear('created_at')
#             else:  # custom
#                 trunc_func = TruncDate('created_at')

#             # Asosiy queryset
#             queryset = PatokDailyIsh.objects.select_related(
#                 'production_line'
#             ).prefetch_related(
#                 'productlar__product'
#             ).filter(
#                 created_at__date__gte=start_date,
#                 created_at__date__lt=end_date if end_date_str else timezone.now().date() + timedelta(days=1)
#             )

#             # Patok bo'yicha filterlash
#             if patok_id:
#                 queryset = queryset.filter(production_line_id=patok_id)

#             # Hisobot ma'lumotlarini yig'ish
#             analytics = []
#             for patok_daily_ish in queryset:
#                 daily_data = {
#                     "production_line_data": {
#                         "id": patok_daily_ish.production_line.id,
#                         "name": patok_daily_ish.production_line.name,
#                         "worker_time_per_day": patok_daily_ish.production_line.worker_time_per_day,
#                         "created_at": patok_daily_ish.production_line.created_at,
#                         "updated_at": patok_daily_ish.production_line.updated_at
#                     },
#                     "workers_count": patok_daily_ish.workers_count,
#                     "total_minutes": patok_daily_ish.total_minutes,
#                     "date": trunc_func.resolve_expression(patok_daily_ish),
#                     'real_ish': patok_daily_ish.productlar.aggregate(Sum('real_ish'))['real_ish__sum'],
#                     'expected_products': patok_daily_ish.productlar.aggregate(Sum('kutilayotgan'))['kutilayotgan__sum'],
#                     'products_count': patok_daily_ish.productlar.count(),
#                     "products": [
#                         {
#                             "product_id": product.product.id,
#                             "product_name": product.product.name,
#                             "kutilayotgan": product.kutilayotgan,
#                             "real_ish": product.real_ish,
#                         } 
#                         for product in patok_daily_ish.productlar.all()
#                     ]
#                 }
#                 analytics.append(daily_data)

#             # Umumiy statistika
#             total_stats = queryset.aggregate(
#                 total_workers=Sum('workers_count'),
#                 total_minutes_all=Sum('total_minutes'),
#                 total_products_all=Sum('productlar__real_ish'),
#                 total_expected_all=Sum('productlar__kutilayotgan'),
#                 avg_efficiency=ExpressionWrapper(
#                     Sum('productlar__real_ish') * 100.0 / Sum('productlar__kutilayotgan'),
#                     output_field=FloatField()
#                 )
#             )

#             # Mahsulotlar bo'yicha statistika
#             products_stats = queryset.values(
#                 'productlar__product__id',
#                 'productlar__product__name'
#             ).annotate(
#                 total_produced=Sum('productlar__real_ish'),
#                 total_expected=Sum('productlar__kutilayotgan'),
#                 efficiency=ExpressionWrapper(
#                     F('total_produced') * 100.0 / F('total_expected'),
#                     output_field=FloatField()
#                 )
#             ).order_by('-total_produced')

#             response_data = {
#                 'report_type': report_type,
#                 'start_date': start_date,
#                 'end_date': end_date if end_date_str else timezone.now().date(),
#                 'total_statistics': total_stats,
#                 'products_statistics': products_stats,
#                 'daily_statistics': analytics
#             }

#             return Response(response_data)

#         except ValueError as e:
#             return Response(
#                 {'detail': str(e)}, 
#                 status=status.HTTP_400_BAD_REQUEST
#             )
#         except Exception as e:
#             return Response(
#                 {'detail': str(e)}, 
#                 status=status.HTTP_500_INTERNAL_SERVER_ERROR
#             )


class PatokAnalyticsView(APIView):
    """
    Patok ishlab chiqarish hisoboti uchun view
    Turli vaqt oraliqlarida hisobot olish mumkin
    """
    
    def _get_truncated_date(self, date, report_type):
        """Date ni report type ga qarab truncate qilish"""
        if report_type == 'weekly':
            return date - timedelta(days=date.weekday())
        elif report_type == 'monthly':
            return date.replace(day=1)
        elif report_type == 'yearly':
            return date.replace(month=1, day=1)
        return date.date()

    def _validate_dates(self, start_date_str: str, end_date_str: str = None) -> tuple:
        """Sanalarni tekshirish va datetime formatiga o'tkazish"""
        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            
            if end_date_str:
                end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
                if end_date < start_date:
                    raise ValueError("Tugash sanasi boshlanish sanasidan oldin bo'lishi mumkin emas")
            else:
                end_date = timezone.now().date() + timedelta(days=1)
                
            return start_date, end_date
            
        except ValueError as e:
            raise ValueError(f"Sana formati noto'g'ri: {str(e)}")

    def get(self, request):
        try:
            # Query parametrlarini olish
            start_date_str = request.query_params.get('start_date')
            end_date_str = request.query_params.get('end_date')
            report_type = request.query_params.get('report_type', 'daily')  # daily, weekly, monthly, yearly, custom
            patok_id = request.query_params.get('patok_id')
            
            # Agar start_date berilmagan bo'lsa, bugungi kunni olish
            if not start_date_str:
                if report_type == 'daily':
                    start_date = timezone.now().date()
                elif report_type == 'weekly':
                    start_date = timezone.now().date() - timedelta(days=7)
                elif report_type == 'monthly':
                    start_date = timezone.now().date() - timedelta(days=30)
                elif report_type == 'yearly':
                    start_date = timezone.now().date() - timedelta(days=365)
                else:
                    start_date = timezone.now().date()
            else:
                start_date, end_date = self._validate_dates(start_date_str, end_date_str)

            # Hisobot turi bo'yicha groupby funksiyasini tanlash
            if report_type == 'daily':
                trunc_func = TruncDate('created_at')
            elif report_type == 'weekly':
                trunc_func = TruncWeek('created_at')
            elif report_type == 'monthly':
                trunc_func = TruncMonth('created_at')
            elif report_type == 'yearly':
                trunc_func = TruncYear('created_at')
            else:  # custom
                trunc_func = TruncDate('created_at')

            # Asosiy queryset
            queryset = PatokDailyIsh.objects.select_related(
                'production_line'
            ).prefetch_related(
                'productlar__product'
            ).filter(
                created_at__date__gte=start_date,
                created_at__date__lt=end_date if end_date_str else timezone.now().date() + timedelta(days=1)
            )

            # Patok bo'yicha filterlash
            if patok_id:
                queryset = queryset.filter(production_line_id=patok_id)

            # Hisobot ma'lumotlarini yig'ish
            analytics = []
            for patok_daily_ish in queryset:
                daily_data = {
                    "production_line_data": {
                        "id": patok_daily_ish.production_line.id,
                        "name": patok_daily_ish.production_line.name,
                        "worker_time_per_day": patok_daily_ish.production_line.worker_time_per_day,
                        "created_at": patok_daily_ish.production_line.created_at,
                        "updated_at": patok_daily_ish.production_line.updated_at
                    },
                    "workers_count": patok_daily_ish.workers_count,
                    "total_minutes": patok_daily_ish.total_minutes,
                    "date": self._get_truncated_date(patok_daily_ish.created_at, report_type),
                    'real_ish': patok_daily_ish.productlar.aggregate(Sum('real_ish'))['real_ish__sum'],
                    'expected_products': patok_daily_ish.productlar.aggregate(Sum('kutilayotgan'))['kutilayotgan__sum'],
                    'products_count': patok_daily_ish.productlar.count(),
                    # "products": [
                    #     {
                    #         "product_id": product.product.id,
                    #         "product_name": product.product.name,
                    #         "kutilayotgan": product.kutilayotgan,
                    #         "real_ish": product.real_ish,
                    #     } 
                    #     for product in patok_daily_ish.productlar.all()
                    # ]
                }
                analytics.append(daily_data)

            # Umumiy statistika
            total_stats = queryset.aggregate(
                total_workers=Sum('workers_count'),
                total_minutes_all=Sum('total_minutes'),
                total_products_all=Sum('productlar__real_ish'),
                total_expected_all=Sum('productlar__kutilayotgan'),
                avg_efficiency=ExpressionWrapper(
                    Sum('productlar__real_ish') * 100.0 / Sum('productlar__kutilayotgan'),
                    output_field=FloatField()
                )
            )

            products_stats = queryset.values(
                'productlar__product__id',
                'productlar__product__name'
            ).annotate(
                total_produced=Sum('productlar__real_ish'),
                total_expected=Sum('productlar__kutilayotgan'),
                efficiency=ExpressionWrapper(
                    F('total_produced') * 100.0 / F('total_expected'),
                    output_field=FloatField()
                )
            ).order_by('-total_produced')

            response_data = {
                'report_type': report_type,
                'start_date': start_date,
                'end_date': end_date if end_date_str else timezone.now().date(),
                'total_statistics': total_stats,
                'products_statistics': products_stats,
                'daily_statistics': analytics
            }

            return Response(response_data)

        except ValueError as e:
            return Response(
                {'detail': str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {'detail': str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )





