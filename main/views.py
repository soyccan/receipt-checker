import re

from django.http import HttpResponse, Http404
from django.shortcuts import render

from main.models import Prize
from main.models import WinNum
from main.utils import encode_json
from main.utils import format_date
from main.utils import Event


def load(request):
    date_list = []
    for datecode in (WinNum.objects
          .values_list('datecode', flat=True)
          .order_by('-datecode')
          .distinct()):
        date_list.append((format_date(datecode), datecode))

    last_win_num = (WinNum.objects
        .filter(datecode=date_list[0])
        .values_list('number', flat=True))

    return render(request, 'main.html', {
        'date_list': date_list,
        'last_win_num': encode_json(last_win_num)
    })

def win_num(request):
    return HttpResponse(
        encode_json(
            WinNum.objects
            .filter(datecode=request.GET['datecode'])
            .values_list('number', flat=True)),
        content_type='application/json')

def full_check(request):
    # TODO: simplify
    result = None
    num = request.GET['num']
    datecode = request.GET['datecode']
    if not re.match(r'\d{8}', num) or not re.match(r'\d{5}', datecode):
        raise Http404("Internal Error")

    for win_num in WinNum.objects.filter(datecode=datecode):
        if (win_num.prizetype.name in ('特別獎', '特獎', '頭獎')
                and num == win_num.number):
            result = win_num.prizetype
        elif win_num.prizetype.name == '頭獎':
            if num[1:] == win_num.number[1:]:
                result = Prize.objects.get(name='二獎')
            elif num[2:] == win_num.number[2:]:
                result = Prize.objects.get(name='三獎')
            elif num[3:] == win_num.number[3:]:
                result = Prize.objects.get(name='四獎')
            elif num[4:] == win_num.number[4:]:
                result = Prize.objects.get(name='五獎')
            elif num[5:] == win_num.number[5:]:
                result = Prize.objects.get(name='六獎')
        elif win_num.prizetype.name == '增開六獎' and num[5:] == win_num.number:
            result = win_num.prizetype

    if result:
        return HttpResponse(encode_json({
            'prizeName': result.name,
            'prizeValue': '{:,}'.format(result.value)
        }), content_type='application/json')
    else:
        raise Http404("Internal Error")
