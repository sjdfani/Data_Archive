from rest_framework import serializers
from rest_framework.validators import ValidationError
from .models import UserInfo


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        fields = '__all__'

    @staticmethod
    def validate_username(value):
        is_exist_username = UserInfo.objects.filter(username=value).exists()
        if is_exist_username:
            raise ValidationError("username was taken.")
        return value
