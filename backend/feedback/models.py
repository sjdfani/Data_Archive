from django.db import models


class Feedback(models.Model):
    username = models.CharField(max_length=50)
    title = models.CharField(max_length=50)
    subject = models.CharField(max_length=100)
    message = models.TextField()

    def __str__(self):
        return self.username
