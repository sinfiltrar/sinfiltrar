from django.core.management.base import BaseCommand
from docs.models import Doc


class Command(BaseCommand):
	help = 'Sets issuer to docs based on from_email'

	def handle(self, *args, **options):
		for doc in Doc.objects.all():
			doc.set_issuer_based_on_email()
			doc.save()
