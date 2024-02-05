from tkinter.tix import Tree
from typing import Any
from django.core.management.base import BaseCommand
from contentfeed.models import ContentItem
from datetime import date, timedelta
import random

class Command(BaseCommand):
    def handle(self, *args: Any, **options: Any):
        datestart = date.today()
        dateend = datestart - timedelta (days=90)
        r = random.randint(1, 5)
        c = ContentItem.objects.filter(item_datepublished__range=[dateend,datestart],item_hidden=False).order_by('?')[:10]
        for i in c:
            i.item_votecount = i.item_votecount + r 
            i.save()
