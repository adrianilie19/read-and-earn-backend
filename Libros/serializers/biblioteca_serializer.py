from rest_framework import serializers
from Libros.models import Biblioteca


class BibliotecaSerializer(serializers.ModelSerializer):
    gutendex_id = serializers.IntegerField(required=True)
    titulo      = serializers.CharField(required=True, max_length=255)
    autor       = serializers.CharField(required=False, allow_blank=True, max_length=255)
    portada_url = serializers.URLField(required=False, allow_blank=True)

    class Meta:
        model = Biblioteca
        fields = ('id', 'gutendex_id', 'titulo', 'autor', 'portada_url', 'progreso', 'estado', 'fecha_agregado')
        read_only_fields = ('id', 'progreso', 'estado', 'fecha_agregado')

    def validate_progreso(self, progreso):
        if progreso < 0 or progreso > 100:
            raise serializers.ValidationError("El progreso debe estar entre 0 y 100.")
        return progreso
