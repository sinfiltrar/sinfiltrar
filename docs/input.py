import json
import boto3

from django.conf import settings

from docs.models import Doc


def process_s3_input(event):
	snsData = json.loads(event['Records'][0]['Sns']['Message'])
	doc = Doc.from_s3(snsData['receipt']['action']['objectKey'])
	doc.save()


def process_existing_s3():
	s3 = boto3.resource('s3', )
	bucket = s3.Bucket(settings.AWS_S3_BUCKET_NAME_INPUT)

	print('Connected to bucket')

	count = sum(1 for _ in bucket.objects.all())
	print(f'About to process {count} emails')

	i = 0
	for object in bucket.objects.all():
		i += 1
		print(f'Processing email ({i}/{count}) {object.key}',)
		doc = Doc.from_s3(object.key)
		doc.save()
