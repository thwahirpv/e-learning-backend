from django.urls import path
from .views import *

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('google/auth/', GoogleAuthenticationView.as_view, name='google_auth'),
    path('resend_otp/', ResendOTPView.as_view(), name='resend_otp'),
    path('verify_otp/', OTPVerifyView.as_view(), name='verify_otp'),
    path('api/token/refresh/', CookieTokenRefreshView.as_view(), name='token_refresh'),
]