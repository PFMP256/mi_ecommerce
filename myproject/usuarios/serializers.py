# usuarios/serializers.py

from rest_framework import serializers
from .models import Usuario
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

class RegistroSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, min_length=8)
    email = serializers.EmailField(required=True)

    class Meta:
        model = Usuario
        fields = ['email', 'password']

    def validate_email(self, value):
        try:
            validate_email(value)
        except ValidationError:
            raise serializers.ValidationError("Correo electrónico no válido")
        if Usuario.objects.filter(email=value).exists():
            raise serializers.ValidationError("Este correo electrónico ya está registrado")
        return value

    def create(self, validated_data):
        usuario = Usuario.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password']
        )
        return usuario
