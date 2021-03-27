from docs.models import Doc
from django.http import HttpResponse
import json


def latest(request):
	docs = Doc.objects.order_by('-issued_at')[:10]
	response = [{
		"title": doc.title,
		"slug": doc.slug,
		"issued_at": doc.issued_at.__str__(),
	} for doc in docs]
	return HttpResponse(json.dumps(response), content_type="application/json");


def one(request, slug):
	doc = Doc.objects.get(slug=slug)
	return HttpResponse(json.dumps({
		"title": doc.title,
		"slug": doc.slug,
		"short_text": doc.short_text,
		"content": doc.body_plain,
		"date": doc.issued_at.__str__(),
		"media": doc.media,
	}), content_type="application/json")
