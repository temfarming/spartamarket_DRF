# from django.shortcuts import render
# from django.http import JsonResponse, HttpResponse
# from django.core import serializers
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from rest_framework import status
# from django.shortcuts import get_object_or_404
# from rest_framework.views import APIView
# from .models import Product
# from .serializers import ProductSerializer

    
# class ProductListAPIView(APIView):
#     def get(self, request):
#         products = Product.objects.all()
#         serializer = ProductSerializer(products, many=True)
#         return Response(serializer.data)
    
#     def post(self, request):
#         serializer = ProductSerializer(data=request.data)
#         if serializer.is_valid(raise_exception=True):
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)

# class ProductDetailAPIView(APIView):

#     def get_object(self, pk):
#         return get_object_or_404(Product, pk=pk)
    
#     def get(self, request, pk):
#         product = self.get_object(pk)
#         serializer = ProductSerializer(product)
#         return Response(serializer.data)
    
#     def put(self, request, pk):
#         product = self.get_object(pk)
#         serializer = ProductSerializer(product, data=request.data, partial=True)
#         if serializer.is_valid(raise_exception=True):
#             serializer.save()
#             return Response(serializer.data)
        
#     def delete(self, request, pk):
#         product = self.get_object(pk)
#         product.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
    
from rest_framework import generics, permissions, serializers  
from .models import Product
from .serializers import ProductSerializer

# 상품 목록 조회 및 상품 등록 View
class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]  # 비로그인 사용자는 조회만 가능, 등록은 로그인 필요

    def perform_create(self, serializer):
        # 상품을 등록할 때 현재 로그인한 사용자를 작성자로 설정
        serializer.save(created_by=self.request.user)

# 상품 상세 조회, 수정, 삭제 View
class ProductDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]  # 비로그인 사용자는 조회만 가능, 수정/삭제는 작성자만 가능

    def perform_update(self, serializer):
        # 상품 수정 시 작성자만 수정할 수 있도록 검증
        product = self.get_object()
        if self.request.user != product.created_by:
            raise serializers.ValidationError({"error": "You do not have permission to update this product."})
        serializer.save()

    def perform_destroy(self, instance):
        # 상품 삭제 시 작성자만 삭제할 수 있도록 검증
        if self.request.user != instance.created_by:
            raise serializers.ValidationError({"error": "You do not have permission to delete this product."})
        instance.delete()
