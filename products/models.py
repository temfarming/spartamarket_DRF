from django.db import models
from accounts.models import CustomUser 

class Product(models.Model):
    # 상품 제목
    title = models.CharField(max_length=200)
    
    # 상품 설명 (기존 content -> description으로 이름 변경)
    description = models.TextField()
    
    # 상품 이미지 (필수는 아니며, 선택적 필드로 설정)
    image = models.ImageField(upload_to='product_images/', null=True, blank=True)
    
    # 상품 작성자 (외래 키로 설정, CustomUser 모델 참조)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    
    # 생성 날짜
    created_at = models.DateTimeField(auto_now_add=True)
    
    # 수정 날짜
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


