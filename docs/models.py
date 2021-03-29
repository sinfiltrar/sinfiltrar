from django.core.exceptions import ObjectDoesNotExist
from sinfiltrar.settings import AWS_S3_BUCKET_NAME_INPUT_ATTACHMENTS, AWS_S3_DOMAIN_INPUT_ATTACHMENTS
from django.db import models
from issuers.models import Issuer, IssuerEmail
import mailparser
import boto3
import base64
import logging
import pytz

logger = logging.getLogger('main')


class Doc(models.Model):
	id = models.CharField(max_length=40, primary_key=True)
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

	def set_issuer_based_on_email(self):
		try:
			issuer_email = IssuerEmail.objects.filter(email=self.from_email).get()
			self.issuer_email = issuer_email
			self.issuer = self.issuer_email.issuer
		except ObjectDoesNotExist:
			pass


	@classmethod
	def from_string(cls, raw_email, key):

		mail = mailparser.parse_from_string(raw_email)

		data = {
			'id': key,
			'title': mail.subject,
			'from_email': mail.from_[0][1],
			'body_html': mail.text_html,
			'body_plain': mail.text_plain,
			'media': cls.process_media(key, mail),
			'meta': [],
			'issued_at': mail.date.replace(tzinfo=pytz.UTC),
		}

		return cls(**data)

	@classmethod
	def process_media(cls, key, mail):

		s3client = boto3.client('s3')

		media = []

		logger.info('Processing media for doc')

		for i, att in enumerate(mail.attachments):
			# Ensure unique objectKeys for attachments
			filename = '{}-{}-{}'.format(key, i, att['filename'])

			logger.info('processing {}'.format(filename))

			response = s3client.put_object(
				ACL='public-read',
				Body=base64.b64decode(att['payload']),
				Bucket=AWS_S3_BUCKET_NAME_INPUT_ATTACHMENTS,
				ContentType=att['mail_content_type'],
				Key=filename,
			)

			# location = s3client.get_bucket_location(Bucket=AWS_S3_BUCKET_NAME_INPUT_ATTACHMENTS)['LocationConstraint']
			url = "%s/%s" % (AWS_S3_DOMAIN_INPUT_ATTACHMENTS, filename)
			cid = att['content-id'].strip('<>')

			media.append({
				'type': att['mail_content_type'],
				'filename': att['filename'],
				'url': url,
				'cid': cid,
			})

		return media