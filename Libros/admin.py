from django.contrib import admin
from Libros.models import Biblioteca

@admin.register(Biblioteca)
class BibliotecaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'autor', 'usuario', 'progreso', 'estado', 'fecha_agregado')
    search_fields = ('titulo', 'autor', 'usuario__nombre')
    list_filter = ('estado',)
