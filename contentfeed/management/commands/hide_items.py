from typing import Any
from django.core.management.base import BaseCommand, CommandError, CommandParser
from django.core import management
import feedparser
from datetime import datetime, date
from zoneinfo import ZoneInfo
from contentfeed.models import Publications, ContentItem

class Command(BaseCommand):
    def handle(self, *args: Any, **options: Any):
        h_pub = Publications.objects.filter(pub_hidden=True)
        for pub in h_pub:
            c_item = ContentItem.objects.filter(item_source = pub.pub_id)
            for item in c_item:
                item.item_hidden = True
                item.save()
