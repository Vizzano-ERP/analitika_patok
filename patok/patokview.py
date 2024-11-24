from .serializers import ProductionLineSerializer
from .models import ProductionLine
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

class ProductionLineViewSet(APIView):
    serializer_class = ProductionLineSerializer
    def post(self, request):
        print(request.data)
        serializer = ProductionLineSerializer(data=request.data)

        if serializer.is_valid():
            print(serializer.validated_data)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def get(self, request):
        production_lines = ProductionLine.objects.all()
        serializer = self.serializer_class(production_lines, many=True)
        return Response(serializer.data)
    
    

class ProductionLineDetail(APIView):
    serializer_class = ProductionLineSerializer

    def get_object(self, pk):
        print(11111111111111111111111111111111111)
        try:
            return ProductionLine.objects.get(pk=pk)
        except ProductionLine.DoesNotExist:
            return Response({'detail': 'Bunday id lik production line topilmadi'}, status=status.HTTP_404_NOT_FOUND)
    
    def get(self, request, pk):
        production_line = self.get_object(pk)
        data = {
            'id':pk,
            'name': production_line.name,
            'worker_time_per_day': production_line.worker_time_per_day,
            'created_at': production_line.created_at,
            'updated_at': production_line.updated_at
        }
        return Response(data)
    
    def put(self, request, pk):
        production_line = self.get_object(pk)
        serializer = self.serializer_class(production_line, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        production_line = self.get_object(pk)
        production_line.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def patch(self, request, pk):
        production_line = self.get_object(pk)
        serializer = self.serializer_class(production_line, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)