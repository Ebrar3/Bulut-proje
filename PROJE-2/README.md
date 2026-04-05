PROJE 2: AKILLI ŞEHİR HAVA KALİTESİ İZLEME SİSTEMİ (IoT Simülasyonu)
═════════════════════════════════════════════════════════════════════

1. PROJE ÖZETİ
──────────────
Bu çalışma kapsamında, gerçek zamanlı bir IoT veri akış sistemi simüle edilecektir. Proje, şehir 
genelindeki sensörlerden gelen hava kalitesi verilerinin (Sıcaklık, PM2.5, CO2) anlık olarak 
toplanmasını, bulut ortamında işlenmesini ve analiz edilmek üzere depolanmasını amaçlamaktadır.


2. KULLANILACAK TEKNOLOJİLER
──────────────────────────────
• Backend Dili: Python (Veri üretimi ve Lambda işleme için)
• Veri Akış Katmanı (Streaming): AWS Kinesis Data Streams
• İşlem Katmanı (Serverless Computing): AWS Lambda
• Veritabanı Katmanı (NoSQL): AWS DynamoDB
• Versiyon Kontrol: Git & GitHub
• SDK: Boto3 (AWS SDK for Python)


3. SİSTEM MİMARİSİ (Mimarinin Tanımı)
──────────────────────────────────────
Sistem mimarisi "Serverless" (Sunucusuz) prensiplerine dayanmaktadır:

Veri Akışı:
1. Yerel bilgisayarda çalışan Python tabanlı sensör simülatörü, gerçek zamanlı hava kalitesi 
   verisi üretir.
2. Üretilen veriler AWS Kinesis üzerindeki veri borusuna (stream) aktarılır.
3. Kinesis'e düşen her veri paketi, bir tetikleyici (trigger) vasıtasıyla AWS Lambda 
   fonksiyonunu ayağa kaldırır.
4. Lambda fonksiyonu gelen veriyi işleyerek (ayrıştırma ve analiz) nihai sonuçları 
   AWS DynamoDB NoSQL tablosuna kalıcı olarak kaydeder.

Mimari Bileşenler:
┌─────────────┐      ┌──────────────┐      ┌────────────┐      ┌──────────────┐
│   Sensör    │ ──→  │   Kinesis    │ ──→  │  Lambda    │ ──→  │  DynamoDB    │
│ Simülatörü  │      │Data Streams  │      │ (Python)   │      │  (NoSQL DB)  │
└─────────────┘      └──────────────┘      └────────────┘      └──────────────┘
  (Local PC)         (AWS Streaming)      (Serverless)        (Data Storage)


4. UYGULAMA VE TESLİMAT PLANI
──────────────────────────────

AŞAMA 1: BULUT ALTYAPISININ HAZIRLANMASI (AWS Setup)
─────────────────────────────────────────────────────
Yapılacaklar:
□ Kinesis Kurulumu: Gerçek zamanlı veri akışını yönetecek "Data Stream" kanalı oluşturulacaktır.
  - Stream Adı: "AirQualityStream"
  - Shard sayısı ve kapasitesi tanımlanacaktır
  
□ DynamoDB Kurulumu: Gelen verilerin zaman damgalı (timestamp) olarak saklanacağı NoSQL 
  tablosu tasarlanacaktır.
  - Tablo Adı: "AirQualityData"
  - Primary Key: timestamp (Partition Key)
  - Attributes: sensor_id, temperature, pm25, co2, location
  - TTL: Ggezli verilerin otomatik silinmesi için ayarlanacaktır

Başarı Kriterleri:
✓ AWS Kinesis stream'i oluşturulmuş ve aktif olmalı
✓ DynamoDB tablosu oluşturulmuş ve okuma/yazma kapasitesi ayarlanmış olmalı


AŞAMA 2: İŞLEM MERKEZİ (Lambda) GELİŞTİRME
──────────────────────────────────────────
Yapılacaklar:
□ Kinesis akışından gelen ham JSON verisini okuyacak bir Python script'i hazırlanacaktır.
  - Lambda function adı: "ProcessAirQualityData"
  - Runtime: Python 3.9+
  
□ Veri doğrulama ve işleme:
  - JSON yapısı kontrol edilecektir
  - Sıcaklık, PM2.5, CO2 değerlerinin aralık kontrolü yapılacaktır
  - Geçersiz veriler log'lanacaktır
  
□ DynamoDB yazma işlemi:
  - Boto3 kütüphanesi kullanılarak veriler DynamoDB'ye yazılacaktır
  - Hata işleme ve retry mekanizması uygulanacaktır
  - CloudWatch loglaması ayarlanacaktır

Başarı Kriterleri:
✓ Lambda fonksiyonu Kinesis tetikleyicisi ile çalışmalı
✓ Gelen veriler başarıyla DynamoDB'ye yazılmalı
✓ CloudWatch'ta loglar görülebilmeli


AŞAMA 3: SENSÖR SİMÜLASYONU (IoT Producer)
───────────────────────────────────────────
Yapılacaklar:
□ Python tabanlı sensör simülatörü geliştirilecektir
  - Dosya adı: "sensor_simulator.py"
  - Gerçek sensör donanımı yerine rastgele/simüle edilmiş veri üretecektir
  
□ Veri Özellikleri:
  - Sıcaklık: 15-35°C aralığında
  - PM2.5: 0-500 µg/m³ aralığında
  - CO2: 400-1200 ppm aralığında
  - Sensor ID: Farklı şehir lokasyonlarını temsil edecek
  
□ AWS SDK (Boto3) Entegrasyonu:
  - Boto3 kütüphanesi ile verileri Kinesis'e aktarma
  - Başarı/hata mesajları ekranda gösterilecektir
  - Veri gönderme hızı: 1-2 saniye aralıkları

Başarı Kriterleri:
✓ Sensör simülatörü çalışmalı ve Kinesis'e veri göndermeli
✓ Her veri paketi başarıyla Kinesis'e ulaşmalı
✓ Hatalar düzgün ele alınmalı


AŞAMA 4: DOKÜMANTASYON VE GİT YÖNETİMİ
────────────────────────────────────────
Yapılacaklar:
□ Hocanın belirttiği "günlük güncelleme" kuralına uygun olarak:
  - Her geliştirme adımı Git'e commit edilecektir
  - Günlük ilerleme raporu güncellenecektir
  - README.md dosyası devamlı bilgilendirilecektir
  
□ Git Yapısı:
  - main branch: Son stabil versiyon
  - develop branch: Geliştirme dalı
  - feature/* branches: Her özellik için ayrı dal
  
□ Dokümantasyon:
  - setup.md: Kurulum adımları
  - architecture.md: Sistem mimarisi detayları
  - api.md: Veri formatları ve API detayları
  - daily_report.md: Günlük ilerleme raporları

Commit Tarihleri (Örnek):
  Gün 1: AWS Kinesis ve DynamoDB kurulumu
  Gün 2: Lambda fonksiyonu geliştirme
  Gün 3: Sensör simülatörü kodlaması
  Gün 4: Entegrasyon ve testler
  Gün 5: Dokümantasyon ve Demo hazırlığı

Başarı Kriterleri:
✓ Tüm kodlar GitHub'a push edilmiş olmalı
✓ Her commit mesajı açıklayıcı olmalı
✓ README.md güncel olmalı


AŞAMA 5: VİDEO DEMO VE NİHAİ TESLİM
──────────────────────────────────────
Yapılacaklar:
□ Teknik video çekilecektir (Minimum 10 dakika)
  - Sensör simülatörü başlatılması
  - Kinesis'e gelen verilerin izlenmesi
  - Lambda fonksiyonu loglarının gösterilmesi
  - DynamoDB'deki saklanan verilerin gösterilmesi
  
□ Video içeriği:
  - Açılış: Sistem mimarisi ve açıklaması (1-2 dakika)
  - Canlı Demo: Sistem çalışması (6-8 dakika)
  - Sonuç: İstatistikler ve performans (1-2 dakika)
  
□ Teslim Platformu:
  - YouTube, Vimeo veya benzeri "tıkla izle" platformu
  - İzin gerektirmeyen, paylaşılabilir link
  
□ Proje Sunumu:
  - Kod kaynak linki (GitHub)
  - Sistem mimarisi diagram'ları
  - Performans metrikleri

Başarı Kriterleri:
✓ Video en az 10 dakika olmalı
✓ Sistem canlı çalışırken görülmeli
✓ Tüm bileşenler tanıtılmış olmalı
✓ Link erişilebilir olmalı


5. ZAMAN ÇIZELGESI (Tahmini)
─────────────────────────────
Gün 1: AWS Setup (Kinesis + DynamoDB)        [4-6 saat]
Gün 2: Lambda Fonksiyonu Geliştirme          [4-6 saat]
Gün 3: Sensör Simülatörü Kodlaması           [3-4 saat]
Gün 4: Entegrasyon ve Testler                [4-5 saat]
Gün 5: Dokümantasyon ve Video Hazırlığı      [3-4 saat]
────────────────────────────────────────────────────
Toplam Tahmini Süre: 20-25 saat


6. BAŞARIY KRİTERLERİ (Genel)
──────────────────────────────
■ Sistem Fonksiyonelliği:
  ✓ Sensör simülatörü düzenli olarak veri gönderebilmeli
  ✓ Kinesis stream'i veriyi alıp aktarabilmeli
  ✓ Lambda fonksiyonu başarıyla tetiklenip veriyi işleyebilmeli
  ✓ DynamoDB'de veriler doğru şekilde saklanabilmeli

■ Kod Kalitesi:
  ✓ Python kodu PEP8 standartlarına uymalı
  ✓ Hata işleme mekanizmaları olmalı
  ✓ Kodlar yorum satırları ile açıklanmalı

■ Dokümantasyon:
  ✓ README.md tam olmalı
  ✓ Kurulum adımları net olmalı
  ✓ API detayları documante edilmiş olmalı

■ Versiyon Kontrol:
  ✓ Günlük commit'ler olmalı
  ✓ Commit mesajları açıklayıcı olmalı
  ✓ Branch yapısı düzgün olmalı

■ Demo ve Sunum:
  ✓ Video minimum 10 dakika olmalı
  ✓ Canlı sistem gösterilmiş olmalı
  ✓ Teknik detaylar açıklanmış olmalı


7. RİSK FAKTÖRLERI VE MİTİGASYON
──────────────────────────────────
Risk 1: AWS Hesap Sınırlamaları
  Solüsyon: Free Tier limitlerini göz önünde bulundurmalı

Risk 2: Kinesis Hız Sorunları
  Solüsyon: Shard sayısı ihtiyaca göre artırılmalı

Risk 3: Lambda Timeout Sorunları
  Solüsyon: Timeout süresi uygun şekilde ayarlanmalı

Risk 4: DynamoDB Kapasitesi
  Solüsyon: On-demand billing moduna geçilebilir


18 NOTLAR VE UYARULAR
──────────────────────
• AWS kredileri takip edilmeli (Free Tier limitleri)
• Lambda fonksiyonları düzenli olarak test edilmeli
• CloudWatch logları hata ayıklama için kullanılmalı
• Güvenlik: IAM roller ve policies dikkatle yapılandırılmalı
• Ölçeklenebilirlik: Veri hacmi arttığında sistem genişletilebilir olmalı

