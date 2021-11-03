from rest_framework import mixins, viewsets


class RetrieveListModelViewSet(mixins.RetrieveModelMixin,
                               mixins.ListModelMixin,
                               viewsets.GenericViewSet):
    pass
