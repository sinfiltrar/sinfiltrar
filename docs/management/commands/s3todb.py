from sinfiltrar.settings import AWS_S3_BUCKET_NAME_INPUT
from django.core.management.base import BaseCommand, CommandError
from docs.models import Doc
import boto3
import json

from docs.input import process_existing_s3

s3 = boto3.resource('s3');

class Command(BaseCommand):
	help = 'Parses emails from the s3 bucket.'

	def handle(self, *args, **options):
		process_existing_s3()