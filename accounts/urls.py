from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import SignupView, ProfileUpdateView, ProfileView, LogoutView, ChangePasswordView, DeleteAccountView

urlpatterns = [
    # 로그인
    path("signin/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    # 로그아웃 
    path('logout/', LogoutView.as_view(), name='logout'),
    # 회원가입
    path("signup/", SignupView.as_view(), name="signup"),
    # 프로필 업데이트
    path("accounts/<str:username>/", ProfileUpdateView.as_view(), name="profile-update"),
    # 프로필 조회 
    path('<str:username>/', ProfileView.as_view(), name='profile'),
    # 패스워드 변경 
    path('password/', ChangePasswordView.as_view(), name='change-password'),
    # 회원 탈퇴 
    path('delete/', DeleteAccountView.as_view(), name='delete-account'),
    # 토큰 갱신
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]

