"""
AWS Rekognition Servisi — PROJE-6
Nesne tanıma, yüz analizi ve metin tespiti işlemleri.
"""

import os
import boto3
from dotenv import load_dotenv

load_dotenv()

# Rekognition istemcisi
rekognition_client = boto3.client(
    "rekognition",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION", "eu-central-1")
)


def detect_labels(bucket_name, s3_key, max_labels=15, min_confidence=70):
    """
    Resimdeki nesneleri/sahneleri tespit eder.
    Örnek: İnsan %99, Araba %95, Doğa %88 ...

    Returns:
        list of dict: [{"name": "Person", "confidence": 99.5, "parents": ["Human"]}, ...]
    """
    response = rekognition_client.detect_labels(
        Image={
            "S3Object": {
                "Bucket": bucket_name,
                "Name": s3_key
            }
        },
        MaxLabels=max_labels,
        MinConfidence=min_confidence
    )

    labels = []
    for label in response.get("Labels", []):
        parents = [p["Name"] for p in label.get("Parents", [])]
        labels.append({
            "name": label["Name"],
            "confidence": round(label["Confidence"], 1),
            "parents": parents,
            "emoji": _label_to_emoji(label["Name"])
        })

    # Confidence'a göre sırala (en yüksek önce)
    labels.sort(key=lambda x: x["confidence"], reverse=True)
    return labels


def detect_faces(bucket_name, s3_key):
    """
    Resimdeki yüzleri analiz eder.
    Yaş tahmini, duygu analizi, gözlük, sakal vb.

    Returns:
        list of dict: Her yüz için özellikler
    """
    response = rekognition_client.detect_faces(
        Image={
            "S3Object": {
                "Bucket": bucket_name,
                "Name": s3_key
            }
        },
        Attributes=["ALL"]  # Tüm özellikleri getir
    )

    faces = []
    for i, face in enumerate(response.get("FaceDetails", []), 1):
        # En baskın duyguyu bul
        emotions = face.get("Emotions", [])
        top_emotion = max(emotions, key=lambda x: x["Confidence"]) if emotions else {"Type": "UNKNOWN", "Confidence": 0}

        # Türkçe duygu adları
        emotion_map = {
            "HAPPY": "😊 Mutlu",
            "SAD": "😢 Üzgün",
            "ANGRY": "😠 Kızgın",
            "SURPRISED": "😮 Şaşkın",
            "CONFUSED": "😕 Kafası Karışık",
            "CALM": "😐 Sakin",
            "DISGUSTED": "🤢 İğrenmiş",
            "FEAR": "😨 Korkmuş",
            "UNKNOWN": "❓ Bilinmiyor"
        }

        age_low = face.get("AgeRange", {}).get("Low", 0)
        age_high = face.get("AgeRange", {}).get("High", 0)

        faces.append({
            "index": i,
            "age_range": f"{age_low}-{age_high} yaş",
            "gender": "Erkek" if face.get("Gender", {}).get("Value") == "Male" else "Kadın",
            "gender_confidence": round(face.get("Gender", {}).get("Confidence", 0), 1),
            "emotion": emotion_map.get(top_emotion["Type"], top_emotion["Type"]),
            "emotion_confidence": round(top_emotion["Confidence"], 1),
            "smile": "Gülümsüyor 😄" if face.get("Smile", {}).get("Value") else "Gülümsemiyor",
            "eyeglasses": "Gözlük var 👓" if face.get("Eyeglasses", {}).get("Value") else "Gözlük yok",
            "sunglasses": "Güneş gözlüğü var 🕶️" if face.get("Sunglasses", {}).get("Value") else "",
            "beard": "Sakal var 🧔" if face.get("Beard", {}).get("Value") else "",
            "mustache": "Bıyık var" if face.get("Mustache", {}).get("Value") else "",
            "confidence": round(face.get("Confidence", 0), 1)
        })

    return faces


def detect_text(bucket_name, s3_key):
    """
    Resimdeki metinleri tespit eder (OCR).
    Plakalar, tabelalar, yazılar vb.

    Returns:
        list of dict: [{"text": "HELLO", "confidence": 99.5, "type": "WORD"}, ...]
    """
    response = rekognition_client.detect_text(
        Image={
            "S3Object": {
                "Bucket": bucket_name,
                "Name": s3_key
            }
        }
    )

    texts = []
    seen = set()  # Tekrar eden kelimeleri engelle

    for text_detection in response.get("TextDetections", []):
        # Sadece LINE türündekileri al (kelimeleri değil, satırları)
        if text_detection["Type"] == "LINE":
            detected_text = text_detection["DetectedText"]
            confidence = round(text_detection["Confidence"], 1)

            if detected_text not in seen and confidence >= 70:
                seen.add(detected_text)
                texts.append({
                    "text": detected_text,
                    "confidence": confidence,
                    "type": text_detection["Type"]
                })

    return texts


def start_video_label_detection(bucket_name, s3_key):
    """
    Video için asenkron label detection başlatır.
    
    Returns:
        str: Job ID (durumu sorgulamak için kullanılır)
    """
    response = rekognition_client.start_label_detection(
        Video={
            "S3Object": {
                "Bucket": bucket_name,
                "Name": s3_key
            }
        },
        MinConfidence=70
    )
    return response["JobId"]


def get_video_label_results(job_id):
    """
    Video analiz işinin durumunu ve sonuçlarını getirir.
    
    Returns:
        tuple: (status, labels, error_message)
        status: "IN_PROGRESS" | "SUCCEEDED" | "FAILED"
    """
    response = rekognition_client.get_label_detection(
        JobId=job_id,
        SortBy="TIMESTAMP"
    )

    status = response["JobStatus"]
    error_message = response.get("StatusMessage", "")
    print(f"[VIDEO STATUS] {status} — {error_message}")  # Log için
    labels = []

    if status == "SUCCEEDED":
        seen_labels = {}
        for item in response.get("Labels", []):
            label = item["Label"]
            name = label["Name"]
            confidence = label["Confidence"]
            timestamp = item["Timestamp"]  # milisaniye

            # Her etiket için en yüksek confidence'ı tut
            if name not in seen_labels or confidence > seen_labels[name]["confidence"]:
                seen_labels[name] = {
                    "name": name,
                    "confidence": round(confidence, 1),
                    "timestamp_ms": timestamp,
                    "timestamp_sec": round(timestamp / 1000, 1),
                    "emoji": _label_to_emoji(name)
                }

        labels = sorted(seen_labels.values(), key=lambda x: x["confidence"], reverse=True)

    return status, labels, error_message


def _label_to_emoji(label_name):
    """Etiket adına göre emoji döndürür."""
    emoji_map = {
        "Person": "🧑", "Human": "🧑", "People": "👥", "Face": "😊",
        "Car": "🚗", "Vehicle": "🚙", "Truck": "🚛", "Bus": "🚌",
        "Dog": "🐕", "Cat": "🐈", "Animal": "🐾", "Bird": "🐦",
        "Tree": "🌳", "Plant": "🌿", "Flower": "🌸", "Nature": "🌿",
        "Building": "🏢", "Architecture": "🏛️", "House": "🏠",
        "Food": "🍽️", "Furniture": "🛋️", "Electronics": "💻",
        "Sky": "☁️", "Water": "💧", "Mountain": "⛰️", "Beach": "🏖️",
        "Road": "🛣️", "Text": "📝", "Sign": "🪧",
        "Clothing": "👕", "Accessory": "👜", "Sports": "⚽",
        "Phone": "📱", "Computer": "💻", "Screen": "🖥️",
        "Book": "📚", "Art": "🎨", "Music": "🎵"
    }
    for key, emoji in emoji_map.items():
        if key.lower() in label_name.lower():
            return emoji
    return "🏷️"  # Varsayılan
