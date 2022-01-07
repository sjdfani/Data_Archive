from django.contrib import admin
from .models import UserInfo


@admin.register(UserInfo)
class UserInfo(admin.ModelAdmin):
    list_display = ('username', 'fullname', 'email', 'type')
    list_filter = ('type',)
