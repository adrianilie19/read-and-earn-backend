from django.contrib import admin
from Logros.models import Logro, LogroUsuario

@admin.register(Logro)
class LogroAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'exp', 'icono')

@admin.register(LogroUsuario)
class LogroUsuarioAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'logro', 'fecha')
    list_filter = ('logro',)
