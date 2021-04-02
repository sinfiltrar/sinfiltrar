from docs.models import Doc
from rest_framework import serializers
from issuers.serializers import IssuerSerializer


class DocSerializer(serializers.ModelSerializer):
    issuer = IssuerSerializer()

    class Meta:
        model = Doc
        fields = ['id', 'title', 'slug', 'body_plain', 'issued_at', 'issuer']
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }

