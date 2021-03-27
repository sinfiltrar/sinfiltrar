from django.db import models
from issuers.models import Issuer, IssuerEmail
import mailparser


class Doc(models.Model):
	id = models.CharField(max_length=40, primary_key=True)
	issuer_name = models.CharField(max_length=200)
	from_email = models.CharField(max_length=254)
	issuer = models.ForeignKey('issuers.Issuer', null=True, on_delete=models.CASCADE)
	issuer_email = models.ForeignKey('issuers.IssuerEmail', null=True, on_delete=models.DO_NOTHING)
	issued_at = models.DateTimeField()
	title = models.CharField(max_length=255)
	slug = models.CharField(max_length=255)
	short_text = models.CharField(max_length=255)
	body_html = models.TextField()
	body_plain = models.TextField()
	body_md = models.TextField()
	media = models.JSONField()
	meta = models.JSONField()
	created_at = models.DateTimeField(auto_now_add=True)


	@classmethod
	def from_string(cls, raw_email, key):

		mail = mailparser.parse_from_string(raw_email)

		data = {
			'id': key,
			'title': mail.subject,
			'from_email': mail._from,
			'body_html': mail.body,
			'body_plain': mail.body,
			'media': [],
			'meta': [],
			'issued_at': mail.date,
		}

		return cls(**data)
