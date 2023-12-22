from sys import exception
from typing import Any
from django.core.management.base import BaseCommand, CommandError, CommandParser
from datetime import datetime
from contentfeed.models import ContentItem, Publications
from contentfeed.views import publications

class Command(BaseCommand):
    def add_arguments(self, parser: CommandParser):
        parser.add_argument("item_title",type=str)
        parser.add_argument("item_url",type=str)
        parser.add_argument("item_datepub",type=str)
        parser.add_argument("item_source",type=str)
    
    def handle(self, *args: Any, **options: Any):
        ititle = options["item_title"]
        iurl = options["item_url"]
        idatepub = options["item_datepub"]
        icreate = datetime.now()
        isource = options["item_source"]

        try:
            newitem = ContentItem(
                item_title=ititle, 
                item_url=iurl, 
                item_datepublished = idatepub,
                item_datecreated = icreate,
                item_source = Publications.objects.get(pub_id=isource),
            )
            newitem.save()
        except:
            self.stdout.write("Item not created: "+ititle)