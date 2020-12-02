import logging

from celery.app import app_or_default
from django.apps import apps as dj_apps
from django.conf import settings

from .helpers import load_data

app = app_or_default()


@app.task(name='phone_info.phone_numbering.workers.refresh_data')
def refresh_data():
    PhoneNumbering = dj_apps.get_model('phone_numbering', 'PhoneNumbering')

    if PhoneNumbering.objects.exists:
        PhoneNumbering.objects.clear_all()

    for source in settings.PHONE_NUMBERING_SOURCES:
        try:
            load_data(source)
        except Exception:
            logger = logging.getLogger('phone_info.phone_numbering.refresh_data')
            logger.exception(
                f"Не удалось полносью загрузить данные из '{source}'."
            )
