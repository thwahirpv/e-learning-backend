from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer, LoginSerializer
from rest_framework_simplejwt.tokens import RefreshToken


class RegisterView(APIView):
    def post(self, req):
        serializer = RegisterSerializer(data=req.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Successfully registered'
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


