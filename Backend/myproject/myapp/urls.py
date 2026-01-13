from django.urls import path
from .views import RegisterView , RoleView , OrganizationView , DashboardView , ResetPasswordAPIView
# from .views import LoginApi , LogoutView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    path('resetpwd/', ResetPasswordAPIView.as_view(), name='resetpwd'),
    path('register/', RegisterView.as_view(), name='register'),
    path('role/', RoleView.as_view(), name='role'),
    path('organizations/', OrganizationView.as_view(), name='organizations'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'), 
]
