from rest_framework import serializers
from .models import Product, Category, Tag
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
    total_likes = serializers.IntegerField( read_only=True)
    tags = serializers.SlugRelatedField(
        many=True,
        slug_field='name',
        queryset=Tag.objects.all(),
        required=False
    )  

    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'image', 'created_at', 'created_by', 'categories', 'category_details', 'tags','total_likes']  # 필요한 필드 설정
        read_only_fields = ['id', 'created_at', 'created_by']  # 읽기 전용 필드 (자동 생성됨)

    def create(self, validated_data):
        categories_data = validated_data.pop('categories', [])  # categories 필드를 따로 처리
        tags_data = validated_data.pop('tags', [])  # 태그 데이터를 분리
        product = Product.objects.create(**validated_data)  # created_by는 views.py에서 처리
        product.categories.set(categories_data)  # 카테고리 연결 (ManyToMany 필드)

        # 태그 생성 또는 기존 태그 사용
        for tag_name in tags_data:
            tag, created = Tag.objects.get_or_create(name=tag_name)  # 태그가 없으면 생성
            product.tags.add(tag)

        return product
    

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']

    def validate_name(self, value):
        return value.lower()  # 태그 이름을 소문자로 변환

