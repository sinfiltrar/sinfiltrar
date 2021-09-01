import json
import boto3

from django.conf import settings

from docs.models import Doc


def process_s3_input(event):
    snsData = json.loads(event['Records'][0]['Sns']['Message'])
    doc = Doc.from_s3(snsData['receipt']['action']['objectKey'])
    doc.save()


def process_existing_s3(dest='db'):
    s3 = boto3.resource('s3', )
    sns = boto3.client('sns')
    bucket = s3.Bucket(settings.AWS_S3_BUCKET_NAME_INPUT)

    print('Connected to bucket')

    count = sum(1 for _ in bucket.objects.all())
    print(f'About to process {count} emails')

    i = 0
    for object in bucket.objects.all():
        i += 1
        if dest == 'db':
            print(f'Processing element ({i}/{count}) {object.key}',)
            doc = Doc.from_s3(object.key)
            doc.save()
        elif dest == 'sns':
            print(f'Sending SNS for element ({i}/{count}) {object.key}',)
            sns.publish(
                TopicArn='arn:aws:sns:us-west-2:153920312805:sinfiltrar-input',
                Message=json.dumps({'receipt': {'action': {'bucketName': object.bucket_name, 'objectKey': object.key}}}),
            )
