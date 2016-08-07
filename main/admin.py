import datetime

from django.contrib.admin import ModelAdmin
from django.contrib.admin import register

from main.models import Prize
from main.models import WinNum
from main.utils import Event
from main.utils import fetch_winnum as _fetch_winnum


@register(Prize)
class PrizeAdmin(ModelAdmin):
    list_display = ('typeid', 'name', 'description', 'value')

@register(WinNum)
class WinNumAdmin(ModelAdmin):
    actions = ['fetch_winnum']
    list_display = ('datecode', 'prizetype', 'number')

    def fetch_winnum(self, request, queryset):
        for winnum in _fetch_winnum(Event.fromdate(datetime.date.today())):
            WinNum.objects.create(**winnum)
    fetch_winnum.short_description = '自網路取得中獎號碼'

    def datecode(self, obj):
        return obj.datecode
    datecode.admin_order_field = '-datecode'

