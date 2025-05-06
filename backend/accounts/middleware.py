from django.utils.deprecation import MiddlewareMixin
from rest_framework.response import Response
from django.contrib.auth.models import AnonymousUser
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from .utils import validate_access_token, refresh_access_token


class JWTMiddleware(MiddlewareMixin):
    def process_request(self, req):
        access = req.COOKIES.get('access')
        refresh = req.COOKIES.get('refresh')

        if access: 
            try: 
                user = validate_access_token(access)
                req.user = user
                return
            except AuthenticationFailed: 
                pass
        
        if refresh: 
            try: 
                user, refreshed_access = refresh_access_token(refresh)
                req.user = user
                req.refreshed_access_token = refreshed_access
                return 
            except AuthenticationFailed:
                Response({'message': "Authentication credentials Invalid."}, status=status.HTTP_401_UNAUTHORIZED) 
        
        req.user = AnonymousUser()


    def process_response(self, req, res): 
        if hasattr(req, 'refreshed_access_token'):
            res.set_cookie(
                key='access', 
                value=req.refreshed_access_token,
                httponly=True,
                samesite='Lax',
                secure=True
            )
        return res


                 
