# PROJE-4: E-Ticaret Uygulaması (Auto Scaling + Load Balancing)

**Öğrenci:** Arife Ebrar Üstüner | **Ders:** Bulut Bilişim (3522) | **Tarih:** Mayıs 2026

## Proje Hakkında

Bu proje, AWS üzerinde yüksek erişilebilirliğe sahip bir e-ticaret web uygulamasıdır.
**Application Load Balancer (ALB)** gelen trafiği sunucular arasında dağıtır.
**Auto Scaling** CPU kullanımı yükseldiğinde otomatik olarak yeni sunucular başlatır.

**Canlı URL:** `http://<ALB_DNS>/` (AWS'de kurulduktan sonra güncellenecek)

## Dosya Yapısı

```
PROJE-4/
├── app.py              → Flask web uygulaması (e-ticaret + /stress + /health endpoint'leri)
├── templates/
│   ├── index.html      → Ana sayfa (ürün listesi + sunucu bilgisi)
│   └── cart.html       → Sepet sayfası
├── requirements.txt    → Python bağımlılıkları
├── userdata.sh         → EC2 başlarken otomatik çalışan kurulum scripti
├── stress_test.py      → Auto Scaling testi için CPU yük aracı
└── README.md
```

## AWS Kurulum Adımları

> Kodlar hazır. Aşağıdaki AWS adımları sırasıyla uygulanacak.

### Adım 1: Launch Template Oluştur

EC2 → Launch Templates → Create launch template

| Alan | Değer |
|---|---|
| Template Name | `cloudshop-template` |
| AMI | Amazon Linux 2023 |
| Instance Type | `t2.micro` (Free Tier) |
| Key Pair | Mevcut key pair seç |
| Security Group | HTTP (80) ve SSH (22) açık |
| User Data | `userdata.sh` içeriğini yapıştır |

### Adım 2: Target Group Oluştur

EC2 → Target Groups → Create target group

| Alan | Değer |
|---|---|
| Target Type | Instances |
| Name | `cloudshop-targets` |
| Protocol / Port | HTTP / 80 |
| Health Check Path | `/health` |

### Adım 3: Application Load Balancer Oluştur

EC2 → Load Balancers → Create → Application Load Balancer

| Alan | Değer |
|---|---|
| Name | `cloudshop-alb` |
| Scheme | Internet-facing |
| Listener | HTTP:80 → cloudshop-targets |
| Availability Zones | En az 2 AZ seç |

### Adım 4: Auto Scaling Group Oluştur

EC2 → Auto Scaling Groups → Create

| Alan | Değer |
|---|---|
| Name | `cloudshop-asg` |
| Launch Template | `cloudshop-template` |
| Min / Max / Desired | 1 / 4 / 1 |
| Load Balancer | cloudshop-alb |
| Scaling Policy | Target Tracking — CPU %50 |

### Adım 5: Test

```bash
# 1. Uygulamanın çalıştığını doğrula
curl http://<ALB_DNS>/health

# 2. Hangi sunucuya bağlandığını gör
curl http://<ALB_DNS>/server-info

# 3. Auto Scaling stres testi başlat
python stress_test.py --url http://<ALB_DNS> --workers 20 --duration 300
```

## API Endpoint'leri

| Method | URL | Açıklama |
|---|---|---|
| GET | `/` | Ana sayfa — ürün listeleme |
| GET | `/cart` | Sepet sayfası |
| POST | `/add_to_cart/<id>` | Ürünü sepete ekle |
| POST | `/remove_from_cart/<id>` | Ürünü sepetten çıkar |
| GET | `/health` | Load Balancer sağlık kontrolü |
| GET | `/server-info` | Sunucu bilgisi (JSON) |
| GET | `/stress?duration=30` | CPU stres testi — Auto Scaling tetikler |

## Yerel Geliştirme

```bash
pip install -r requirements.txt
python app.py
# Uygulama: http://localhost:80
```
