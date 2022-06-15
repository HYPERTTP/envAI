from django.db import models

# Create your models here.


class Product(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField(default=10)
    scores = models.CharField(max_length=500)
