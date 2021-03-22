from django.shortcuts import render
from django.http import HttpResponse
from issuers.models import Issuer
import json

def index(request): 

    issuers = Issuer.objects.all();

    response = [{
        "name": issuer.name,
        "slug": issuer.slug,
    } for issuer in issuers]

    return HttpResponse(json.dumps(response), content_type="application/json");
