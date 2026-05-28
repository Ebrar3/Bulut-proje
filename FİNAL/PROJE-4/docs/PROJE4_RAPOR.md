# BULUT BİLİŞİM (3522) - PROJE 4 RAPORU

**Öğrenci:** Arife Ebrar Üstüner
**Öğrenci No:** 23291207
**Proje Konusu:** Yüksek Erişilebilirliğe Sahip E-Ticaret Uygulaması (AWS EC2 + ALB + Auto Scaling)

---

## 📌 Proje Bağlantıları
- **GitHub Repository:** [Proje 4 Kaynak Kodları](https://github.com/Ebrar3/Bulut-proje/tree/main/FİNAL/PROJE-4)
- **Proje Sunum Videosu:** [Google Drive Video Linki](https://drive.google.com/drive/folders/1Kwnhe32qCb3DiB_Idqw9Zr1v7ztcqUbO?usp=drive_link)

---

## 1. Projenin Amacı ve Mimari

Bu projenin temel amacı; ani trafik artışlarına (örneğin indirim dönemlerindeki yoğunluğa) dayanabilen, kendi kendini otomatik olarak ölçekleyebilen (**Auto Scaling**) ve gelen kullanıcı isteklerini sağlıklı sunuculara eşit şekilde dağıtan (**Load Balancer**) bir bulut mimarisi kurmaktır.

Sistem, Python (Flask) ile yazılmış bir E-Ticaret uygulaması üzerinde çalışmaktadır. 

### Mimari Bileşenler:
1. **Launch Template:** Yeni açılacak EC2 sunucularının şablonunu belirler. Yazdığımız `userdata.sh` scripti sayesinde yeni bir sunucu açılır açılmaz GitHub'dan kodları çeker, gereksinimleri kurar ve web sitesini otomatik başlatır.
2. **Application Load Balancer (ALB):** Kullanıcı trafiğini karşılayan ana giriş noktasıdır. Trafiği arkada çalışan EC2 sunucularına dağıtır.
3. **Auto Scaling Group (ASG):** Sunucuların CPU kullanımı %50'yi aştığında otomatik olarak yeni sunucular başlatır (Scale Out). Trafik azaldığında ise fazla sunucuları kapatarak maliyet tasarrufu sağlar (Scale In).

---

## 2. Geliştirme Süreci ve Yapılan Ayarlar

### Adım Adım Kurulum:
- **Security Group (Güvenlik Grubu):** Dışarıdan web trafiğine izin vermek için HTTP (80) ve SSH (22) portları açıldı.
- **Flask Uygulamasının Kodlanması:** Sepete ürün ekleme özellikleri olan, modern arayüzlü bir E-Ticaret sitesi kodlandı. Uygulama, hangi EC2 sunucusunda çalıştığını göstermek üzere AWS Metadata servisinden kendi *Instance ID* bilgisini alacak şekilde ayarlandı.
- **Load Balancer & Target Group:** Hedef grubu oluşturularak ALB'ye bağlandı. ALB'nin, sunucuların sağlıklı çalışıp çalışmadığını anlaması için `/health` endpoint'i tanımlandı.

### Stres Testi (Yük Testi) ve Ölçeklendirme:
Auto Scaling'in gerçekten çalıştığını kanıtlamak için özel bir `stress_test.py` aracı kodlandı. Bu araç, ALB adresine çok sayıda eşzamanlı istek göndererek `/stress` endpoint'ini tetikledi ve CPU kullanımını anlık olarak %100'e çıkardı. 
- **Sonuç:** AWS CloudWatch metrikleri üzerinden CPU artışı tespit edildi ve Auto Scaling Group yeni bir EC2 sunucusu başlatarak sistemi rahatlattı. Yük dağıtıcının çalıştığı, web sayfasının altındaki *Instance ID* kısmının farklılaşmasıyla gözlemlendi.

---

## 3. Karşılaşılan Hatalar ve Çözümleri

Proje geliştirme sürecinde aşağıdaki hata durumları simüle edilmiş/deneyimlenmiş ve çözülmüştür:

**Hata 1: 503 Service Temporarily Unavailable**
- **Durum:** Sunucuyu Target Group'tan manuel olarak çıkartınca (Deregister), ALB trafiği yönlendirecek sağlıklı sunucu bulamadı.
- **Çözüm:** EC2 Console üzerinden `Target Groups -> Register targets` adımları izlenerek çalışan EC2 instance'ı tekrar Load Balancer hedeflerine eklendi. "Pending" durumundan "Healthy" durumuna geçmesi beklenerek sorun çözüldü.

**Hata 2: Auto Scaling Döngüsü (Continuous Terminate/Launch)**
- **Durum:** UserData scriptindeki bir dizin yolu (Türkçe karakter) hatası yüzünden uygulama `Target Group` sağlık kontrolünden geçemediği için ASG sürekli sunucuları kapatıp yenisini açıyordu.
- **Çözüm:** `userdata.sh` scripti içine hata yakalama (`set -e`) ve loglama mekanizması eklendi. Türkçe karakter dizin adı `find` komutu ile dinamik bulunarak düzeltildi ve Auto Scaling Group "Instance Refresh" yapılarak yeni şablonla güncellendi.

**Hata 3: Stres Testinde 502 Bad Gateway**
- **Durum:** Stres testi esnasında çok fazla istek alan ilk sunucunun kapasitesi tam dolduğunda anlık 502 hataları döndürdü.
- **Çözüm:** Bu bir hata değil, **beklenen bir durumdu**. Hemen ardından Auto Scaling devreye girip ikinci sunucuyu ayağa kaldırdığında, Load Balancer trafiği dağıtmaya başladı ve sistem normal seyrine döndü.

---

## 4. Sonuç
Bu proje ile modern bulut sistemlerinde **Yüksek Erişilebilirlik (High Availability)** kavramı uygulamalı olarak gerçekleştirildi. Manuel müdahaleye gerek kalmadan sistemin yüke göre kendi kendini optimize ettiği başarılı bir şekilde kanıtlandı.
