from django.contrib import admin
from .models import Users, Code


@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    pass

@admin.register(Code)
class CodeAdmin(admin.ModelAdmin):
    pass