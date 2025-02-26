from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

# Registrar o modelo CustomUser
admin.site.register(CustomUser, UserAdmin)