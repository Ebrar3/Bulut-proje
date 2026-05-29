"""
PROJE-6: Video Akışı ve İşleme Uygulaması
AWS Rekognition + S3 + Flask

Kullanıcı fotoğraf veya video yükler, AWS Rekognition ile analiz edilir.
Nesne tanıma, yüz analizi ve metin tespiti yapılır.
"""

import os
import uuid
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

# Servisler
from s3_service import upload_to_s3, upload_bytes_to_s3, delete_from_s3
from rekognition_service import detect_labels, detect_faces, detect_text
from video_service import extract_frames

# .env dosyasından ortam değişkenlerini yükle
load_dotenv()

app = Flask(__name__)
app.secret_key = "proje6-bulut-bilisim-2026"

# Desteklenen dosya türleri
IMAGE_EXTENSIONS = {"jpg", "jpeg", "png", "gif", "bmp", "webp"}
VIDEO_EXTENSIONS = {"mp4", "mov", "avi", "mkv"}

# Maksimum dosya boyutu (200MB - video için)
app.config["MAX_CONTENT_LENGTH"] = 200 * 1024 * 1024

def allowed_file(filename, extensions):
    """Dosya uzantısının geçerli olup olmadığını kontrol eder."""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in extensions

def is_image(filename):
    return allowed_file(filename, IMAGE_EXTENSIONS)

def is_video(filename):
    return allowed_file(filename, VIDEO_EXTENSIONS)


# ─────────────────────────────────────────
# Route'lar
# ─────────────────────────────────────────

@app.route("/")
def index():
    """Ana sayfa — dosya yükleme formu."""
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    """
    Dosyayı al, S3'e yükle, Rekognition ile analiz et, sonuçları göster.
    """
    # Dosya kontrolü
    if "file" not in request.files:
        flash("Dosya seçilmedi!", "error")
        return redirect(url_for("index"))

    file = request.files["file"]
    if file.filename == "":
        flash("Dosya seçilmedi!", "error")
        return redirect(url_for("index"))

    if not (is_image(file.filename) or is_video(file.filename)):
        flash("Desteklenmeyen dosya türü! JPG, PNG veya MP4 yükleyin.", "error")
        return redirect(url_for("index"))

    # Güvenli ve benzersiz dosya ismi oluştur
    ext = file.filename.rsplit(".", 1)[1].lower()
    unique_filename = f"{uuid.uuid4().hex}.{ext}"

    try:
        # Dosyayı S3'e yükle
        s3_key, s3_url = upload_to_s3(file, unique_filename)

        bucket_name = os.getenv("S3_BUCKET_NAME")

        # Analiz seçeneklerini al
        run_labels = request.form.get("labels", "on") == "on"
        run_faces = request.form.get("faces", "on") == "on"
        run_text = request.form.get("text", "on") == "on"

        results = {
            "filename": file.filename,
            "s3_url": s3_url,
            "s3_key": s3_key,
            "file_type": "image" if is_image(file.filename) else "video",
            "labels": [],
            "faces": [],
            "text_detections": [],
            "video_frames": []  # Video karelerinin analiz sonuçları
        }

        if is_image(file.filename):
            # ── Resim Analizi ──
            if run_labels:
                results["labels"] = detect_labels(bucket_name, s3_key)
            if run_faces:
                results["faces"] = detect_faces(bucket_name, s3_key)
            if run_text:
                results["text_detections"] = detect_text(bucket_name, s3_key)

        else:
            # ── Video Analizi: Kareler çıkar, birleşik sonuç üret ──
            file.seek(0)
            frames = extract_frames(file, num_frames=5)

            merged_labels = {}  # name -> en yüksek confidence

            for i, frame_bytes in enumerate(frames, 1):
                frame_key, _ = upload_bytes_to_s3(
                    frame_bytes, f"frames/{uuid.uuid4().hex}_frame{i}.jpg"
                )
                frame_labels = detect_labels(bucket_name, frame_key, max_labels=10)

                # Her nesnenin en yüksek güven oranını sakla
                for lbl in frame_labels:
                    name = lbl["name"]
                    if name not in merged_labels or lbl["confidence"] > merged_labels[name]["confidence"]:
                        merged_labels[name] = lbl

            # Güven oranına göre sırala, en fazla 15 nesne
            results["labels"] = sorted(
                merged_labels.values(),
                key=lambda x: x["confidence"],
                reverse=True
            )[:15]

        return render_template("result.html", results=results)

    except Exception as e:
        flash(f"Analiz sırasında hata oluştu: {str(e)}", "error")
        return redirect(url_for("index"))


@app.route("/video-status/<job_id>")
def video_status(job_id):
    """Video analiz durumunu kontrol eder (AJAX endpoint)."""
    try:
        status, labels, error_message = get_video_label_results(job_id)
        return jsonify({
            "status": status,
            "labels": labels,
            "error": error_message
        })
    except Exception as e:
        return jsonify({"status": "ERROR", "error": str(e)}), 500


@app.route("/health")
def health():
    """Sağlık kontrolü endpoint'i."""
    return jsonify({"status": "healthy", "service": "PROJE-6 Rekognition"}), 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
