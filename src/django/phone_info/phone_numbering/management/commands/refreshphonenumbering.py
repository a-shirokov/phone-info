from django.apps import apps as dj_apps
from django.conf import settings
from django.core.management import BaseCommand

from ...helpers import load_data


class Command(BaseCommand):
    help = "Обновляет данные справочника нумерации телефонных номеров."

    def handle(self, *app_labels, **options):
        self.verbosity = options['verbosity']

        PhoneNumbering = dj_apps.get_model('phone_numbering', 'PhoneNumbering')

        if not settings.PHONE_NUMBERING_SOURCES:
            if self.verbosity > 0:
                self.stdout.write('В настройках не указан ни один источник!')
            return

        if PhoneNumbering.objects.exists:
            if self.verbosity > 1:
                self.stdout.write('Очищаем справочник!')

            PhoneNumbering.objects.clear_all()

        for source in settings.PHONE_NUMBERING_SOURCES:
            if self.verbosity > 1:
                self.stdout.write(f"Загрузка данных из источника '{source}'...")

            try:
                load_data(source)
            except Exception:
                self.stderr.write('Возникла ошибка при загрузке данных. '
                                  'Данные загружены не полностью!')

        if self.verbosity > 1:
            self.stdout.write('Справочник обновлен!')
