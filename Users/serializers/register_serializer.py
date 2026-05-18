from rest_framework import serializers
from Users.models import CustomUser


class RegisterSerializer(serializers.ModelSerializer):
    nombre = serializers.CharField(required=True, allow_blank=False, max_length=50)
    email = serializers.EmailField(required=True, allow_blank=False, max_length=100)
    password1 = serializers.CharField(required=True, allow_blank=False, min_length=6)
    password2 = serializers.CharField(required=True, allow_blank=False, min_length=6)

    class Meta:
        model = CustomUser
        fields = ('nombre', 'email', 'password1', 'password2')

    def validate_email(self, email):
        if CustomUser.objects.filter(email=email).exists():
            raise serializers.ValidationError("Ya existe una cuenta con ese email.")
        return email

    def validate_password1(self, password):
        if not any(c.isdigit() for c in password):
            raise serializers.ValidationError("La contraseña debe tener al menos un número.")
        return password

    def validate(self, attrs):
        if attrs['password1'] != attrs['password2']:
            raise serializers.ValidationError("Las contraseñas no coinciden.")
        return attrs

    def create(self, validated_data):
        password = validated_data.pop('password1')
        validated_data.pop('password2')
        user = CustomUser.objects.create(
            email=validated_data['email'],
            nombre=validated_data['nombre'],
        )
        user.set_password(password)
        user.save()
        return user
