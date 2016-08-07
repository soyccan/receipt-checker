#!/usr/bin/python3

import datetime

from django.core.management.base import BaseCommand

from main.models import WinNum
from main.utils import fetch_winnum
from main.utils import Event


class Command(BaseCommand):
    def handle(self, *args, **options):
        event = Event.fromdate(datetime.date.today())
        if WinNum.objects.filter(datecode=event.datecode):
            print('Up-to-date:', event)
        else:
            print('Updating:', event)
            for winnum in fetch_winnum(event):
                WinNum.objects.create(**winnum)
            print('Success!')
