from django.db import models
from django.contrib.auth.models import AbstractUser
from constants.accounts import ROLE_CHOICE, ROLE_ADMIN, ROLE_TUTOR, ROLE_STUDENT
from phonenumber_field.modelfields import PhoneNumberField
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number = PhoneNumberField(region=None, blank=True, null=True)
    country_code = models.CharField(max_length=5, blank=True, null=True)
    role = models.CharField(max_length=15, choices=ROLE_CHOICE, default='student')
    is_verified = models.BooleanField(default=False)
    otp = models.CharField(max_length=6, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'country_code', 'phone_number', 'password']

    def __str__(self):
        return self.username
    
    @property
    def is_admin(self):
        return self.role == ROLE_ADMIN

    @property
    def is_tutor(self):
        return self.role == ROLE_TUTOR
    
    @property
    def is_student(self):
        return self.role == ROLE_STUDENT
    
    
