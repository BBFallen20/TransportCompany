from rest_framework.response import Response


def is_driver(func):
    def outer(self, request):
        if 'driver' in list(map(lambda x: x.name, request.user.groups.all())):
            return func(self, request)
        return Response({'detail': 'Driver group required to view this page.'}, 401)
    return outer
