import datetime
import re
import ssl
from collections.abc import Iterable
from lxml import html
from itertools import chain
from json import JSONEncoder
from typing import Any
from typing import Dict
from typing import Generator
from typing import Sequence
from urllib.request import urlopen

from main.models import Prize


DIGIT = '〇一二三四五六七八九'
UNIT = ('千', '百', '十', '')
LARGE_UNIT = ('兆', '億', '萬', '')


class _HugeNumeral(Exception):
    """numeral too big to handle"""
    def __str__(self):
        return 'Numeral over limit of sixteen digit!'

class _JSONEncoder(JSONEncoder):
    """support arbitrary iterators"""
    def default(self, o):
        if isinstance(o, Iterable):
            return tuple(o)
        else:
            return super().default(o)
_json_encoder = _JSONEncoder()

class Event:
    """datecode: 5-lengthed string, for example,
       08809 means september of year 88"""
    @classmethod
    def fromdate(cls, date: datetime.date):
        cls.year = date.year - 1911
        cls.begin_month = date.month - 2
        if date.day < 25:
            cls.begin_month -= 2
        if date.month % 2 == 0:
            cls.begin_month -= 1
        if cls.begin_month <= 0:
            cls.year -= 1
            cls.begin_month += 12
        cls.end_month = cls.begin_month + 1
        cls.datecode = '{:03}{:02}'.format(cls.year, cls.begin_month)
        return cls()

    @classmethod
    def fromdatecode(cls, datecode: str):
        cls.datecode = datecode
        cls.year = int(datecode[0:3])
        cls.begin_month = int(datecode[3:5])
        cls.end_month = cls.begin_month + 1
        return cls()

    @classmethod
    def fromstring(cls, datestr):
        (cls.year,
         cls.begin_month,
         cls.end_month) = map(int, re.findall(r'\d+', datestr))
        if cls.year > 1911:
            cls.year -= 1911
        cls.datecode = '{:03}{:02}'.format(cls.year, cls.begin_month)
        return cls()

    def __str__(self):
        """example: 104年5-6月"""
        return '{}年{}-{}月'.format(self.year, self.begin_month, self.end_month)


def _split_number(number: str) -> Generator:
    # split number per four digit
    # length of number must be a multiple of four
    return (number[i:i+4] for i in range(0, len(number), 4))

def _under_10000(number: str) -> Generator:
    for i, n in enumerate(number):
        yield DIGIT[int(n)]
        if n != '0':
            yield UNIT[i]

def _over_10000(number: str) -> Generator:
    for i, n in enumerate(_split_number(number)):
        yield _under_10000(n)
        if n != '0000':
            yield LARGE_UNIT[i]

def chinese_numeral(numeral: int) -> str:
    """translate Arabic numeral to Chinese numeral
    sixteen digits for maximum
    give an integer and return translated string

    Example: 1234567890123456 -->
        一千二百三十四兆五千六百七十八億九千〇一十二萬三千四百五十六
    """
    if numeral == 0:
        return DIGIT[0]
    elif numeral > 9999999999999999: # 京
        raise _HugeNumeral

    result = ''.join(chain.from_iterable(
        _over_10000(str(numeral).zfill(16)))).strip('〇')
    result = re.sub('〇+', '〇', result)
    result = re.sub('^一十', '十', result)
    return result

def encode_json(obj: Any) -> str:
    """Return a JSON string representation of a Python data structure."""
    return _json_encoder.encode(obj)

def format_date(datecode: str) -> str:
    return Event.fromdatecode(datecode).__str__()

def fetch_winnum(event: Event) -> Sequence[Dict]:
    # 財政部網站
    tree = html.parse(urlopen(
        'https://www.etax.nat.gov.tw/etw-main/web/ETW183W2_'+event.datecode,
        context=ssl._create_unverified_context()))

    result = []
    table = tree.find('//table')
    for i in (3,5,7,19):
        prizetype = table[i].find('tr/th').text
        nums = table[i+1].find('tr/td/span').text
        for num in nums.split('、'): # 頓號 ideographic comma
            result.append({
                'datecode': event.datecode,
                'prizetype': Prize.objects.get(name=prizetype),
                'number': num})
    return result
