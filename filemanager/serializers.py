from rest_framework import serializers
from filemanager.models import FileManager, FileStorageSize
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import os


class FileManagerSerializer(serializers.ModelSerializer):

    size = serializers.SerializerMethodField()
    file_type = serializers.SerializerMethodField()

    class Meta:
        model = FileManager
        # fields = "__all__"
        fields = (
            "id",
            "name",
            "file_public",
            "file_private",
            "size",
            "file_type",
            "storage_type",
            "created_date",
        )

    def validate(self, data):

        if not data.get("file_private") and not data.get("file_public"):
            raise serializers.ValidationError(
                {"detail": _("At least one of the fields file_public or file_private required be filled.")}
            )

        return data

    def get_size(self, value):

        if value.storage_type == "public":
            file_obj = value.file_public
        else:
            file_obj = value.file_private

        return file_obj.size

    def get_file_type(self, value):

        if value.storage_type == "public":
            file_obj = value.file_public
        else:
            file_obj = value.file_private

        name, extension = os.path.splitext(file_obj.name)
        return extension

    def create(self, validated_data):

        print("file burada", validated_data.get("file"))

        data = {}
        data["user"] = validated_data.get("user")
        data["name"] = validated_data.get("name")

        if validated_data.get("file_public"):
            data["storage_type"] = "public"
            data["file_public"] = validated_data.get("file_public")
        else:
            data["storage_type"] = "private"
            data["file_private"] = validated_data.get("file_private")

        print(data)

        instance = FileManager.objects.create(**data)

        return instance


def convert_bytes(size):
    """Convert bytes to KB, or MB or GB"""
    for x in ["bytes", "KB", "MB", "GB", "TB"]:
        if size < 1024.0:
            return "%3.1f %s" % (size, x)
        size /= 1024.0


class FileManagerFilterSerializer(serializers.ModelSerializer):

    size = serializers.SerializerMethodField()
    file_type = serializers.SerializerMethodField()

    class Meta:
        model = FileManager
        fields = (
            "id",
            "name",
            "size",
            "file_type",
            "file_public",
            "file_private",
            "storage_type",
            "created_date",
        )

    def get_size(self, value):

        if value.storage_type == "public":
            file_obj = value.file_public
        else:
            file_obj = value.file_private

        return file_obj.size

    def get_file_type(self, value):

        if value.storage_type == "public":
            file_obj = value.file_public
        else:
            file_obj = value.file_private

        name, extension = os.path.splitext(file_obj.name)
        return extension


class FileStorageSizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileStorageSize
        fields = "__all__"
