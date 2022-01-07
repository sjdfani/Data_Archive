from django.db import models


class Payment(models.Model):
    username = models.CharField(max_length=50)
    title = models.CharField(max_length=50)
    fullname = models.CharField(max_length=50)
    phone = models.CharField(max_length=11)
    company = models.CharField(max_length=50)
    price = models.CharField(max_length=50)
    date = models.CharField(max_length=11)
    time = models.CharField(max_length=14)
    state = models.CharField(max_length=10)
    is_pay = models.CharField(max_length=3)
    tracking_code = models.CharField(max_length=100)

    def __str__(self):
        return self.username
