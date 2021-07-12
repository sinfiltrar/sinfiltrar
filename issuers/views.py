from django.shortcuts import render

from rest_framework import viewsets

from issuers.serializers import IssuerSerializer
from issuers.models import Issuer

from docs.models import Doc


def index(request):
	context = {
		'issuers': Issuer.objects.order_by('name')
	}
	return render(request, 'issuers/index.html', context)


def one(request, slug):
	issuer = Issuer.objects.get(slug=slug)
	context = {
		'issuer': issuer,
		'issuer_docs': Doc.objects.filter(issuer=issuer).all()
	}
	return render(request, 'issuers/one.html', context)


class ApiIssuerViewSet(viewsets.ReadOnlyModelViewSet):
	lookup_field = 'slug'
	queryset = Issuer.objects.order_by('slug')
	serializer_class = IssuerSerializer
	permission_classes = []