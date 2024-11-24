from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Sum, F, Q
from django.utils import timezone
from django.db.models import Sum
from rest_framework import views
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

class ProductView(views.APIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

    
    
    def post(self,request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def get(self,request):
        queryset = Product.objects.all()
        serializer = ProductSerializer(queryset,many=True)
        return Response(serializer.data)
    


class ProductDetail(views.APIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    
    def get_object(self,pk):
        print(111111111111111111111111111111111111111111111111111)
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response({'detail':'Bunday id lik product topilmadi'},status=status.HTTP_404_NOT_FOUND)
    
    def get(self,request,pk):
        product = self.get_object(pk)
        data  = {
            'name':product.name,
            'time_per_unit':product.time_per_unit
        }
        return Response(data)
    def put(self,request,pk):
        product = self.get_object(pk)
        serializer = self.serializer_class(product,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,pk):
        product = self.get_object(pk)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def patch(self,request,pk):
        product = self.get_object(pk)
        serializer = self.serializer_class(product,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)