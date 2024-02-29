from typing import Any
from django.core.management.base import BaseCommand, CommandError, CommandParser
from django.core import management
import feedparser
from datetime import datetime, date
from zoneinfo import ZoneInfo
from contentfeed.models import Publications, SourceType

class Command(BaseCommand):
    def handle(self, *args: Any, **options: Any):
        rssid = SourceType.objects.get(type_name__icontains="RSS").type_id
        rss_pubs = Publications.objects.filter(pub_feedtype=rssid, pub_hidden=False)
        for p in rss_pubs:
            pub_url = p.pub_feedurl
            pub_name = p.pub_name
            pub_id = p.pub_id
            r_check = 1
            try:
                r_content = feedparser.parse(pub_url)
            except:
                r_check = 0 
                raise CommandError("failed to parse feed: "+pub_name)
            while r_check == 1:
                if r_content.status >= 400:
                    r_check = 0 
                    raise CommandError("Bad HTTP Status: "+pub_name+"["+str(r_content.status)+"]")
                if r_content.bozo == 1:
                    r_check = 0 
                    raise CommandError("Bad Bozo Flag: "+pub_name+"["+str(r_content.bozo_exception)+"]")
                for r in r_content.entries:
                    try:
                        pub_date = datetime(*r.published_parsed[:6],tzinfo=ZoneInfo('Pacific/Auckland'))
                        pub_date = datetime.date(pub_date)
                    except:
                        pub_date = datetime.today()
                        pub_date = datetime.date(pub_date)
                    #self.stdout.write(r.title + ',' + r.link + ',' + str(pub_date) + ',' +pub_name + ': ', ending="")
                    management.call_command("write_content",r.title,r.link,pub_date,pub_id)
                    r_check = 0  