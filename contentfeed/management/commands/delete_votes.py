from typing import Any
from django.core.management.base import BaseCommand
from contentfeed.models import Votes

class Command(BaseCommand):
    def handle(self, *args: Any, **options: Any):
        Votes.objects.all().delete()
