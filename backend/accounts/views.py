from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer, LoginSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from google.oauth2 import id_token
from google.auth.transport import requests
from django.contrib.auth import get_user_model
from .models import CustomUser
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .utils import send_otp_mail

class RegisterView(APIView):
    def post(self, req):
        serializer = RegisterSerializer(data=req.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Successfully registered'
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, req):
        serializer = LoginSerializer(data=req.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)

            response = Response({
                'message': 'Login successful',
                'username': user.username,
                'role': user.role
            }, status=status.HTTP_200_OK)

            response.set_cookie(
                key='access', 
                value=str(refresh.access_token),
                httponly=True,
                samesite='Lax',
                secure=True
            )
            response.set_cookie(
                key='refresh',
                value=str(refresh),
                httponly=True,
                samesite='Lax',
                secure=True
            )
            return response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@method_decorator(csrf_exempt, name='dispatch')
class GoogleAuthenticationView(APIView):
    
    def post(self, req):
        token = req.data.get('token')

        if not token: 
            return Response({"message": "No token provided"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            info = id_token.verify_oauth2_token(token, requests.Request())

            email = info['email']
            username = info.get('username') or email.split("@")[0]
            
            user, created = CustomUser.objects.get_or_create(email=email, defaults={
                "email": email,
                "username": username
            })

            if created: 
                user.set_unusable_password()
                user.save()
            
            refresh = RefreshToken.for_user(user)
            response = Response({
                'message': 'Login successful',
                'username': user.username,
                'role': user.role 
            }, status=status.HTTP_200_OK)

            response.set_cookie(
                key='access', 
                value=str(refresh.access_token),
                httponly=True,
                samesite='Lax',
                secure=True
            )
            response.set_cookie(
                key='refresh', 
                value=str(refresh),
                httponly=True,
                samesite='Lax',
                secure=True
            )
            return response
        except ValueError as e:
            return Response({"message": "Invalid google token"}, status=status.HTTP_400_BAD_REQUEST)
        

class ResendOTPView(APIView):
    
    def post(slef, req):
        email = req.data.get('email')
        try:
            user = CustomUser.objects.get(email=email)
            send_otp_mail(user)
            return Response({'message': 'OTP resent successfully'}, status=status.HTTP_200_OK)
        except:
            return Response({'message': 'User not found!'}, status=status.HTTP_404_NOT_FOUND)
        

class OTPVerifyView(APIView):

    def post(self, req):
        email = req.data.get('email')
        otp = req.data.get('otp')

        try:
            user = CustomUser.objects.get(email=email)
            if user.otp == otp:
                user.is_verified = True
                user.otp = ''
                user.save()
                return Response({'message': 'OTP verified successfully'}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


# Override default TokenRefreshView for fetch refresh token from cookie
class CookieTokenRefreshView(TokenRefreshView):
    def post(self, req, *args, **kwargs):
        refresh_token = req.COOKIES.get('refresh')
        if refresh_token is None: 
            return Response({'error': 'Refresh token missing'}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = self.get_serializer(data={'refresh': refresh_token})

        try: 
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])
        
        response = Response({'message': 'Token refreshed'}, status=status.HTTP_200_OK)
        try:
            access_token = serializer.validated_data['access']
        except Exception as e: 
            raise Exception(e.args[0])
        response.set_cookie(
            key='access',
            value=str(access_token),
            httponly=True,
            samesite='Lax',
            secure=True
        )
        return response




