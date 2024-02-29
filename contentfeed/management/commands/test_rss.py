from typing import Any
from django.core.management.base import BaseCommand
import feedparser
from datetime import datetime
from zoneinfo import ZoneInfo

class Command(BaseCommand):
    def handle(self, *args: Any, **options: Any):
        test_url = 'https://blog.frost.kiwi/feed'
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
                try:
                    pub_date = datetime(*r.published_parsed[:6],tzinfo=ZoneInfo('Pacific/Auckland'))
                    pub_date = datetime.date(pub_date)
                except:
                    pub_date = datetime.today()
                    pub_date = datetime.date(pub_date)
                self.stdout.write(r.title + ',' + r.link + ',' + str(pub_date) + ': ', ending="")
                r_check = 0  