from django.contrib import admin
from app import models

# Register your models here.
admin.register(models.User)
admin.register(models.Comment)
