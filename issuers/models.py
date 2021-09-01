from django.db import models

class Issuer(models.Model):

    STATUS_CHOICES = (
        ('new', 'Nuevo'),
        ('waiting', 'Esperando primer doc'),
        ('active', 'Activo'),
        ('inactive', 'Inactivto'),
    )
    status = models.CharField(max_length=255, choices=STATUS_CHOICES)
    slug = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    info = models.TextField(blank=True, null=True)
    color = models.CharField(max_length=6, default='006EFF')
    avatar = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'({self.status}) {self.name}'


class IssuerEmail(models.Model):
    email = models.CharField(max_length=254)
    issuer = models.ForeignKey('Issuer', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
