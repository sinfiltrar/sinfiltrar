from django.shortcuts import render

from docs.models import Doc
from issuers.models import Issuer


def home(request):
	context = {
		'latest_docs': Doc.objects.order_by('-issued_at')[:10],
		'issuers': Issuer.objects.order_by('name').all()
	}
	return render(request, 'home.html', context)