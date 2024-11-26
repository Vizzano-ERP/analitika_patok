from rest_framework import  status
from rest_framework.response import Response
from rest_framework import views
from .models import Product
from .serializers import ProductSerializer

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