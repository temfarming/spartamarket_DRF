
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status, views, serializers
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import CustomUser
from .serializers import SignupSerializer, CustomUserSerializer
from django.contrib.auth import update_session_auth_hash


# 로그인  (JWT 토큰 발급)
class CustomTokenObtainPairView(TokenObtainPairView):
    pass

# 로그아웃 
class LogoutView(views.APIView):
    permission_classes = [IsAuthenticated]  # 인증된 사용자만 가능

    def post(self, request):
        try:
            # 클라이언트에서 전달된 refresh 토큰을 무효화
            refresh_token = request.data.get("refresh")
            token = RefreshToken(refresh_token)
            token.blacklist()  # Refresh Token 무효화
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        
# 회원가입 
class SignupView(generics.CreateAPIView):
    serializer_class = SignupSerializer
    permission_classes = [AllowAny]  # 누구나 접근 가능 (회원가입)

# 프로필 조회 
class ProfileView(generics.RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = SignupSerializer
    permission_classes = [IsAuthenticated]  # 로그인한 사용자만 조회 가능
    lookup_field = 'username'  # URL에서 username을 통해 사용자 조회

    def get_queryset(self):
        # 로그인한 사용자만 자신의 프로필을 조회할 수 있도록 제한
        return CustomUser.objects.filter(username=self.request.user.username)

# 프로필 업데이트  (PUT 요청)
class ProfileUpdateView(generics.UpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer  # 같은 serializer 사용 가능 (필드들이 같기 때문에)
    permission_classes = [IsAuthenticated]  # 로그인한 사용자만 접근 가능
    lookup_field = 'username'  # URL에서 username을 기반으로 검색

    def get_queryset(self):
        # 로그인한 사용자만 자신의 프로필을 수정할 수 있도록 제한
        return CustomUser.objects.filter(username=self.request.user.username)
    
    # 패스워드 변경 View
class ChangePasswordView(views.APIView):
    permission_classes = [IsAuthenticated]

    class ChangePasswordSerializer(serializers.Serializer):
        old_password = serializers.CharField(required=True)
        new_password = serializers.CharField(required=True)

    def put(self, request, *args, **kwargs):
        user = request.user
        serializer = self.ChangePasswordSerializer(data=request.data)

        if serializer.is_valid():
            # 기존 비밀번호가 맞는지 확인
            if not user.check_password(serializer.data.get("old_password")):
                return Response({"old_password": "Wrong password."}, status=status.HTTP_400_BAD_REQUEST)

            # 새로운 비밀번호 설정
            user.set_password(serializer.data.get("new_password"))
            user.save()

            # 세션 유지
            update_session_auth_hash(request, user)

            return Response({"detail": "Password updated successfully."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# 회원 탈퇴 View
class DeleteAccountView(views.APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        user = request.user
        password = request.data.get("password")

        # 비밀번호가 맞는지 확인
        if not user.check_password(password):
            return Response({"password": "Wrong password."}, status=status.HTTP_400_BAD_REQUEST)

        user.delete()  # 계정 삭제
        return Response({"detail": "Account deleted successfully."}, status=status.HTTP_204_NO_CONTENT)