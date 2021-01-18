from django.db import models

class Register(models.Model):
    username=models.CharField(max_length=120)
    email=password=models.CharField(max_length=40)
    password=models.CharField(max_length=40)
    repassword=models.CharField(max_length=40)

    def __str__(self):
        return self.username
