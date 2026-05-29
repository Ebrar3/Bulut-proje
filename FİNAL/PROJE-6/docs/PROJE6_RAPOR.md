# BULUT BİLİŞİM (3522) — PROJE 6 RAPORU
# Video Akışı ve Görsel İşleme Uygulaması

**Öğrenci:** Arife Ebrar Üstüner
**Öğrenci No:** 23291207
**Ders:** Bulut Bilişim (3522)
**Tarih:** Mayıs 2026

---

## 📌 Proje Bağlantıları

- **GitHub Repository:** [Proje 6 Kaynak Kodları](https://github.com/Ebrar3/Bulut-proje/tree/main/FİNAL/PROJE-6)
- **Proje Sunum Videosu:** *(Drive linki)*

---

## 1. Projenin Amacı

Bu projede, AWS'nin yapay zeka tabanlı görüntü işleme servisi olan **Amazon Rekognition** kullanılarak fotoğraf ve videolar üzerinde otomatik analiz yapan bir web uygulaması geliştirilmiştir. Projenin temel hedefleri:

- Kullanıcının yüklediği fotoğraf/videoda **nesne ve sahne tanıma** yapmak
- Fotoğrafta bulunan **insan yüzlerini analiz etmek** (yaş tahmini, duygu tespiti, aksesuar tespiti)
- Görseldeki **yazıları otomatik okumak** (OCR — Optik Karakter Tanıma)
- Tüm bu işlemleri **bulut tabanlı, sunucusuz** bir yapay zeka API'si aracılığıyla gerçekleştirmek

---

## 2. Kullanılan Teknolojiler ve Mimari

### 2.1 Teknoloji Yığını

| Katman | Teknoloji | Açıklama |
|--------|-----------|----------|
| Backend | Python 3 + Flask | Web sunucusu, istek yönetimi |
| Dosya Depolama | AWS S3 | Yüklenen dosyaları bulutta saklar |
| Yapay Zeka | AWS Rekognition | Nesne, yüz, metin analizi |
| SDK | boto3 | Python için AWS kütüphanesi |
| Arayüz | HTML + CSS (Dark Mode) | Modern kullanıcı arayüzü |
| Ortam Yönetimi | python-dotenv | Güvenli kimlik bilgisi saklama |

### 2.2 Sistem Mimarisi

```
Kullanıcı (Tarayıcı)
       │
       │  1. Fotoğraf/Video yükle (HTTP POST)
       ▼
Flask Web Sunucusu (localhost:5000)
       │
       │  2. Dosyayı S3'e yükle
       ▼
AWS S3 (Depolama)
  proje6-rekognition-320042237584/uploads/
       │
       │  3. S3 Bucket bilgisini Rekognition'a gönder
       ▼
AWS Rekognition API
  ├── detect_labels()     → Nesne Tanıma
  ├── detect_faces()      → Yüz Analizi
  └── detect_text()       → Metin Tespiti (OCR)
       │
       │  4. JSON sonuçlarını Flask'a döndür
       ▼
Flask → result.html'i render et
       │
       ▼
Kullanıcı arayüzünde sonuçları görüntüle
```

### 2.3 Dosya Yapısı

```
PROJE-6/
├── app.py                 → Ana Flask uygulaması
├── rekognition_service.py → AWS Rekognition API çağrıları
├── s3_service.py          → AWS S3 dosya yükleme
├── templates/
│   ├── index.html         → Dosya yükleme sayfası
│   └── result.html        → Analiz sonuçları sayfası
├── requirements.txt       → Python bağımlılıkları
└── .env                   → AWS kimlik bilgileri (gizli)
```

---

## 3. AWS Servisleri Kurulumu

### 3.1 Amazon S3 Bucket Oluşturma

Yüklenen dosyaları depolamak için S3 bucket oluşturuldu:
- **Bucket Adı:** `proje6-rekognition-320042237584`
- **Bölge:** `eu-central-1` (Frankfurt)
- **Erişim:** Public read izni bucket policy ile verildi

**Bucket Policy:**
```json
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Principal": "*",
    "Action": "s3:GetObject",
    "Resource": "arn:aws:s3:::proje6-rekognition-320042237584/*"
  }]
}
```

### 3.2 IAM Kullanıcı İzinleri

Flask uygulamasının AWS servislerine erişebilmesi için IAM kullanıcısına aşağıdaki politikalar eklendi:
- ✅ `AmazonS3FullAccess`
- ✅ `AmazonRekognitionFullAccess`

### 3.3 Ortam Değişkenleri (.env)

```
AWS_ACCESS_KEY_ID=AKIAUVBAA72ICWFN7LOC
AWS_SECRET_ACCESS_KEY=********************
AWS_REGION=eu-central-1
S3_BUCKET_NAME=proje6-rekognition-320042237584
```

---

## 4. Uygulama Kodunun Açıklaması

### 4.1 `app.py` — Ana Flask Sunucusu

Ana web sunucusudur. Kullanıcıdan gelen dosyayı alır, S3'e yükler ve Rekognition ile analiz eder.

```python
@app.route("/analyze", methods=["POST"])
def analyze():
    file = request.files["file"]
    s3_key, s3_url = upload_to_s3(file, unique_filename)   # S3'e yükle
    results["labels"] = detect_labels(bucket_name, s3_key) # Nesne tanı
    results["faces"]  = detect_faces(bucket_name, s3_key)  # Yüz analiz
    results["text"]   = detect_text(bucket_name, s3_key)   # Metin oku
    return render_template("result.html", results=results)
```

### 4.2 `rekognition_service.py` — Yapay Zeka İşlemleri

AWS Rekognition API'sine bağlanan servis modülüdür. Üç temel fonksiyon içerir:

**`detect_labels()`** — Nesne Tanıma:
```python
response = rekognition_client.detect_labels(
    Image={"S3Object": {"Bucket": bucket_name, "Name": s3_key}},
    MaxLabels=15,
    MinConfidence=70
)
# Sonuç: [{"name": "Person", "confidence": 99.5}, ...]
```

**`detect_faces()`** — Yüz Analizi:
```python
response = rekognition_client.detect_faces(
    Image={"S3Object": {"Bucket": bucket_name, "Name": s3_key}},
    Attributes=["ALL"]  # Tüm özellikler: yaş, duygu, gözlük...
)
```

**`detect_text()`** — Metin Tespiti:
```python
response = rekognition_client.detect_text(
    Image={"S3Object": {"Bucket": bucket_name, "Name": s3_key}}
)
```

### 4.3 `s3_service.py` — Dosya Depolama

Kullanıcının yüklediği dosyayı AWS S3'e aktarır:
```python
s3_client.upload_fileobj(
    file_obj,
    BUCKET_NAME,
    f"uploads/{filename}"
)
```

---

## 5. Test Sonuçları

Sistem üç farklı görsel ile test edilmiş ve başarılı sonuçlar alınmıştır.

### Test 1 — Bitki Fotoğrafı (Nesne Tanıma)

*[BURAYA BİTKİ ANALİZİ EKRAN GÖRÜNTÜsÜ EKLENECEKTİR]*

| Tespit Edilen Nesne | Güven Oranı |
|--------------------|------------|
| Plant (Bitki) | %100 |
| Potted Plant (Saksı Bitkisi) | %100 |
| Tree (Ağaç) | %98.3 |
| Jar (Kavanoz) | %97 |
| Flower (Çiçek) | %96.5 |
| Flower Arrangement | %96.5 |

**Sonuç:** Bitki fotoğrafında hiç yüz ya da metin bulunmadığından bu bölümler boş döndü. Nesne tanıma ise %100 güvenle doğru çalıştı.

---

### Test 2 — İnsan Fotoğrafı (Yüz Analizi)

*[BURAYA YÜZ ANALİZİ EKRAN GÖRÜNTÜsÜ EKLENECEKTİR]*

**Nesne Tanıma:** 15 nesne tespit edildi (Person, Face, Hand, Clothing, Glasses, Monitor, Screen...)

**Yüz Analizi — 2 Yüz Tespit Edildi:**

| Özellik | 1. Yüz | 2. Yüz |
|---------|--------|--------|
| Güven | %100 | %100 |
| Yaş Aralığı | 23-29 yaş | 18-22 yaş |
| Cinsiyet | Kadın (%96.4) | Erkek (%100) |
| Duygu | 😮 Şaşkın (%86.6) | 😐 Sakin (%99.9) |
| Gözlük | Gözlük var 👓 | Gözlük yok |
| Gülümseme | Gülümsemiyor | Gülümsemiyor |

**Sonuç:** İki farklı kişiyi aynı fotoğrafta birbirinden ayırt ederek, yaş, cinsiyet ve duygu durumlarını %100 güvenle tespit etti.

---

### Test 3 — Ördek Fotoğrafı (Detaylı Nesne Tanıma)

*[BURAYA ÖRDEK ANALİZİ EKRAN GÖRÜNTÜsÜ EKLENECEKTİR]*

| Tespit Edilen Nesne | Güven Oranı |
|--------------------|------------|
| Teal (Yeşil Başlı Ördek) | %99.9 |
| Animal (Hayvan) | %98.9 |
| Anseriformes (Kuş Familyası) | %98.9 |
| Bird (Kuş) | %98.9 |
| Waterfowl (Su Kuşu) | %98.9 |
| Duck (Ördek) | %94.9 |
| Mallard (Yeşil Başlı Ördek türü) | %94.9 |

**Sonuç:** Rekognition sadece "ördek" demekle kalmadı; kuşun tam biyolojik sınıfını (Anseriformes) ve türünü (Mallard) tespit etti.

---

### Test 4 — Yazılı Belge (Metin Tespiti / OCR)

*[BURAYA METİN TESPİTİ EKRAN GÖRÜNTÜsÜ EKLENECEKTİR]*

Bir belge/ekran görüntüsü yüklendiğinde Rekognition 30'dan fazla metin satırını başarıyla okudu. Tespit edilen metinler arasında:
- "1. Web Exploitation"
- "Attacking web apps, APIs, and services"
- "SQL Injection (SQLi)"
- "Cross Site Scripting (XSS)"
- HTTP adresleri ve komut satırı örnekleri

**Sonuç:** OCR özelliği yazılı belgeler, ekran görüntüleri, tabelalar ve plakalardaki metinleri yüksek doğrulukla okuyabilmektedir.

---

## 6. Karşılaşılan Hatalar ve Çözümleri

| Hata | Sebep | Çözüm |
|------|-------|-------|
| `AccessDenied: s3:PutObject` | IAM kullanıcısının S3 yazma izni yoktu | IAM → `AmazonS3FullAccess` politikası eklendi |
| `AccessDenied: Rekognition` | Rekognition izni eksikti | IAM → `AmazonRekognitionFullAccess` eklendi |
| Bucket Policy hatası | Görseller public değildi | Bucket Policy ile `s3:GetObject` izni verildi |

---

## 7. Sonuç ve Değerlendirme

Bu proje ile:

1. **AWS Rekognition** servisinin nesne tanıma, yüz analizi ve OCR yetenekleri başarıyla uygulandı.
2. **AWS S3** ile bulut tabanlı dosya depolama entegrasyonu gerçekleştirildi.
3. **Flask (Python)** ile tam işlevsel bir web uygulaması geliştirildi.
4. IAM üzerinden güvenli kimlik doğrulama ve yetkilendirme yönetimi yapıldı.

Proje, makine öğrenmesi veya yapay zeka modeli eğitmeye gerek kalmadan, AWS'nin hazır **AI/ML servislerini** kullanarak güçlü görüntü işleme çözümleri üretilebileceğini göstermiştir. Bu yaklaşım, hem geliştirme süresini önemli ölçüde kısaltmakta hem de sınırsız ölçeklenebilirlik sağlamaktadır.
