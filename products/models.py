from django.db import models
from accounts.models import CustomUser 

# 카테고리 모델
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)  # 카테고리명은 유일해야 함

    def __str__(self):
        return self.name
    
# 상품 모델
class Product(models.Model):
    title = models.CharField(max_length=200)        # 상품 제목
    description = models.TextField()                # 상품 설명 (기존 content -> description으로 이름 변경)
    image = models.ImageField(upload_to='product_images/', null=True, blank=True)   # 상품 이미지 (필수는 아니며, 선택적 필드로 설정)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)    # 상품 작성자 (외래 키로 설정, CustomUser 모델 참조)
    created_at = models.DateTimeField(auto_now_add=True)                    # 생성 날짜
    updated_at = models.DateTimeField(auto_now=True)                        # 수정 날짜
    categories = models.ManyToManyField(Category)                           # 상품과 카테고리 간의 다대다 관계

    def __str__(self):
        return self.title


