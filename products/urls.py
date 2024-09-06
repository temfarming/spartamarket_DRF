from django.urls import path
from .views import ProductListCreateAPIView, ProductDetailAPIView, CategoryListCreateAPIView

# 상품 관련 URL 패턴 설정
urlpatterns = [
    # 상품 목록 조회 및 등록 (GET: 조회, POST: 등록)
    path('', ProductListCreateAPIView.as_view(), name='product-list-create'),
    
    # 상품 상세 조회, 수정, 삭제 (GET: 조회, PUT: 수정, DELETE: 삭제)
    path('<int:pk>/', ProductDetailAPIView.as_view(), name='product-detail'),

    # 카테고리 목록 조회 및 등록 (관리자만 가능)
    path('categories/', CategoryListCreateAPIView.as_view(), name='category-list-create'),
]

