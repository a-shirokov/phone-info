from django.urls import include, path

# API
api_urlpatterns = []

from phone_info.phone_numbering.api.urls import (  # noqa
    urlpatterns as phone_num_urls,
)
api_urlpatterns += phone_num_urls


from phone_info.phone_numbering.web.views import PhoneInfoView  # noqa
urlpatterns = [
    path('', PhoneInfoView.as_view(), name='phone_info'),

    path('api/', include(api_urlpatterns)),
]
