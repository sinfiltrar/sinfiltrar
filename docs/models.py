from bs4 import BeautifulSoup
import mailparser
import markdown
import boto3
import base64
import logging
import pytz
import re
import twitter

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.urls import reverse
from django.utils.text import slugify

from docs.markdown import CleanMarkdownConverter
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
    slug = models.CharField(max_length=255, unique=True)
    short_text = models.CharField(max_length=255, blank=True, null=True)
    body_html = models.TextField()
    body_plain = models.TextField(blank=True, null=True)
    body_md = models.TextField()
    body = models.TextField(blank=True, null=True)
    media = models.JSONField(blank=True, null=True)
    meta = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        ordering = ('-issued_at', )

    def save(self, *args, **kwargs):
        insert = self._state.adding
        super().save(*args, **kwargs)
        # if insert:
        self.send_tweet()

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
        body_html = ' '.join(mail.text_html)

        # correctly set s3 attachments urls
        if body_html:
            for att in media:
                if att['cid']:
                    body_html = body_html.replace('cid:{}'.format(att['cid']), att['url'])

        # process body
        # convert to md to clean up all but the format
        body_md = CleanMarkdownConverter().convert(body_html)

        # convert again to html
        soup = BeautifulSoup(markdown.markdown(body_md), 'html.parser')

        # add target=_blank to a
        href_re = re.compile(r"^https?://")
        links = soup.find_all('a', href=href_re)
        for link in links:
            link['target'] = '_blank'

        doc = cls(**{
            'id': key,
            'title': mail.subject,
            'slug': slugify(mail.subject),
            'from_email': mail.from_[0][1],
            'body_html': body_html,
            'body_plain': ','.join(mail.text_plain),
            'body_md': body_md,
            'body': str(soup),
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

    def get_absolute_url(self):
        from django.urls import reverse
        return settings.DOMAIN + reverse('docs_one', kwargs={'slug': self.slug})

    def send_tweet(self):

        if self.issuer is None:
            return

        api = twitter.Api(consumer_key=settings.TWITTER_CONSUMER_API_KEY,
                          consumer_secret=settings.TWITTER_CONSUMER_API_SECRET_KEY,
                          access_token_key=settings.TWITTER_ACCESS_TOKEN,
                          access_token_secret=settings.TWITTER_ACCESS_TOKEN_SECRET)

        tweet = f'{self.issuer.name}: {self.title} – {self.get_absolute_url()}'

        print(f'Tweeting about Doc #{self.id}: {tweet}')

        api.PostUpdate(tweet)