from django.urls import re_path

from .views import get_phone_info

urlpatterns = [
    re_path(
        r'^phones/(?P<raw_phone>7[0-9]{10})$',
        get_phone_info,
        name='phone-info-detail',
    ),
]
