from django.http import Http404
import time
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status
from rest_framework.filters import OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.decorators import route_permissions


class HelloView(APIView):
    """Hello options test"""

    def get(self, request, version):
        content = {"message": "Hello, World!"}
        return Response(content)


class HelloAView(APIView):
    """Hello options test IsAuthenticated"""

    permission_classes = (IsAuthenticated,)

    def get(self, request, version):
        content = {"message": "Hello, World! IsAuthenticated"}
        return Response(content)
