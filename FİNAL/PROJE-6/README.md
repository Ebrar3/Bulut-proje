# PROJE-6: CloudVision — AWS Rekognition ile Görsel Analiz

**Öğrenci:** Arife Ebrar Üstüner | **No:** 23291207 | **Ders:** Bulut Bilişim (3522)

## Proje Hakkında

Bu proje, AWS Rekognition yapay zeka servisini kullanarak fotoğraf ve videolar üzerinde otomatik analiz yapan bir web uygulamasıdır.

Kullanıcı bir dosya yükler → AWS S3'e kaydedilir → Rekognition analiz eder → Sonuçlar güzel bir arayüzde gösterilir.

**Analiz Türleri:**
- 🏷️ **Nesne Tanıma:** İnsan, araba, hayvan, nesne tespiti (%confidence ile)
- 😊 **Yüz Analizi:** Yaş tahmini, duygu tespiti, gözlük/sakal/gülümseme
- 📝 **Metin Tespiti (OCR):** Resimdeki yazılar, plakalar, tabelalar
- 🎬 **Video Analizi:** MP4 videolarda nesne tespiti (asenkron)

## Dosya Yapısı

```
PROJE-6/
├── app.py                 → Flask web sunucusu (ana uygulama)
├── rekognition_service.py → AWS Rekognition API çağrıları
├── s3_service.py          → AWS S3 dosya yükleme/silme
├── templates/
│   ├── index.html         → Dosya yükleme arayüzü (dark mode)
│   └── result.html        → Analiz sonuçları sayfası
├── requirements.txt       → Python bağımlılıkları
├── .env.example           → AWS credentials şablonu
└── docs/
    └── PROJE6_RAPOR.md
```

## Hızlı Başlangıç

```bash
# 1. Bağımlılıkları kur
pip install -r requirements.txt

# 2. .env dosyası oluştur
cp .env.example .env
# .env dosyasını düzenle — AWS credentials ekle

# 3. Uygulamayı başlat
python app.py
# → http://localhost:5000 adresini aç
```

## AWS Kurulumu

### 1. S3 Bucket Oluştur
- AWS Console → S3 → Create bucket
- Bucket adı: `proje6-rekognition-HESAP_ID`
- Region: `eu-central-1`
- Public access: **Açık** bırak (görselleri göstermek için)

### 2. IAM Kullanıcısı / Yetki
Mevcut IAM kullanıcısına şu izinleri ekle:
- `AmazonRekognitionFullAccess`
- `AmazonS3FullAccess`

### 3. .env Dosyasını Doldur

```
AWS_ACCESS_KEY_ID=AKIAXXXXXXXXXXXXXXXX
AWS_SECRET_ACCESS_KEY=xxxxxxxx...
AWS_REGION=eu-central-1
S3_BUCKET_NAME=proje6-rekognition-HESAP_ID
```
