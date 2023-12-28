from django.contrib import admin
from .models import Application

admin.register(Application, admin.ModelAdmin)
