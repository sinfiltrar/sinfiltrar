from django.core.management.base import BaseCommand, CommandError
from docs.models import Doc
import boto3
import json

AWS_INPUT_BUCKET_NAME = 'sinfiltrar-input'
# bucket_name = 'sinfiltrar-attachments'
# bucket_location = 'https://sinfiltrar-attachments.s3-us-west-2.amazonaws.com'

s3 = boto3.resource('s3')

class Command(BaseCommand):
	help = 'Parses emails from the s3 bucket.'


	def handle(self, *args, **options):

		self.stdout.write('Fetching object list from {} bucket'.format(AWS_INPUT_BUCKET_NAME));
		bucket = s3.Bucket(AWS_INPUT_BUCKET_NAME)
		object_count = sum(1 for _ in bucket.objects.all())
		self.stdout.write('Got {} objects from {} bucket'.format(object_count, AWS_INPUT_BUCKET_NAME));

		for i, obj in enumerate(bucket.objects.all()):
			self.stdout.write('{}/{} downloading object {}'.format(i+1, object_count, obj.key))
			file = self.download(AWS_INPUT_BUCKET_NAME, obj.key);
			mailBody = file.get()['Body'].read().decode('utf-8')
			doc = Doc.from_string(mailBody, obj.key)
			doc.save()

	def download(self, bucket, key):
		# metadata = s3.head_object(Bucket=bucket, key)
		file = s3.Object(bucket, key)
		return file