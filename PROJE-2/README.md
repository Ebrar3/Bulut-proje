Proje 2: Akıllı Şehir Hava Kalitesi İzleme Sistemi (IoT Simülasyonu)
1. Proje Özeti
Bu çalışma kapsamında, gerçek zamanlı bir IoT veri akış sistemi simüle edilecektir. Proje, şehir genelindeki sensörlerden gelen hava kalitesi verilerinin (Sıcaklık, PM2.5, CO2) anlık olarak toplanmasını, bulut ortamında işlenmesini ve analiz edilmek üzere depolanmasını amaçlamaktadır.
2. Kullanılacak Teknolojiler
Backend Dili: Python (Veri üretimi ve Lambda işleme için).
Veri Akış Katmanı (Streaming): AWS Kinesis Data Streams. 
İşlem Katmanı (Serverless Computing): AWS Lambda.
Veritabanı Katmanı (NoSQL): AWS DynamoDB.
Versiyon Kontrol: Git & GitHub.
3. Sistem Mimarisi (Mimarinin Tanımı)Sistem mimarisi "Serverless" (Sunucusuz) prensiplerine dayanmaktadır. Yerel bir bilgisayarda çalışan Python tabanlı sensör simülatörü, ürettiği gerçek zamanlı verileri AWS Kinesis üzerindeki veri borusuna aktarır. Kinesis'e düşen her veri paketi, bir tetikleyici (trigger) vasıtasıyla AWS Lambda fonksiyonunu ayağa kaldırır. Lambda fonksiyonu gelen veriyi işleyerek (ayrıştırma ve analiz) nihai sonuçları AWS DynamoDB NoSQL tablosuna kalıcı olarak kaydeder.
4. Uygulama ve Teslimat Planı
Aşama 1: Bulut Altyapısının Hazırlanması (AWS Setup)
Kinesis Kurulumu: Gerçek zamanlı veri akışını yönetecek "Data Stream" kanalı oluşturulacaktır.
DynamoDB Kurulumu: Gelen verilerin zaman damgalı (timestamp) olarak saklanacağı NoSQL tablosu tasarlanacaktır.
Aşama 2: İşlem Merkezi (Lambda) Geliştirme
Kinesis akışından gelen ham JSON verisini okuyacak bir Python script'i hazırlanacaktır.Verinin doğruluğu kontrol edildikten sonra boto3 kütüphanesi kullanılarak DynamoDB'ye yazma işlemi Lambda üzerinden gerçekleştirilecektir
Aşama 3: Sensör Simülasyonu (IoT Producer)
Gerçek bir sensör donanımı yerine internet ortamından veya rastgele üretimle hava kalitesi verilerini simüle eden bir Python kodu geliştirilecektir.Bu kod, AWS SDK (Boto3) aracılığıyla verileri anlık olarak Kinesis akışına pompalayacaktır.
Aşama 4: Dokümantasyon ve Git Yönetimi
Hocanın belirttiği "günlük güncelleme" kuralına uygun olarak rapor ve kodlar parça parça Git'e yüklenecektir.Her geliştirme adımı Git üzerinde dokümante edilecek ve süreç raporu sürekli güncellenecektir.
Aşama 5: Video Demo ve Nihai Teslim
Sistem çalışır hale getirildiğinde, verilerin Kinesis'ten DynamoDB'ye geçişini gösteren en az 10 dakikalık bir teknik video çekilecektir.Video, izin gerektirmeyen "tıkla izle" formatında bir platform üzerinden teslim edilecektir.