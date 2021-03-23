from django.db import models


class Doc(models.Model):
	issuer = models.ForeignKey('issuers.Issuer', on_delete=models.CASCADE)
	issuer_name = models.CharField(max_length=200)
	from_email = models.ForeignKey('issuers.IssuerEmail', on_delete=models.DO_NOTHING)
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
