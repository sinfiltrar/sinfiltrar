from sinfiltrar.settings import AWS_S3_BUCKET_NAME_INPUT
from django.core.management.base import BaseCommand, CommandError
from docs.models import Doc
import boto3
import json

s3 = boto3.resource('s3');

class Command(BaseCommand):
	help = 'Parses emails from the s3 bucket.'

	def handle(self, *args, **options):

		self.stdout.write('Fetching object list from {} bucket'.format(AWS_S3_BUCKET_NAME_INPUT));
		bucket = s3.Bucket(AWS_S3_BUCKET_NAME_INPUT)
		object_count = sum(1 for _ in bucket.objects.all())
		self.stdout.write('Got {} objects from {} bucket'.format(object_count, AWS_S3_BUCKET_NAME_INPUT));

		for i, obj in enumerate(bucket.objects.all()):
			self.stdout.write('{}/{} downloading object {}'.format(i+1, object_count, obj.key))
			file = self.download(AWS_S3_BUCKET_NAME_INPUT, obj.key)
			mail_body = file.get()['Body'].read().decode('utf-8')
			doc = Doc.from_string(mail_body, obj.key)
			self.stdout.write('Processed doc {}'.format(doc.title))
			doc.save()

	def download(self, bucket, key):
		file = s3.Object(bucket, key)
		return file
