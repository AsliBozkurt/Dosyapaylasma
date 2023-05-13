import os
import re
import secrets
from datetime import date, datetime, time, timedelta

from django.contrib.auth import authenticate, login

import boto3

from users.models import CustomUser


def filemanager_size(user_id):
    """User için S3 deki dosya alanını hesaplar

    Args:
        user_id (_type_): CustomUser.id

    Returns:
        int: byte
    """
    AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID_S3")
    AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY_S3")

    conn = boto3.resource(
        service_name="s3",
        region_name="eu-west-1",
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    )

    prefix_public = f"media/public/user_file/{user_id}"
    prefix_private = f"media/private/user_file/{user_id}"

    my_bucket = conn.Bucket(os.environ.get("AWS_STORAGE_BUCKET_NAME_S3"))
    total_size_public = 0
    for obj in my_bucket.objects.filter(Prefix=prefix_public):
        total_size_public = total_size_public + obj.size
    total_size_private = 0
    for obj in my_bucket.objects.filter(Prefix=prefix_private):
        total_size_private = total_size_private + obj.size

    return total_size_public + total_size_private
