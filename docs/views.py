from django.contrib.postgres.search import SearchVector
from django.shortcuts import render

from rest_framework import viewsets

from docs.serializers import DocSerializer
from docs.models import Doc


def index(request):
    context = {
        'latest_docs': Doc.objects.filter(issuer__isnull=False).order_by('-issued_at')[:20]
    }
    return render(request, 'docs/index.html', context)


def one(request, slug):
    doc = Doc.objects.get(slug=slug)
    context = {'doc': doc}
    return render(request, 'docs/one.html', context)


class ApiDocViewSet(viewsets.ReadOnlyModelViewSet):
    lookup_field = 'slug'
    queryset = Doc.objects.order_by('-issued_at')
    serializer_class = DocSerializer
    permission_classes = []

    def get_queryset(self):
        queryset = self.queryset
        issuer_slug = self.request.query_params.get('issuer')
        if issuer_slug is not None:
            queryset = queryset.filter(issuer__slug=issuer_slug)
        else:
            queryset = queryset.filter(issuer__isnull=False)

        q = self.request.query_params.get('q')
        if q is not None:
            queryset = queryset.annotate(search=SearchVector('title', 'body_plain')).filter(search=q)

        return queryset
