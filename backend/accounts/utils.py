import random
from django.core.mail import send_mail


def generated_otp(): 
    return str(random.randint(10000, 99999))

def send_otp_mail(instance):
    otp = generated_otp()
    instance.otp = otp
    instance.save()
    message = f"""
            Hi {instance.username}
            Thank you for registering with E-Learning 🎉

            To complete your sign-up, please use the One-Time Password (OTP) below:

            🔐 Your OTP: {instance.otp}

            Please don’t share it with anyone for your account’s safety.

            If you didn’t request this, you can safely ignore this email.

            Thanks for choosing E-Learning — we’re excited to have you on board! 😊

            Best regards,  
            The E-Learning Team
        """
    send_mail(
        subject='OTP for E-learning Registration',
        message=message,
        from_email='thwahirxpv@gmail.com',
        recipient_list=[instance.email],
        fail_silently=False
    )
    return