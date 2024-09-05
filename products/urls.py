from django.urls import path
from .views import ProductListCreateAPIView, ProductDetailAPIView

# 상품 관련 URL 패턴 설정
urlpatterns = [
    # 상품 목록 조회 및 등록 (GET: 조회, POST: 등록)
    path('products/', ProductListCreateAPIView.as_view(), name='product-list-create'),
    
    # 상품 상세 조회, 수정, 삭제 (GET: 조회, PUT: 수정, DELETE: 삭제)
    path('products/<int:pk>/', ProductDetailAPIView.as_view(), name='product-detail'),
]

