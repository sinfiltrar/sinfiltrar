import mailparser
import boto3
import base64
import logging
import pytz
from markdownify import markdownify as md

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.urls import reverse
from django.utils.text import slugify

from issuers.models import IssuerEmail
from sinfiltrar.emails import mail_staff


logger = logging.getLogger('main')


class Doc(models.Model):
    id = models.CharField(max_length=40, primary_key=True)
    from_email = models.CharField(max_length=254, blank=True, null=True)
    issuer = models.ForeignKey('issuers.Issuer', null=True, on_delete=models.CASCADE)
    issuer_email = models.ForeignKey('issuers.IssuerEmail', null=True, on_delete=models.DO_NOTHING)
    issued_at = models.DateTimeField()
    title = models.CharField(max_length=255)
    slug = models.CharField(max_length=255)
    short_text = models.CharField(max_length=255)
    body_html = models.TextField()
    body_plain = models.TextField()
    body_md = models.TextField(blank=True, null=True)
    media = models.JSONField(blank=True, null=True)
    meta = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        ordering = ('-issued_at', )

    def set_issuer_based_on_email(self):
        try:
            issuer_email = IssuerEmail.objects.filter(email=self.from_email).get()
            self.issuer_email = issuer_email
            self.issuer = self.issuer_email.issuer
        except ObjectDoesNotExist:
            # mail staff on unknown issuer email
            url = settings.DOMAIN + reverse('admin:docs_doc_change', args=[self.id])
            mail_staff(
                subject='Nuevo input sin issuer asignado',
                message=f"""key: {self.id} {url}/n
                from: {self.from_email}/n
                title: {self.title}
                """,
                html_message=f"""key: <a href="{url}">{self.id}</a><br/>
                from: {self.from_email}<br/>
                title: {self.title}<br/>
                """,
            )

    @classmethod
    def from_string(cls, raw_email, key):

        mail = mailparser.parse_from_string(raw_email)

        media = cls.process_media(key, mail)
        body_html = ','.join(mail.text_html)

        # correctly set s3 attachments urls
        if body_html:
            for att in media:
                if att['cid']:
                    body_html = body_html.replace('cid:{}'.format(att['cid']), att['url'])

        doc = cls(**{
            'id': key,
            'title': mail.subject,
            'slug': slugify(mail.subject),
            'from_email': mail.from_[0][1],
            'body_html': body_html,
            'body_plain': ','.join(mail.text_plain),
            'body_md': md(' '.join(mail.text_html)),
            'media': media,
            'meta': [],
            'issued_at': mail.date.replace(tzinfo=pytz.UTC),
        })
        doc.set_issuer_based_on_email()
        return doc

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
                Bucket=settings.AWS_S3_BUCKET_NAME_INPUT_ATTACHMENTS,
                ContentType=att['mail_content_type'],
                Key=filename,
            )

            # location = s3client.get_bucket_location(Bucket=AWS_S3_BUCKET_NAME_INPUT_ATTACHMENTS)['LocationConstraint']
            url = "%s/%s" % (settings.AWS_S3_DOMAIN_INPUT_ATTACHMENTS, filename)
            cid = att['content-id'].strip('<>')

            media.append({
                'type': att['mail_content_type'],
                'filename': att['filename'],
                'url': url,
                'cid': cid,
            })

        return media

    @classmethod
    def from_s3(cls, objectKey):

        s3 = boto3.resource('s3', )

        file = s3.Object(settings.AWS_S3_BUCKET_NAME_INPUT, objectKey)
        print(f'Downloading from {objectKey}')

        mailBody = file.get()['Body'].read().decode('utf-8')
        print(f'Got body from {objectKey}')

        return cls.from_string(mailBody, objectKey)
