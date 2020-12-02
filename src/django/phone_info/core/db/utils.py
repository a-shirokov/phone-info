import datetime
from enum import Enum


def sane_repr(*attrs):
    from django.utils.timezone import is_aware

    def _repr(self):
        cls = type(self).__name__

        attr_list = attrs

        pk_field_name = self._meta.pk.attname
        if pk_field_name not in attr_list:
            attr_list = (pk_field_name,) + attr_list

        pairs = []
        for attr in attr_list:
            val = getattr(self, attr, None)

            if val is None:
                r = '<none>'
            elif isinstance(val, str):
                r = "'{}'".format(val)
            elif isinstance(val, datetime.datetime):
                _val = val.isoformat()
                if val.microsecond:
                    _val = _val[:23] + _val[26:]
                if _val.endswith('+00:00'):
                    _val = _val[:-6] + 'Z'

                r = "'{}'".format(_val)
            elif isinstance(val, datetime.date):
                _val = val.isoformat()

                r = "'{}'".format(_val)
            elif isinstance(val, datetime.time):
                if is_aware(val):
                    raise ValueError("JSON can't represent timezone-aware times.")

                _val = val.isoformat()
                if val.microsecond:
                    _val = _val[:12]

                r = "'{}'".format(_val)
            elif issubclass(type(val), Enum):
                r = str(val.name)
            else:
                r = repr(val)

            pairs.append('{}={}'.format(attr, r))

        return '<{}: {}>'.format(cls, ', '.join(pairs))

    return _repr
