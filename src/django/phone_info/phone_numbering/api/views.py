from django.http import Http404
from phonenumber_field.phonenumber import PhoneNumber
from phonenumbers import NumberParseException
from rest_framework import status as https_status
from rest_framework.decorators import api_view, throttle_classes
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle

from ..models import PhoneNumbering


@api_view(['GET'])
@throttle_classes([AnonRateThrottle])
def get_phone_info(request, raw_phone):
    try:
        phone = PhoneNumber.from_string(phone_number=raw_phone)
    except NumberParseException:
        raise Http404

    if not phone.is_valid():
        raise Http404

    code = int(raw_phone[1:4])
    number = int(raw_phone[4:])
    try:
        phone_info = PhoneNumbering.objects.get(
            code=code, start__lte=number, end__gte=number,
        )
    except PhoneNumbering.DoesNotExist:
        return Response({
            'detail': f"Информация о номере телефона '{phone.as_e164}' "
                      f"отсутствует."
        }, status=https_status.HTTP_400_BAD_REQUEST)

    return Response({
        'operator': phone_info.operator_name,
        'region': phone_info.region_name,
    })
