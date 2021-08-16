import json
from docs.models import Doc


def process_s3_input(event):
	snsData = json.loads(event['Records'][0]['Sns']['Message'])
	doc = Doc.from_s3(snsData['receipt']['action']['objectKey'])
	doc.save()


