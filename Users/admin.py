from django.contrib import admin
from Users.models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'email', 'nivel', 'exp', 'is_active')
    search_fields = ('nombre', 'email')
    list_filter = ('is_active',)
