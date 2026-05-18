from rest_framework import serializers
from Premios.models import Premio


class PremioSerializer(serializers.ModelSerializer):
    disponible = serializers.SerializerMethodField()

    class Meta:
        model = Premio
        fields = ('id', 'titulo', 'autor', 'coste_exp', 'stock', 'portada_url', 'disponible')

    def get_disponible(self, obj):
        return obj.stock > 0 and obj.is_active
