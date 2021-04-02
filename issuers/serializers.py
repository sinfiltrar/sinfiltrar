from rest_framework import serializers
from issuers.models import Issuer, IssuerEmail


class IssuerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issuer
        fields = ['name', 'slug', ]


class IssuerEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = IssuerEmail
        fields = ['email', ]