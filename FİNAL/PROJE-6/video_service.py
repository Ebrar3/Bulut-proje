"""
Video Frame Extraction Servisi — PROJE-6
Video dosyasından belirli aralıklarla kare çıkarır.
imageio + imageio-ffmpeg kullanılır.
"""

import io
import os
import tempfile
import imageio
from PIL import Image


def extract_frames(file_obj, num_frames=5):
    """
    Video dosyasından eşit aralıklı kareler çıkarır.

    Args:
        file_obj: Flask file object (video)
        num_frames: Kaç kare çıkarılacak (varsayılan: 5)

    Returns:
        list of bytes: Her kare için JPEG byte verisi
    """
    video_bytes = file_obj.read()
    file_obj.seek(0)  # S3 upload için pointer'ı başa al

    frames_data = []
    tmp_path = None

    try:
        # Geçici dosyaya yaz
        suffix = ".mp4"
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(video_bytes)
            tmp_path = tmp.name

        # imageio ile video oku
        reader = imageio.get_reader(tmp_path)
        total_frames = reader.count_frames()
        print(f"[VIDEO] Toplam kare: {total_frames}")

        if total_frames < 1:
            reader.close()
            return []

        # Eşit aralıklı kare indekslerini hesapla
        if total_frames <= num_frames:
            indices = list(range(total_frames))
        else:
            step = total_frames // num_frames
            indices = [i * step for i in range(num_frames)]

        print(f"[VIDEO] Seçilen indeksler: {indices}")

        for idx in indices:
            try:
                frame_array = reader.get_data(idx)
                pil_image = Image.fromarray(frame_array)
                if pil_image.mode != "RGB":
                    pil_image = pil_image.convert("RGB")
                # Büyük kareleri küçült (S3 ve Rekognition için)
                pil_image.thumbnail((1280, 720), Image.LANCZOS)
                buffer = io.BytesIO()
                pil_image.save(buffer, format="JPEG", quality=85)
                buffer.seek(0)
                frames_data.append(buffer.getvalue())
            except Exception as e:
                print(f"[VIDEO] Kare {idx} hatası: {e}")

        reader.close()

    except Exception as e:
        print(f"[FRAME EXTRACT ERROR] {e}")
        import traceback
        traceback.print_exc()
    finally:
        if tmp_path and os.path.exists(tmp_path):
            try:
                os.unlink(tmp_path)
            except Exception:
                pass

    print(f"[VIDEO] Çıkarılan kare sayısı: {len(frames_data)}")
    return frames_data
