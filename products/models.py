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
    likes = models.ManyToManyField(CustomUser, related_name='liked_products', blank=True)  # 좋아요 기능 (ManyToMany)

    def total_likes(self):
        """게시글의 좋아요 수를 반환"""
        return self.likes.count()
    
    def __str__(self):
        return self.title


# 상품 태그 모델
class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)  # 태그 이름 (유일한 값)

    def save(self, *args, **kwargs):
        """태그를 소문자로 저장하여 대소문자 구분 없이 처리"""
        self.name = self.name.lower()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name