from django.contrib import admin
from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("username", "title", "date", "time", "state", "is_pay")
    list_filter = ("username",)
