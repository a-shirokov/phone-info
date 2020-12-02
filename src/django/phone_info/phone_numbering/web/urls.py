from django.urls import path

from .views import PhoneInfoView

urlpatterns = [
    path('', PhoneInfoView.as_view(), name='phone_info'),
]
