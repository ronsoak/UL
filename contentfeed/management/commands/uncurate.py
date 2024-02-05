from tkinter.tix import Tree
from typing import Any
from django.core.management.base import BaseCommand
from contentfeed.models import ContentItem

class Command(BaseCommand):
    def handle(self, *args: Any, **options: Any):
        c = ContentItem.objects.filter(item_curated=True,item_hidden=False).order_by('-item_datepublished')[4:20]
        for item in c:
            item.item_curated = False 
            item.save()