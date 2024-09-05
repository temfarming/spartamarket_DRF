from rest_framework import serializers
from .models import Product
from accounts.models import CustomUser

# 작성자 정보에서 username만 직렬화하는 Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username']  # username만 반환되도록 설정

# Product 모델에 대한 Serializer
class ProductSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)  # 작성자 정보를 username으로 직렬화

    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'image', 'created_at', 'created_by']  # 필요한 필드 설정
        read_only_fields = ['id', 'created_at', 'created_by']  # 읽기 전용 필드 (자동 생성됨)

    def create(self, validated_data):
        # 상품 등록 시, 요청을 보낸 사용자를 작성자로 설정
        user = self.context['request'].user
        product = Product.objects.create(created_by=user, **validated_data)
        return product

    def update(self, instance, validated_data):
        # 상품 수정 시 기존 데이터를 유지하고 필요한 부분만 업데이트
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.image = validated_data.get('image', instance.image)
        instance.save()
        return instance
