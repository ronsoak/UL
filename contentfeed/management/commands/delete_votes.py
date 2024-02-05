from typing import Any
from django.core.management.base import BaseCommand
from contentfeed.models import Votes
from datetime import date, timedelta

class Command(BaseCommand):
    def handle(self, *args: Any, **options: Any):
        today = date.today()
        datestart = today - timedelta (days=3)
        dateend = datestart - timedelta (days=100)
        v = Votes.objects.filter(vote_date__range=[dateend,datestart])
        v.delete()
