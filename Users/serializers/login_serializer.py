from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from Users.models import CustomUser


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, min_length=6)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        user = CustomUser.objects.filter(email=email).first()

        if not user:
            raise serializers.ValidationError("El usuario no existe.")
        if not user.check_password(password):
            raise serializers.ValidationError("La contraseña es incorrecta.")
        if not user.is_active:
            raise serializers.ValidationError("La cuenta está desactivada.")

        refresh = RefreshToken.for_user(user)
        refresh["nombre"] = user.nombre
        refresh["nivel"] = user.nivel

        return {
            "success": True,
            "data": {
                "nombre": user.nombre,
                "email": user.email,
                "nivel": user.nivel,
                "exp": user.exp,
                "refreshToken": str(refresh),
                "token": str(refresh.access_token),
            }
        }
