import random
from django.core.mail import send_mail
from rest_framework_simplejwt.authentication import JWTAuthentication   
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

jwt_auth = JWTAuthentication()

def generated_otp(): 
    return str(random.randint(1000, 9999))

def send_otp_mail(instance):
    otp = generated_otp()
    instance.otp = otp
    instance.save()
    # message = f"""
    #         Hi {instance.username}
    #         Thank you for registering with E-Learning.

    #         To complete your sign-up, please use the One-Time Password (OTP) below:

    #         Your OTP: {instance.otp}

    #         Please don’t share it with anyone for your account’s safety.

    #         If you didn’t request this, you can safely ignore this email.

    #         Thanks for choosing E-Learning — we’re excited to have you on board!

    #         Best regards,  
    #         The E-Learning Team
    #     """

    message = f'Your OTP: {instance.otp}'
    
    print(instance.email)
    send_mail(
        subject='OTP for E-learning Registration',
        message=message,
        from_email='thwahirpvmohd@gmail.com',
        recipient_list=[instance.email],
        fail_silently=False
    )

    return


def validate_access_token(access_token):
    validate_token = jwt_auth.get_validated_token(access_token)
    user = jwt_auth.get_user(validate_token)
    return user

def refresh_access_token(refresh_token):
    refresh_token_obj = RefreshToken(refresh_token)
    refreshed_access = str(refresh_token_obj.access_token)

    validate_token = jwt_auth.get_validated_token(refreshed_access)
    user = jwt_auth.get_user(validate_token)
    return user, refreshed_access
