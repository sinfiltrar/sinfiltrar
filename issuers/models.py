from django.db import models;

class Issuer(models.Model):
    slug = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    created_at = models.DateTimeField();


