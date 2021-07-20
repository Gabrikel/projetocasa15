from django.contrib import admin


from .models import UserBase

@admin.register(UserBase)
class UserAdmin(admin.ModelAdmin):
    list_display = ['email']


