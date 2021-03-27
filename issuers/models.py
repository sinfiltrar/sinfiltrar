from django.db import models

class Issuer(models.Model):
    slug = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class IssuerEmail(models.Model):
    email = models.CharField(max_length=254)
    issuer = models.ForeignKey('Issuer', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
