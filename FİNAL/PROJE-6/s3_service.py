"""
S3 Servisi — PROJE-6
Dosyaları AWS S3'e yükler ve siler.
"""

import os
import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv

load_dotenv()

# S3 istemcisi oluştur
s3_client = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION", "eu-central-1")
)

BUCKET_NAME = os.getenv("S3_BUCKET_NAME")


def upload_to_s3(file_obj, filename):
    """
    Dosyayı S3'e yükler.
    
    Args:
        file_obj: Flask file object (request.files["file"])
        filename: S3'e kaydedilecek dosya adı (uuid.ext)
    
    Returns:
        tuple: (s3_key, public_url)
    """
    s3_key = f"uploads/{filename}"

    # Dosyayı S3'e yükle (public-read)
    s3_client.upload_fileobj(
        file_obj,
        BUCKET_NAME,
        s3_key,
        ExtraArgs={
            "ContentType": _get_content_type(filename)
        }
    )

    # Public URL oluştur
    region = os.getenv("AWS_REGION", "eu-central-1")
    s3_url = f"https://{BUCKET_NAME}.s3.{region}.amazonaws.com/{s3_key}"

    return s3_key, s3_url


def delete_from_s3(s3_key):
    """S3'ten dosyayı siler."""
    try:
        s3_client.delete_object(Bucket=BUCKET_NAME, Key=s3_key)
        return True
    except ClientError as e:
        print(f"S3 silme hatası: {e}")
        return False


def _get_content_type(filename):
    """Dosya uzantısına göre MIME type döndürür."""
    ext = filename.rsplit(".", 1)[-1].lower()
    types = {
        "jpg": "image/jpeg",
        "jpeg": "image/jpeg",
        "png": "image/png",
        "gif": "image/gif",
        "bmp": "image/bmp",
        "webp": "image/webp",
        "mp4": "video/mp4",
        "mov": "video/quicktime",
        "avi": "video/x-msvideo",
        "mkv": "video/x-matroska"
    }
    return types.get(ext, "application/octet-stream")
