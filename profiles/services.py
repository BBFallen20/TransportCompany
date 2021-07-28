from django.utils.translation import ugettext_lazy as _
from rest_framework.response import Response


def is_driver(func):
    def outer(self, request, **kwargs):
        if 'driver' in list(map(lambda x: x.name.lower(), request.user.groups.all())):
            return func(self, request)
        return Response({'detail': _('Driver group required to view this page.')}, 401)
    return outer
