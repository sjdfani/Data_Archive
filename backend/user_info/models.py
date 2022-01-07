from django.db import models


class UserInfo(models.Model):
    fullname = models.CharField(max_length=50)
    username = models.CharField(max_length=50)
    email = models.EmailField()
    password = models.CharField(max_length=50)
    type = models.CharField(max_length=20)

    def __str__(self):
        return self.username
