from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer, LoginSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError


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




