from rest_framework_simplejwt.authentication import JWTAuthentication

class CookieJWTAuthentication(JWTAuthentication):
    def get_raw_token(self, req):
        token = req.COOKIES.get('access')
        return token
