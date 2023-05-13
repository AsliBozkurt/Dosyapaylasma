from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions, status, viewsets
from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import (
    SAFE_METHODS,
    BasePermission,
    DjangoModelPermissions,
    IsAdminUser,
    IsAuthenticated,
)
from rest_framework.response import Response
from rest_framework.views import APIView

from api.decorators import (
    BlocklistPermission,
    any_permission_drf_required,
    route_permissions,
)
from filemanager.filters import FileManagerFilter
from filemanager.models import FileManager, FileStorageSize
from filemanager.serializers import (
    FileManagerFilterSerializer,
    FileManagerSerializer,
    FileStorageSizeSerializer,
)
from api.helper import filemanager_size
from django.shortcuts import Http404


class LargeResultsSetCustomPagination(PageNumberPagination):
    page_size = 30
    page_size_query_param = "page_size"
    max_page_size = 50000

    def get_paginated_response(self, data):
        print(self.page.paginator.count, self.page_size)

        total_pages = self.page.paginator.count / self.page_size
        total_pages = round(total_pages)

        if total_pages == 0:
            total_pages = 1

        return Response(
            {
                "count": self.page.paginator.count,
                "results": data,
                "total_pages": total_pages,
            }
        )


class FileManagerView(APIView):
    """
    Dosya kaydeder.
    """

    permission_classes = (IsAuthenticated,)

    # def get(self, request, version, format=None):

    #     snippets = FileManager.objects.filter(emailvendor=1)
    #     serializer = EmailVendorDetailSerializer(snippets, many=True)
    #     return Response(serializer.data)

    parser_classes = [MultiPartParser]

    def post(self, request, version, format=None):
        user = self.request.user

        serializer = FileManagerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FileManagerFilter(ListAPIView):
    """
    İki tarih aralığında kaydedilen dosyaları getirir.
    """

    permission_classes = (IsAuthenticated,)

    serializer_class = FileManagerFilterSerializer
    pagination_class = LargeResultsSetCustomPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ["name", "created_date"]
    filterset_class = FileManagerFilter
    ordering_fields = ["id"]
    ordering = ["-id"]

    def get_queryset(self):
        user = self.request.user
        queryset = FileManager.objects.filter(user=user)

        return queryset


class FileManagerSizeView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, version):
        user = self.request.user

        content = {"user_size": filemanager_size(user.id), "storage_size": user.filestoragesize.size}

        return Response(content)


class FileManagerDetail(APIView):
    """
    Dosya detay bilgilerini getirir.
    """

    def get_object(self, pk, user):
        print(user.id)

        try:
            return FileManager.objects.get(pk=pk, user=user)
        except FileManager.DoesNotExist:
            raise Http404

    def get(self, request, pk, version, format=None):
        user = self.request.user
        snippet = self.get_object(pk, user)
        serializer = FileManagerSerializer(snippet)
        return Response(serializer.data)

    def delete(self, request, pk, version, format=None):
        user = self.request.user
        snippet = self.get_object(pk, user)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
