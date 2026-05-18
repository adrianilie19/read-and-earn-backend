from rest_framework import serializers
from Logros.models import Logro


class LogroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Logro
        fields = ('id', 'titulo', 'descripcion', 'exp', 'icono')
