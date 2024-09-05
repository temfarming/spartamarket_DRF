from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import SignupView, ProfileUpdateView

urlpatterns = [
    # 로그인
    path("signin/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    # 토큰 갱신
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # 회원가입
    path("signup/", SignupView.as_view(), name="signup"),
    # 프로필 업데이트
    path("accounts/<str:username>/", ProfileUpdateView.as_view(), name="profile-update"),
]
