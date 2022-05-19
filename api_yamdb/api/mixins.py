from rest_framework import viewsets
from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   ListModelMixin)


class CustomMixin(CreateModelMixin,
                  DestroyModelMixin,
                  ListModelMixin,
                  viewsets.GenericViewSet):
    pass
