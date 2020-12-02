from django import forms
from phonenumber_field.formfields import PhoneNumberField

from ..models import PhoneNumbering


class PhoneNumberForm(forms.Form):
    phone = PhoneNumberField(
        label='Номер телефона',
        widget=forms.TextInput(
            attrs={'placeholder': '+7 xxx xxxxxxx'}
        )
    )

    def __init__(self, *args, **kwargs):
        self._phone_info = None
        super().__init__(*args, **kwargs)

    def clean(self):
        phone = self.cleaned_data.get('phone')
        phone_str = str(phone.national_number)

        code = int(phone_str[:3])
        number = int(phone_str[3:])
        try:
            self._phone_info = PhoneNumbering.objects.get(
                code=code, start__lte=number, end__gte=number,
            )
        except PhoneNumbering.DoesNotExist:
            pass

        return self.cleaned_data

    def get_phone_info(self):
        return self._phone_info
