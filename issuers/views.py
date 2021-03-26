from django.http import HttpResponse
from issuers.models import Issuer
from docs.models import Doc
import json


def index(request):
	issuers = Issuer.objects.all()
	response = [{
		"name": issuer.name,
		"slug": issuer.slug,
	} for issuer in issuers]
	return HttpResponse(json.dumps(response), content_type="application/json")


def one(request, slug):
	issuer = Issuer.objects.get(slug=slug)
	return HttpResponse(json.dumps({
		"name": issuer.name,
		"slug": issuer.slug,
	}), content_type="application/json")


def docs(request, slug):
	issuer = Issuer.objects.get(slug=slug)
	docs = Doc.objects.filter(issuer=issuer)
	return HttpResponse(json.dumps([{
		"title": doc.title,
		"slug": doc.slug,
		"short_text": doc.short_text,
		"content": doc.body_plain,
		"date": doc.issued_at.__str__(),
		"media": doc.media,
	} for doc in docs]), content_type="application/json")
