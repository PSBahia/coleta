from rest_framework import serializers
from .models import DadosColetados
from django.contrib.auth.models import User

class DadosColetadosSerializer(serializers.ModelSerializer):
    class Meta:
        model = DadosColetados
        fields = '__all__'  # Inclui todos os campos do modelo no serializer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user