
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status, views
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import CustomUser
from .serializers import SignupSerializer, CustomUserSerializer


# 로그인  (JWT 토큰 발급)
class CustomTokenObtainPairView(TokenObtainPairView):
    pass

# 로그아웃 View
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