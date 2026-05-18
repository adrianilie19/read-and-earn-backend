from django.contrib import admin
from Premios.models import Premio, Canje

@admin.register(Premio)
class PremioAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'autor', 'coste_exp', 'stock', 'is_active')
    list_filter = ('is_active',)

@admin.register(Canje)
class CanjeAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'premio', 'exp_gastada', 'fecha')
    list_filter = ('premio',)
