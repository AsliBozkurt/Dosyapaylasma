from django.contrib import admin

from filemanager.models import FileManager, FileStorageSize


class FileStorageSizeAdmin(admin.ModelAdmin):
    list_display = ["user", "size"]

    class Meta:
        model = FileStorageSize


admin.site.register(FileStorageSize, FileStorageSizeAdmin)


class FileManagerAdmin(admin.ModelAdmin):
    list_display = ["user", "created_date", "storage_type"]

    class Meta:
        model = FileManager


admin.site.register(FileManager, FileManagerAdmin)
