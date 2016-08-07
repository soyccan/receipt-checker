# manually edited

from django.db.migrations import Migration as _Migration
from django.db.migrations import RunSQL


class Migration(_Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        RunSQL(
            "INSERT INTO main_prize VALUES(0, '特別獎', '同期統一發票收執聯8位數號碼與上列號碼相同者', 1000000);"
            "INSERT INTO main_prize VALUES(1, '特獎', '同期統一發票收執聯8位數號碼與上列號碼相同者', 2000000);"
            "INSERT INTO main_prize VALUES(2, '頭獎', '同期統一發票收執聯8位數號碼與上列號碼相同者', 200000);"
            "INSERT INTO main_prize VALUES(3, '二獎', '同期統一發票收執聯末7位數號碼與頭獎中獎號碼末7位相同者', 40000);"
            "INSERT INTO main_prize VALUES(4, '三獎', '同期統一發票收執聯末6位數號碼與頭獎中獎號碼末6位相同者', 10000);"
            "INSERT INTO main_prize VALUES(5, '四獎', '同期統一發票收執聯末5位數號碼與頭獎中獎號碼末5位相同者', 4000);"
            "INSERT INTO main_prize VALUES(6, '五獎', '同期統一發票收執聯末4位數號碼與頭獎中獎號碼末4位相同者', 1000);"
            "INSERT INTO main_prize VALUES(7, '六獎', '同期統一發票收執聯末3位數號碼與頭獎中獎號碼末3位相同者', 200);"
            "INSERT INTO main_prize VALUES(8, '增開六獎', '同期統一發票收執聯末3位數號碼與上列號碼相同者', 200);"
        )
    ]
