from rest_framework import viewsets
from issuers.serializers import IssuerSerializer
from issuers.models import Issuer


class IssuerViewSet(viewsets.ReadOnlyModelViewSet):
	lookup_field = 'slug'
	queryset = Issuer.objects.order_by('slug')
	serializer_class = IssuerSerializer
	permission_classes = []