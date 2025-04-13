from django.db import models
from django.contrib.auth.models import AbstractUser
from constants.accounts import ROLE_CHOICE, ROLE_ADMIN, ROLE_TUTOR, ROLE_STUDENT

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15)
    role = models.CharField(max_length=15, choices=ROLE_CHOICE, default='student')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'

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
    
    
