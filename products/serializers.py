from rest_framework import serializers
from .models import Product, Category
from accounts.models import CustomUser

# 작성자 정보에서 username만 직렬화하는 Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username']  # username만 반환되도록 설정

# 카테고리 Serializer
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']  # 카테고리 ID와 이름 반환

# Product 모델에 대한 Serializer
class ProductSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)  # 작성자 정보를 username으로 직렬화
    categories = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), many=True, write_only=True)
    category_details = CategorySerializer(many=True, read_only=True, source='categories')

    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'image', 'created_at', 'created_by', 'categories', 'category_details']  # 필요한 필드 설정
        read_only_fields = ['id', 'created_at', 'created_by']  # 읽기 전용 필드 (자동 생성됨)

    def create(self, validated_data):
        categories_data = validated_data.pop('categories', [])  # categories 필드를 따로 처리
        product = Product.objects.create(**validated_data)  # created_by는 views.py에서 처리
        product.categories.set(categories_data)  # 카테고리 연결 (ManyToMany 필드)
        return product


