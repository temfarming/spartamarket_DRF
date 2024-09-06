
from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator

class SignupSerializer(serializers.ModelSerializer):
    # 이메일 필드: 필수 입력이며, 이메일이 유일한지 확인하는 유효성 검사 추가
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=CustomUser.objects.all())]  # 이메일 유일성 검증
    )
    
    # 비밀번호 필드: 쓰기 전용이며, 비밀번호 규칙 유효성 검사와 마스킹 처리 추가
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        style={'input_type': 'password'}  # HTML 폼에서 비밀번호를 마스킹 처리
    )
    
    # 비밀번호 확인 필드: 쓰기 전용이며, 비밀번호와 동일한 값이 입력되어야 함
    password2 = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    # 추가 필드: 이름, 닉네임, 생일은 필수 입력
    first_name = serializers.CharField(required=True)
    nickname = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=CustomUser.objects.all())]  # 닉네임 유일성 검증
    )
    birth_date = serializers.DateField(required=True)

    # 선택 필드: 성별과 자기소개는 선택 사항
    gender = serializers.CharField(required=False, allow_blank=True)
    bio = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = CustomUser
        # 필수 및 선택 필드를 모두 포함
        fields = ['username', 'email', 'password', 'password2', 'first_name', 'nickname', 'birth_date', 'gender', 'bio']

    # 비밀번호와 비밀번호 확인 필드가 일치하는지 추가 유효성 검사
    def validate(self, attrs):
        # 만약 'password'와 'password2'가 일치하지 않으면 오류 발생
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "비밀번호가 일치하지 않습니다."})
        return attrs  # 문제가 없으면 데이터를 그대로 반환

    # 유효성 검사가 완료된 데이터를 바탕으로 실제로 User 객체를 생성하는 메서드
    def create(self, validated_data):
        # username과 email을 이용해 User 객체 생성
        user = CustomUser(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name']  # 이름 저장
        )
        # 비밀번호는 해싱하여 저장 (보안을 위해 평문이 아닌 해시된 값으로 저장)
        user.set_password(validated_data['password'])
        
        user.nickname = validated_data.get('nickname')  # nickname 저장
        user.birth_date = validated_data.get('birth_date')  # birth_date 저장
        user.gender = validated_data.get('gender', '')  # gender 저장
        user.bio = validated_data.get('bio', '')  # bio 저장
        
        # 사용자 프로필 관련 추가 정보 저장
        # user.profile.nickname = validated_data['nickname']
        # user.profile.birth_date = validated_data['birth_date']
        # user.profile.gender = validated_data.get('gender', '')  # 선택 필드는 없을 수 있음
        # user.profile.bio = validated_data.get('bio', '')        # 선택 필드는 없을 수 있음
        
        # 데이터베이스에 사용자 정보 저장
        user.save()
        return user  # 새로 생성된 User 객체를 반환
    
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [ 'email', 'first_name', 'nickname', 'birth_date', 'gender', 'bio']
        read_only_fields = ['username']  # username 필드를 읽기 전용으로 설정