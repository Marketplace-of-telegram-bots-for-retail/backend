from django.db.models import F, OuterRef, Prefetch
from django_filters import rest_framework as dj_filters
from rest_framework import mixins, viewsets
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response


class OrderViewSet(viewsets.ModelViewSet):
    def list(self, request, *args, **kwargs):
        return Response({'message': 'в разработке'})

    def create(self, request, *args, **kwargs):
        return Response({'message': 'в разработке'})

    def retrieve(self, request, *args, **kwargs):
        return Response({'message': 'в разработке'})

    def update(self, request, *args, **kwargs):
        return Response({'message': 'в разработке'})

    def partial_update(self, request, *args, **kwargs):
        return Response({'message': 'в разработке'})

    def destroy(self, request, *args, **kwargs):
        return Response({'message': 'в разработке'})
