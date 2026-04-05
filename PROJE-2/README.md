# 🌍 Akıllı Şehir Hava Kalitesi İzleme Sistemi (IoT Simülasyonu)

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=flat-square&logo=python)
![AWS](https://img.shields.io/badge/AWS-Cloud-FF9900?style=flat-square&logo=amazon-aws)
![GitHub](https://img.shields.io/badge/GitHub-Repository-181717?style=flat-square&logo=github)
![Status](https://img.shields.io/badge/Status-In%20Development-yellow?style=flat-square)

---

## 📋 İçindekiler

- [Proje Özeti](#proje-özeti)
- [Teknoloji Stack'i](#teknoloji-stacki)
- [Sistem Mimarisi](#sistem-mimarisi)
- [Kurulum](#kurulum)
- [Kullanım](#kullanım)
- [Proje Yapısı](#proje-yapısı)
- [Geliştirme Planı](#geliştirme-planı)
- [Başarı Kriterleri](#başarı-kriterleri)
- [Lisans](#lisans)

---

## 🎯 Proje Özeti

Bu proje, gerçek zamanlı bir **IoT veri akış sistemi** simüle etmektedir. Amaç, şehir genelindeki sensörlerden gelen hava kalitesi verilerinin (Sıcaklık, PM2.5, CO2) anlık olarak toplanmasını, bulut ortamında serverless mimarisi ile işlenmesini ve analiz edilmek üzere depolanmasıdır.

### 🎓 Akademik Bağlam
- **Hocanın İsteği**: Gün gün yükleme (Daily Development)
- **Hedef**: Profesyonel bir IoT sisteminin gerçek bulut teknolojileri ile uygulanması
- **Süre**: Tahminen 5 gün (20-25 saat)

---

## 🛠️ Teknoloji Stack'i

| Bileşen | Teknoloji | Açıklama |
|---------|-----------|----------|
| **Backend** | Python 3.9+ | Sensör simülasyon ve veri işleme |
| **Streaming** | AWS Kinesis Data Streams | Gerçek zamanlı veri akışı |
| **Processing** | AWS Lambda | Sunucusuz veri işleme |
| **Database** | AWS DynamoDB | NoSQL veritabanı |
| **SDK** | Boto3 | AWS SDK for Python |
| **Versiyon Kontrol** | Git & GitHub | Kod yönetimi |
| **Monitoring** | AWS CloudWatch | Log ve metrik izleme |

---

## 🏗️ Sistem Mimarisi

### Mimariye Genel Bakış

```
┌─────────────────┐      ┌──────────────────┐      ┌────────────────┐      ┌──────────────────┐
│   Sensör        │      │   Kinesis        │      │  Lambda        │      │  DynamoDB        │
│   Simülatörü    │ ───► │   Data Stream    │ ───► │  Function      │ ───► │  (NoSQL DB)      │
│   (Local PC)    │      │   (AWS)          │      │  (Python)      │      │  (AWS)           │
└─────────────────┘      └──────────────────┘      └────────────────┘      └──────────────────┘
       │                          │                        │                       │
       │                          │                        │                       │
  Veri Üretim              Veri Aktarım           Veri İşleme            Veri Depolama
```

### Veri Akışı Adımları

1. **Sensör Simülasyonu**: Yerel bilgisayarda çalışan Python script'i gerçek zamanlı hava kalitesi verisi üretir
2. **Kinesis Stream**: Üretilen veriler AWS Kinesis üzerindeki veri borusuna aktarılır
3. **Lambda Tetikleme**: Kinesis'e düşen her veri paketi otomatik olarak Lambda fonksiyonunu tetikler
4. **Veri İşleme**: Lambda fonksiyonu veriyi doğrular, işler ve formatlandırır
5. **DynamoDB Depolama**: İşlenen veriler zaman damgası ile DynamoDB'ye kaydedilir

### Bileşen Detayları

#### AWS Kinesis Data Stream
- **Stream Adı**: `AirQualityStream`
- **Shard Yapısı**: İhtiyaca göre ayarlanabilir (başlangıç: 1 shard)
- **Veri Formatı**: JSON

#### AWS Lambda Function
- **Fonksiyon Adı**: `ProcessAirQualityData`
- **Runtime**: Python 3.9+
- **Timeout**: 60 saniye
- **Memory**: 256 MB

#### AWS DynamoDB Table
- **Tablo Adı**: `AirQualityData`
- **Partition Key**: `timestamp` (Zaman damgası)
- **Sort Key**: `sensor_id` (Opsiyonel)
- **Attributes**:
  - `temperature`: Sıcaklık (°C)
  - `pm25`: PM2.5 (µg/m³)
  - `co2`: CO2 (ppm)
  - `location`: Sensör konumu
  - `sensor_id`: Sensör kimliği

---

## 💾 Kurulum

### Ön Koşullar

- Python 3.9+ yüklü olmalı
- AWS hesabı (Free Tier uygun)
- AWS CLI yapılandırılmış
- Git yüklü

### Adım 1: AWS Hizmetlerini Yapılandırma

#### Kinesis Stream Oluşturma
```bash
aws kinesis create-stream \
  --stream-name AirQualityStream \
  --shard-count 1
```

#### DynamoDB Tablosu Oluşturma
```bash
aws dynamodb create-table \
  --table-name AirQualityData \
  --attribute-definitions \
    AttributeName=timestamp,AttributeType=S \
    AttributeName=sensor_id,AttributeType=S \
  --key-schema \
    AttributeName=timestamp,KeyType=HASH \
    AttributeName=sensor_id,KeyType=RANGE \
  --billing-mode PAY_PER_REQUEST
```

### Adım 2: Projeyi Klonlama

```bash
git clone https://github.com/[kullanici]/Bulut-proje.git
cd Bulut-proje/PROJE-2
```

### Adım 3: Python Bağımlılıklarını Yükleme

```bash
pip install -r requirements.txt
```

**requirements.txt** içeriği:
```
boto3==1.26.137
botocore==1.29.137
python-dotenv==1.0.0
```

---

## 🚀 Kullanım

### Sensör Simülatörünü Başlatma

```bash
python sensor_simulator.py
```

**Çıktı Örneği:**
```
[2026-04-05 10:30:45] Sensör simülatörü başladı...
[2026-04-05 10:30:46] Veri gönderiliyor: {"timestamp": "2026-04-05T10:30:46", "sensor_id": "SENSOR_001", "temperature": 22.5, "pm25": 45, "co2": 650}
[2026-04-05 10:30:47] ✓ Veriler Kinesis'e başarıyla gönderildi
[2026-04-05 10:30:48] Veri gönderiliyor: {"timestamp": "2026-04-05T10:30:48", "sensor_id": "SENSOR_002", ...}
```

### CloudWatch'ta Logları İzleme

```bash
aws logs tail /aws/lambda/ProcessAirQualityData --follow
```

### DynamoDB'deki Verileri Sorgulamak

```bash
aws dynamodb scan \
  --table-name AirQualityData \
  --limit 10
```

---

## 📁 Proje Yapısı

```
PROJE-2/
├── README.md                      # Bu dosya
├── plan.txt                        # Detaylı proje planı
├── requirements.txt               # Python bağımlılıkları
├── .env.example                   # Environment variables şablonu
│
├── src/
│   ├── sensor_simulator.py        # IoT sensör simülatörü
│   ├── lambda_handler.py          # AWS Lambda fonksiyonu
│   ├── utils/
│   │   ├── validators.py          # Veri doğrulama
│   │   └── config.py              # Konfigürasyon
│   └── constants.py               # Sabitler
│
├── aws/
│   ├── kinesis-setup.sh           # Kinesis kurulum scripti
│   ├── dynamodb-setup.sh          # DynamoDB kurulum scripti
│   └── iam-policy.json            # IAM policy tanımı
│
├── docs/
│   ├── ARCHITECTURE.md            # Detaylı mimari dokümantasyon
│   ├── SETUP.md                   # Adım adım kurulum rehberi
│   ├── API.md                     # Veri formatı ve API
│   └── DAILY_REPORTS.md           # Günlük ilerleme raporları
│
├── tests/
│   ├── test_sensor_data.py        # Sensör verisi testleri
│   ├── test_lambda_handler.py     # Lambda fonksiyonu testleri
│   └── test_dynamodb.py           # DynamoDB testleri
│
└── .gitignore                     # Git ignore dosyası
```

---

## ✅ Başarı Kriterleri

### Sistem Fonksiyonelliği
- ✓ Sensör simülatörü düzenli olarak veri gönderebilmeli
- ✓ Kinesis stream'i veriyi alıp aktarabilmeli
- ✓ Lambda fonksiyonu başarıyla tetiklenip veriyi işleyebilmeli
- ✓ DynamoDB'de veriler doğru şekilde saklanabilmeli

### Kod Kalitesi
- ✓ Python kodu PEP8 standartlarına uymalı
- ✓ Hata işleme mekanizmaları olmalı
- ✓ Kodlar yorum satırları ile açıklanmalı
- ✓ Unit testler yazılmış olmalı

### Dokümantasyon
- ✓ README.md tam ve güncel olmalı
- ✓ Kurulum adımları net olmalı
- ✓ API detayları documante edilmiş olmalı
- ✓ Günlük rapor güncellenmiş olmalı

### Versiyon Kontrol
- ✓ Günlük commit'ler olmalı
- ✓ Commit mesajları açıklayıcı olmalı
- ✓ Branch yapısı düzgün olmalı (`main`, `develop`, `feature/*`)

### Demo ve Sunum
- ✓ Video minimum 10 dakika olmalı
- ✓ Canlı sistem gösterilmiş olmalı
- ✓ Teknik detaylar açıklanmış olmalı
- ✓ Link erişilebilir olmalı

---

## 🚨 Önemli Notlar

### Maliyet Yönetimi
- AWS Free Tier limitlerini göz önünde bulundurun
- Kinesis Shard sayısını minimal tutun
- DynamoDB Pay-Per-Request modunu kullanın

### Güvenlik
- IAM roller ve policies dikkatle yapılandırılmalı
- AWS credentials asla git'e commit etmeyin
- `.env` dosyasını `.gitignore`'a ekleyin

### Ölçeklenebilirlik
- Veri hacmi arttığında Lambda timeout süresi artırılabilir
- Kinesis shard sayısı ihtiyaca göre düşürülebilir/artırılabilir
- DynamoDB otomatik scaling ayarlanabilir

---

## 📚 Ek Kaynaklar

- [AWS Kinesis Documentation](https://docs.aws.amazon.com/kinesis/)
- [AWS Lambda Documentation](https://docs.aws.amazon.com/lambda/)
- [AWS DynamoDB Documentation](https://docs.aws.amazon.com/dynamodb/)
- [Boto3 Documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)
- [Python PEP8 Style Guide](https://www.python.org/dev/peps/pep-0008/)

---

## 🎉 Teşekkürler

---



