from rest_framework import viewsets
from docs.models import Doc
from docs.serializers import DocSerializer


class DocViewSet(viewsets.ReadOnlyModelViewSet):
	lookup_field = 'slug'
	queryset = Doc.objects.order_by('-issued_at')
	serializer_class = DocSerializer
	permission_classes = []

	def get_queryset(self):
		queryset = self.queryset
		issuer_slug = self.request.query_params.get('issuer')
		if (issuer_slug is not None):
			queryset = queryset.filter(issuer__slug=issuer_slug)
		return queryset;
