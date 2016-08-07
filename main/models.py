from django.db.models import ForeignKey
from django.db.models import IntegerField
from django.db.models import Model
from django.db.models import TextField


class Prize(Model):
    typeid = IntegerField(primary_key=True)
    name = TextField()
    description = TextField()
    value = IntegerField()

    def __str__(self):
        return '{} {}'.format(self.typeid, self.name)

class WinNum(Model):
    datecode = TextField(blank=False)
    prizetype = ForeignKey(Prize, blank=False)
    number = TextField(blank=False)
