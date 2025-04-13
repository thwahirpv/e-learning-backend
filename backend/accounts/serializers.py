from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth import authenticate

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'country_code', 'phone_number', 'role', 'password']
        extra_kwargs = {'password': {'write_only': True}}
    
    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)
    
    def validate(self, attrs):
        attrs = super().validate(attrs)

        # Custom calidation check for phone number and country code 
        country_code = str(attrs.get('country_code'))
        phone_number = str(attrs.get('phone_number'))
        if not phone_number.replace("+", "").startswith(country_code.replace("+", "")):
            raise serializers.ValidationError("phone number does not match the selected country code.")
        return attrs


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


    def validate(self, data):
        user = authenticate(email=data['email'], password=data['password'])
        if not user: 
            raise serializers.ValidationError("Invalid credentials")
        
        if not user.is_active: 
            raise serializers.ValidationError("Your account is inactive. Please contact support.")
        
        data['user'] = data
        return data
        


