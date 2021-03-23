from docs.models import Doc
from django.http import HttpResponse
import json


def latest(request):

	docs = Doc.objects.all()

	response = [{
		"title": doc.title,
		"slug": doc.slug,
		# "issued_at": doc.issued_at,
	} for doc in docs]

	return HttpResponse(json.dumps(response), content_type="application/json");
