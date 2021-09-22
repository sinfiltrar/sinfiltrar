from django.db.models import F, CharField, Value, Count
from django.db.models.functions import Concat, Extract
from django.http import JsonResponse
from docs.models import Doc
from django.shortcuts import render

from datetime import timedelta
from django.utils import timezone
from django.utils.dateformat import format as format_date


def index(request):
    return render(request, 'stats/index.html')


def weekly_docs(request):

    from_date = Doc.objects.order_by('issued_at').first().issued_at.date()
    to_date = timezone.now().date()

    data = (Doc.objects
            .filter(issued_at__gte=from_date)
            .exclude(issuer=None)
            .annotate(month=Concat(Extract('issued_at', 'year'), Value('-'), Extract('issued_at', 'month'), output_field=CharField()))
            .values('month')
            .annotate(count=Count('*'), )
            .order_by('month',)
        )

    day_count = (to_date - from_date).days + 1
    series = {}
    for date in (from_date + timedelta(n) for n in range(day_count)):
        month = date.strftime('%Y-%-m')
        series[month] = {'month': format_date(date, 'N Y'), 'count': 0}

    for row in data:
        series[row['month']]['count'] = row['count']

    result = [series[row] for row in series]

    return JsonResponse(result, safe=False)
