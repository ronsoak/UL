from typing import Any
from django.core.management.base import BaseCommand, CommandError, CommandParser
from django.core import management
import feedparser
from datetime import datetime, date
from zoneinfo import ZoneInfo
from contentfeed.models import Publications, SourceType

class Command(BaseCommand):
    def handle(self, *args: Any, **options: Any):
        test_url = 'https://patrickklepek.substack.com/feed'
        r_check = 1
        try:
            r_content = feedparser.parse(test_url)
        except:
            r_check = 0 
            self.stdout.write("failed to parse feed: ")
        while r_check == 1:
            if r_content.status >= 400:
                r_check = 0 
                self.stdout.write("Bad HTTP Status: "+"["+str(r_content.status)+"]")
            if r_content.bozo == 1:
                r_check = 0 
                self.stdout.write("Bad Bozo Flag: "+"["+str(r_content.bozo_exception)+"]")
            for r in r_content.entries:
                pub_date = datetime(*r.published_parsed[:6],tzinfo=ZoneInfo('Pacific/Auckland'))
                pub_date = datetime.date(pub_date)
                self.stdout.write(r.title + ',' + r.link + ',' + str(pub_date) + ': ', ending="")
                r_check = 0  