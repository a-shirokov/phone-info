import uuid

from django.db import connection, models
from phone_info.core.db.utils import sane_repr


class PhoneNumberingManager(models.Manager):

    def get_by_code(self, code):
        return self.get(code=code)

    def clear_all(self):
        cursor = connection.cursor()
        cursor.execute(f'TRUNCATE TABLE "{self.model._meta.db_table}";')


class PhoneNumbering(models.Model):
    id = models.UUIDField(
        verbose_name='идентификатор',
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    code = models.SmallIntegerField(
        verbose_name='код',
        db_index=True,
    )

    start = models.IntegerField(
        verbose_name='начало нумерации',
    )
    end = models.IntegerField(
        verbose_name='окончание нумерации',
    )
    count = models.IntegerField(
        verbose_name='количество',
    )

    operator_name = models.CharField(
        'наименование оператора',
        max_length=500,
    )
    region_name = models.CharField(
        'наименование региона',
        max_length=250,
    )

    objects = PhoneNumberingManager()

    class Meta:
        verbose_name = 'справочник нумерации телефонных номеров'
        verbose_name_plural = 'справочники нумерации телефонных номеров'
        db_table = 'phonenumbering'

    __repr__ = sane_repr(
        'code', 'start', 'end', 'count', 'operator_name', 'region_name',
    )

    def __str__(self):
        return self.get_display_name()

    def get_display_name(self):
        return f'{self.code} {self.start}-{self.end}'
