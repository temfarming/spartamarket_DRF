 
from rest_framework import generics, permissions, serializers, status, views
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from .models import Product, Category, Tag
from .serializers import ProductSerializer, CategorySerializer, TagSerializer
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404


# 카테고리 목록 조회 및 등록 (관리자만 생성 가능)
class CategoryListCreateAPIView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAdminUser]  # 관리자만 생성 가능

# 상품 목록 조회 및 상품 등록 View
class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]  # 비로그인 사용자는 조회만 가능, 등록은 로그인 필요
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['title', 'description', 'created_by__username']  # 제목, 설명, 작성자명으로 필터링 가능
    pagination_class = PageNumberPagination

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


# 상품 좋아요 추가/제거 View
class ProductLikeView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        if product.likes.filter(id=request.user.id).exists():
            return Response({"detail": "Already liked this product."}, status=status.HTTP_400_BAD_REQUEST)
        
        product.likes.add(request.user)
        return Response({"detail": "Product liked."}, status=status.HTTP_200_OK)

    def delete(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        if not product.likes.filter(id=request.user.id).exists():
            return Response({"detail": "You haven't liked this product."}, status=status.HTTP_400_BAD_REQUEST)
        
        product.likes.remove(request.user)
        return Response({"detail": "Product unliked."}, status=status.HTTP_200_OK)

# 태그 생성 View
class TagCreateView(generics.CreateAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        tag_name = self.request.data.get("name")
        if tag_name:
            tag_name = tag_name.lower()  # 대소문자 구분 없이 태그 저장
        serializer.save(name=tag_name)