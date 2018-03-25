#!/usr/bin/python3

import datetime, sys

from django.core.management.base import BaseCommand

from main.models import WinNum
from main.utils import fetch_winnum
from main.utils import Event


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('datecode', nargs='?')

    def handle(self, *args, **options):
        if options['datecode']:
            event = Event.fromdatecode(options['datecode'])
        else:
            event = Event.fromdate(datetime.date.today())

        if not event:
            print('ERROR!')
            return False

        if WinNum.objects.filter(datecode=event.datecode):
            print('Up-to-date:', event)
        else:
            print('Updating:', event)
            try:
                for winnum in fetch_winnum(event):
                    WinNum.objects.create(**winnum)
            except Exception as e:
                print(sys.exc_info())
                return False
            print('Success!')
