# PROJE-3: Akıllı Veri Analitiği ve Makine Öğrenmesi Uygulaması
## Bulut Bilişim Dersi (3522) — Proje Raporu

**Öğrenci:** Ebrar  
**Proje Adı:** Titanic Hayatta Kalma Tahmini — Makine Öğrenmesi ve Bulut Dağıtımı  
**Tarih:** Mayıs 2026  
**Platform:** AWS (S3, Lambda, API Gateway)  

---

## İÇİNDEKİLER

1. Proje Özeti
2. Kullanılan Teknolojiler
3. Sistem Mimarisi
4. Uygulama Süreci (Gün Gün)
   - Gün 1: Hazırlık ve Temel Kodlar
   - Gün 2: EDA, Model Eğitimi ve Yerel Test
   - Gün 3: AWS Dağıtımı ve Canlı Yayın
5. Makine Öğrenmesi Modeli
6. AWS Servisleri Açıklamaları
7. API Kullanımı
8. Sonuç ve Değerlendirme

---

## 1. PROJE ÖZETİ

Bu projede, Titanic gemisindeki yolcuların hayatta kalıp kalmayacağını tahmin eden
bir makine öğrenmesi modeli geliştirilmiş ve bu model AWS bulut platformuna dağıtılmıştır.

**Hedefler:**
- Gerçek bir veri seti üzerinde makine öğrenmesi modeli geliştirmek
- Modeli bir REST API'ye dönüştürmek
- API'yi AWS Lambda ile serverless (sunucusuz) olarak buluta taşımak
- Web arayüzü ile son kullanıcıya sunmak

**Sonuç:** Kullanıcı bir Titanic yolcusunun bilgilerini girdiğinde
(sınıf, cinsiyet, yaş, ücret vb.), sistem %80.3 doğrulukla
hayatta kalıp kalmayacağını tahmin etmektedir.

**Canlı Web Sitesi:**
http://bulut-proje-titanic-ml-titanic-ebrar.s3-website.eu-central-1.amazonaws.com/

**API Endpoint:**
https://l7om4ms6bi.execute-api.eu-central-1.amazonaws.com/default/titanic-predict

---

## 2. KULLANILAN TEKNOLOJİLER

| Kategori | Teknoloji | Amaç |
|----------|-----------|------|
| Backend Dili | Python 3.13 | Model eğitimi ve API |
| ML Kütüphanesi | Scikit-learn | Makine öğrenmesi |
| Veri İşleme | Pandas, NumPy | Veri manipülasyonu |
| Görselleştirme | Matplotlib, Seaborn | Grafik oluşturma |
| Yerel API | Flask | Geliştirme ortamı testi |
| API Test | Postman | API endpoint testi |
| Bulut (Depolama) | AWS S3 | Model ve web sitesi barındırma |
| Bulut (Hesaplama) | AWS Lambda | Serverless fonksiyon |
| Bulut (API) | AWS API Gateway | HTTP endpoint |
| Versiyon Kontrol | Git & GitHub | Kod yönetimi |

---

## 3. SİSTEM MİMARİSİ

```
┌─────────────────────────────────────────────────────────────┐
│                    KULLANICI TARAYICISI                     │
│   http://bulut-proje-titanic-ml...amazonaws.com             │
└────────────────────────┬────────────────────────────────────┘
                         │ 1. Web sayfasını yükle
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                  AWS S3 (Static Website)                    │
│                    index.html                               │
│       (Kullanıcı arayüzü — form ve sonuç ekranı)           │
└────────────────────────┬────────────────────────────────────┘
                         │ 2. POST /predict (JSON veri)
                         ▼
┌─────────────────────────────────────────────────────────────┐
│               AWS API GATEWAY (REST API)                    │
│    l7om4ms6bi.execute-api.eu-central-1.amazonaws.com        │
│          (Dışarıdan gelen isteklerin kapısı)                │
└────────────────────────┬────────────────────────────────────┘
                         │ 3. Lambda'yı tetikle
                         ▼
┌─────────────────────────────────────────────────────────────┐
│           AWS LAMBDA (titanic-predict fonksiyonu)           │
│              Python 3.13 | 1024 MB RAM | 60 sn              │
│                                                             │
│   Adım 1: S3'ten titanic_model.pkl dosyasını indir         │
│   Adım 2: Gelen yolcu verisini işle                        │
│   Adım 3: model.predict() ile tahmin yap                   │
│   Adım 4: JSON sonucu döndür                               │
└────────────────────────┬────────────────────────────────────┘
                         │ 4. Model dosyasını oku
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                  AWS S3 (Dosya Deposu)                      │
│         titanic_model.pkl (132 KB) — eğitilmiş model       │
└─────────────────────────────────────────────────────────────┘
```

**[GÖRSEL-1: Sistem mimarisi diyagramı veya AWS Console genel görünümü]**

---

## 4. UYGULAMA SÜRECİ

---

### GÜN 1 — 24 Mayıs 2026: Hazırlık ve Temel Kodlar

#### 4.1.1 Proje Klasör Yapısının Oluşturulması

Proje başlangıcında, kodların düzenli tutulması için aşağıdaki klasör yapısı oluşturulmuştur:

```
FİNAL/
├── PROJE-3/
│   ├── data/        → Ham veri ve grafikler
│   ├── model/       → ML kodu ve eğitilmiş model
│   ├── api/         → Flask ve Lambda kodları
│   ├── frontend/    → Web arayüzü
│   └── docs/        → Rapor
├── PROJE-4/         → (İlerleyen haftalarda)
└── PROJE-6/         → (İlerleyen haftalarda)
```

Bu yapı, her bileşenin (veri, model, API, arayüz) birbirinden ayrı tutulmasını
sağlamaktadır. Profesyonel yazılım projelerinde bileşenlerin birbirinden bağımsız
olması, bakım ve hata ayıklamayı kolaylaştırmaktadır.

**[GÖRSEL-2: GitHub repository ana sayfası — klasör yapısı]**

#### 4.1.2 Gereksinim Dosyası (requirements.txt)

Python kütüphaneleri `requirements.txt` dosyasına kaydedilmiştir.
Bu dosya, projenin başka bir ortamda kurulabilmesi için gerekli tüm
bağımlılıkları listeler:

```
scikit-learn==1.4.2
pandas==2.2.2
numpy==1.26.4
matplotlib==3.8.4
seaborn==0.13.2
flask==3.0.3
joblib==1.4.2
boto3==1.34.102
```

`pip install -r requirements.txt` komutu ile tüm kütüphaneler tek seferde kurulabilir.

#### 4.1.3 İlk Git Commit

Günün sonunda tüm dosyalar Git ile versiyon kontrolüne alınmış ve
GitHub'a yüklenmiştir.

```bash
git add .
git commit -m "feat: PROJE-3 klasör yapısı oluşturuldu"
git push
```

**[GÖRSEL-3: GitHub commit geçmişi]**

---

### GÜN 2 — 27 Mayıs 2026: EDA, Model Eğitimi ve Yerel Test

#### 4.2.1 Veri Seti

**Kullanılan Veri Seti:** Titanic - Machine Learning from Disaster  
**Kaynak:** Stanford Üniversitesi açık veri seti  
**URL:** https://web.stanford.edu/class/archive/cs/cs109/cs109.1166/stuff/titanic.csv

Veri seti 887 yolcunun bilgisini içermektedir:

| Sütun | Açıklama | Örnek Değer |
|-------|----------|-------------|
| Survived | Hayatta kaldı mı? (0/1) | 0 veya 1 |
| Pclass | Yolcu sınıfı | 1, 2 veya 3 |
| Name | Yolcu adı | "Braund, Mr. Owen Harris" |
| Sex | Cinsiyet | male / female |
| Age | Yaş | 22.0 |
| Siblings/Spouses Aboard | Kardeş/eş sayısı | 1 |
| Parents/Children Aboard | Ebeveyn/çocuk sayısı | 0 |
| Fare | Bilet ücreti ($) | 7.25 |

#### 4.2.2 EDA (Keşifsel Veri Analizi)

EDA (Exploratory Data Analysis), makine öğrenmesi modelinden önce
veriyi tanıma ve anlama sürecidir. `model/data_analysis.py` scripti
çalıştırılarak aşağıdaki bulgular elde edilmiştir:

**Genel İstatistikler:**
- Toplam yolcu: 887
- Hayatta kalan: 342 kişi (%38.6)
- Hayatını kaybeden: 545 kişi (%61.4)
- Eksik değer: Bu veri setinde eksik değer bulunmamaktadır

**Temel Bulgular:**
- Kadın yolcuların büyük çoğunluğu hayatta kalmıştır
- 1. sınıf yolcular 3. sınıfa göre çok daha yüksek hayatta kalma oranına sahiptir
- Genç yolcular ve çocuklar daha yüksek hayatta kalma oranı göstermektedir

**[GÖRSEL-4: EDA grafikleri — eda_grafikleri.png dosyası]**
*(data/eda_grafikleri.png dosyasını buraya ekleyin)*

Bu grafik 6 alt grafikten oluşmaktadır:
- Sol üst: Genel hayatta kalma oranı (bar chart)
- Orta üst: Cinsiyete göre hayatta kalma
- Sağ üst: Yolcu sınıfına göre hayatta kalma
- Sol alt: Yaş dağılımı
- Orta alt: Bilet ücreti dağılımı
- Sağ alt: Korelasyon matrisi

```bash
# EDA çalıştırma komutu:
python "model/data_analysis.py"
```

#### 4.2.3 Veri Ön İşleme (Preprocessing)

Ham veri, modele verilmeden önce dönüştürülmüştür:

| İşlem | Açıklama |
|-------|----------|
| Cinsiyet kodlama | male=0, female=1 |
| Boş yaş değerleri | Medyan (ortalama) değerle dolduruldu |
| Boş ücret değerleri | Medyan değerle dolduruldu |
| Biniş limanı kodlama | C=0, Q=1, S=2 |
| Yeni özellik | FamilySize = SibSp + Parch + 1 |
| Gereksiz sütunlar | Name, PassengerId gibi sütunlar çıkarıldı |

Bilgisayar sayısal verileri anlar; "male/female" gibi metin değerleri
sayısal forma dönüştürülmeden modele verilemez.

#### 4.2.4 Model Eğitimi

`model/train_model.py` scripti ile üç farklı makine öğrenmesi
algoritması denenerek karşılaştırılmıştır:

**Logistic Regression (Lojistik Regresyon):**
Özelliklerin ağırlıklı toplamına dayalı doğrusal bir sınıflandırma yöntemidir.
En basit modeldir; yorumlanması kolaydır ancak karmaşık örüntüleri yakalamada
sınırlıdır.

**Random Forest (Rastgele Orman):**
100 karar ağacının oluşturduğu bir topluluk modelidir. Her ağaç bağımsız
tahmin yapar; çoğunluğun kararı final tahmin olur. Tek bir ağaca göre
çok daha güvenilirdir.

**Gradient Boosting (Gradyan Artırma):**
Her adımda bir önceki modelin hatalarını öğrenerek düzelten bir yöntemdir.
Zayıf modellerden güçlü bir model oluşturur.

**Model Karşılaştırma Sonuçları:**

| Model | CV Accuracy | Test Accuracy |
|-------|-------------|---------------|
| Logistic Regression | %80.5 ± 2.9 | %77.5 |
| Random Forest | %81.4 ± 1.8 | %78.1 |
| **Gradient Boosting** | **%83.4 ± 4.0** | **%80.3** |

**Kazanan: Gradient Boosting — %80.3 Test Accuracy**

**[GÖRSEL-5: Model performans grafikleri — model_performans.png]**
*(data/model_performans.png dosyasını buraya ekleyin)*

Bu grafik 3 bölümden oluşur:
- Sol: Confusion Matrix (doğru/yanlış tahminlerin dağılımı)
- Orta: 3 modelin accuracy karşılaştırması
- Sağ: Özellik önem skorları (hangi değişken en çok etki ediyor)

```bash
# Model eğitimi çalıştırma:
python "model/train_model.py"
```

Eğitim sonunda model `model/titanic_model.pkl` dosyasına kaydedilmiştir.
`.pkl` (pickle) formatı, Python'da nesneleri dosyaya kaydetmek için
kullanılan standarttır. Model bir kez eğitilip kaydedilir; her tahmin
için yeniden eğitilmesine gerek kalmaz.

#### 4.2.5 Flask API ile Yerel Test

Eğitilen model bir REST API'ye dönüştürülmüştür. `api/app.py` dosyası
Flask web framework'ü kullanılarak yazılmıştır.

```bash
# API'yi başlatma:
python "api/app.py"
# Çıktı: * Running on http://0.0.0.0:5000
```

**API Endpoint'leri:**

| Method | URL | Açıklama |
|--------|-----|----------|
| GET | /  | API bilgileri |
| GET | /health | Sağlık kontrolü |
| POST | /predict | Tahmin yap |

**Postman ile Test:**

Postman uygulaması kullanılarak API test edilmiştir:
- Method: POST
- URL: http://localhost:5000/predict
- Body (JSON):
```json
{
    "Pclass": 3,
    "Sex": "male",
    "Age": 25,
    "SibSp": 0,
    "Parch": 0,
    "Fare": 7.25,
    "Embarked": "S"
}
```

**[GÖRSEL-6: Postman ekranı — POST isteği ve cevap]**

API'nin döndürdüğü cevap:
```json
{
    "hayatta_kaldi": false,
    "mesaj": "❌ Hayatını kaybederdi.",
    "olasilik": {
        "hayatini_kaybetti": 0.9189,
        "hayatta_kaldi": 0.0811
    },
    "tahmin": 0
}
```

Bu cevap, 25 yaşında, 3. sınıf erkek yolcunun %91.89 ihtimalle
hayatını kaybedeceğini göstermektedir. Bu sonuç tarihi verilerle
örtüşmektedir.

**[GÖRSEL-7: localhost:5000 tarayıcı ekranı — API ana sayfası]**

Git commit:
```
fix: Stanford CSV sütun isimleri düzeltildi | EDA ve model tamamlandı
```

---

### GÜN 3 — 28 Mayıs 2026: AWS Dağıtımı ve Canlı Yayın

#### 4.3.1 AWS S3 Bucket Oluşturma

AWS S3 (Simple Storage Service), bulutta dosya depolama hizmetidir.
Bu projede iki farklı amaçla kullanılmıştır:

1. **Model Dosyası Depolama:** `titanic_model.pkl` dosyası S3'e yüklenmiştir.
   Lambda fonksiyonu her çalıştığında bu dosyayı S3'ten okur.

2. **Web Sitesi Barındırma:** `index.html` dosyası S3'e yüklenerek
   Static Website Hosting özelliği ile web sitesi olarak yayınlanmıştır.

**Oluşturulan Bucket:**
- **Ad:** bulut-proje-titanic-ml-titanic-ebrar
- **Bölge:** eu-central-1 (Frankfurt)
- **Yüklenen Dosyalar:** titanic_model.pkl (132 KB), lambda_linux.zip (80 MB)

**[GÖRSEL-8: AWS S3 bucket içeriği — Objects listesi]**

#### 4.3.2 AWS Lambda Fonksiyonu

AWS Lambda, sunucu kurmadan kod çalıştırmayı sağlayan "Serverless Computing"
hizmetidir. Temel prensibi şudur:

- İstek geldiğinde fonksiyon **uyanır**
- İşlemi yapar ve cevabı döndürür
- Fonksiyon tekrar **uyur**
- Kullanılmayan süre için ücret ödenmez

**Lambda Kurulum Süreci:**

İlk girişimde, Python kütüphaneleri Windows işletim sisteminde
derlendiği için Linux ortamında çalışan Lambda'da hata vermiştir:
```
AttributeError: module 'os' has no attribute 'add_dll_directory'
```

Bu sorun, **AWS CloudShell** kullanılarak çözülmüştür. CloudShell,
AWS'nin kendi Linux terminalıdır. Kütüphaneler burada derlendiğinde
Lambda ile uyumlu hale gelmektedir.

**CloudShell'de yapılan işlemler:**
```bash
mkdir lambda_pkg
pip install scikit-learn numpy joblib -t lambda_pkg/
# lambda_function.py dosyası oluşturuldu
zip -r lambda_linux.zip lambda_pkg/
aws s3 cp lambda_linux.zip s3://bulut-proje-titanic-ml-titanic-ebrar/
aws lambda update-function-code \
  --function-name titanic-predict \
  --s3-bucket bulut-proje-titanic-ml-titanic-ebrar \
  --s3-key lambda_linux.zip
```

**[GÖRSEL-9: AWS CloudShell ekranı — komutlar çalışırken]**

**Lambda Ayarları:**

| Ayar | Değer | Açıklama |
|------|-------|----------|
| Fonksiyon Adı | titanic-predict | — |
| Runtime | Python 3.13 | Programlama dili |
| Bellek | 1024 MB | Scikit-learn için yeterli |
| Timeout | 60 saniye | Model yükleme süresi için |
| Handler | lambda_function.lambda_handler | Giriş noktası |

**Environment Variables (Ortam Değişkenleri):**

| Key | Value |
|-----|-------|
| S3_BUCKET_NAME | bulut-proje-titanic-ml-titanic-ebrar |
| MODEL_KEY | titanic_model.pkl |

**[GÖRSEL-10: AWS Lambda fonksiyon sayfası — Configuration/Environment Variables]**

**IAM İzinleri:**

Lambda'nın S3'teki model dosyasını okuyabilmesi için
`AmazonS3ReadOnlyAccess` politikası eklenmiştir.

**[GÖRSEL-11: AWS IAM rol sayfası — AmazonS3ReadOnlyAccess politikası]**

**Lambda Test Sonucu:**

Lambda'nın Test sekmesinde aşağıdaki JSON ile test yapılmıştır:
```json
{
  "httpMethod": "POST",
  "body": "{\"Pclass\": 1, \"Sex\": \"female\", \"Age\": 35, \"SibSp\": 1, \"Parch\": 0, \"Fare\": 71.28, \"Embarked\": \"C\"}"
}
```

Sonuç:
```json
{
  "statusCode": 200,
  "body": "{\"tahmin\": 1, \"hayatta_kaldi\": true, \"olasilik\": {\"hayatini_kaybetti\": 0.0385, \"hayatta_kaldi\": 0.9615}, \"mesaj\": \"✅ Hayatta kalabilirdi!\"}"
}
```

1. sınıf kadın yolcu için model %96.15 hayatta kalma olasılığı vermiştir.
Bu sonuç tarihi verilerle tam örtüşmektedir.

**[GÖRSEL-12: AWS Lambda Test sekmesi — başarılı test sonucu (yeşil)]**

#### 4.3.3 AWS API Gateway

API Gateway, Lambda fonksiyonuna internet üzerinden erişilebilir
bir HTTP URL oluşturmaktadır. Lambda'nın "kapıcısı" rolünü üstlenir.

Lambda → **Add trigger** → API Gateway → REST API → Open → Add

**Oluşturulan API:**
- **Ad:** titanic-predict-API
- **Endpoint:** https://l7om4ms6bi.execute-api.eu-central-1.amazonaws.com/default/titanic-predict
- **Method:** ANY (tüm HTTP metodları)
- **Auth:** NONE (herkese açık)

**[GÖRSEL-13: AWS Lambda sayfası — API Gateway trigger]**

#### 4.3.4 CORS Nedir? Neden Gerekti?

**CORS (Cross-Origin Resource Sharing — Çapraz Kaynak Paylaşımı)**,
tarayıcıların güvenlik mekanizmasıdır.

Senaryomuz şöyledir:
- Web sitesi: `http://bulut-proje-...s3-website.eu-central-1.amazonaws.com`
- API: `https://l7om4ms6bi.execute-api.eu-central-1.amazonaws.com`

Bu iki adres farklı "origin" (kaynak) sayılır. Tarayıcı,
güvenlik nedeniyle farklı kaynaklara istek atmayı **varsayılan olarak engeller**.
Buna CORS politikası denir.

**Çözüm:** API Gateway'de CORS etkinleştirilmiştir. Bu sayede API,
yanıt başlıklarına şunu ekler:
```
Access-Control-Allow-Origin: *
```
Bu başlık tarayıcıya der ki: "Her kaynaktan gelen istek kabul edilir."

**[GÖRSEL-14: API Gateway Console — CORS ayarları]**

#### 4.3.5 S3 Static Website Hosting

Web arayüzü (`frontend/index.html`) AWS S3 üzerinde barındırılmıştır.
S3 Static Website Hosting, bir sunucuya ihtiyaç duymadan web sayfası
yayınlamayı sağlar.

**Yapılan Ayarlar:**
1. Bucket → Properties → Static website hosting → Enable
2. Index document: `index.html`
3. Block public access → Kapatıldı
4. Bucket policy → Herkese okuma izni verildi
5. `index.html` dosyası yüklendi

**Web Sitesi URL'si:**
http://bulut-proje-titanic-ml-titanic-ebrar.s3-website.eu-central-1.amazonaws.com/

**[GÖRSEL-15: Web sitesi ekranı — form doldurulmuş hali]**

**[GÖRSEL-16: Web sitesi ekranı — tahmin sonucu gösterilmiş hali]**

---

## 5. MAKİNE ÖĞRENMESİ MODELİ DETAYLARI

### Performans Metrikleri

**Accuracy (Doğruluk):** %80.3
Tüm tahminlerin yüzdesi olarak doğru olanların oranıdır.

**Precision (Kesinlik):** %77.4
"Hayatta kaldı" dediğimizde ne kadar isabetliyiz?

**Recall (Duyarlılık):** %69.6
Gerçekten hayatta kalanların kaçını doğru tespit ettik?

**F1-Score:** %73.3
Precision ve Recall'un harmonik ortalaması.

### Confusion Matrix

|  | Tahmin: Hayatını Kaybetti | Tahmin: Hayatta Kaldı |
|--|--------------------------|----------------------|
| **Gerçek: Hayatını Kaybetti** | 95 (Doğru) | 14 (Yanlış) |
| **Gerçek: Hayatta Kaldı** | 21 (Yanlış) | 48 (Doğru) |

### En Etkili Özellikler (Feature Importance)

Gradient Boosting modeline göre hayatta kalmayı etkileyen
en önemli faktörler:
1. **Cinsiyet** — en belirleyici faktör
2. **Bilet Ücreti** — sosyoekonomik durumu yansıtır
3. **Yaş** — özellikle çocuklar önceliklendirilmiştir
4. **Yolcu Sınıfı** — 1. sınıf en yüksek hayatta kalma oranına sahip

---

## 6. AWS SERVİSLERİ AÇIKLAMALARI

### AWS S3 (Simple Storage Service)
Bulut tabanlı nesne depolama hizmetidir. Herhangi bir dosyayı
(resim, video, kod, veri) internet üzerinden depolamak ve
erişmek için kullanılır. Bu projede:
- Model dosyası (.pkl) depolanmıştır
- Web sitesi dosyaları (HTML) barındırılmıştır

### AWS Lambda
Sunucu yönetimine gerek duymadan kod çalıştırmayı sağlayan
"Serverless" (Sunucusuz) hesaplama hizmetidir.
- İstek geldiğinde otomatik başlar
- İşlem bitince durur
- Sadece kullanılan süre için ücretlendirilir
- Free Tier: Aylık 1 milyon istek ücretsiz

### AWS API Gateway
RESTful API'ler oluşturmak, yönetmek ve dağıtmak için
kullanılan bir servistir. Lambda fonksiyonuna internet
üzerinden erişilebilir HTTP URL sağlar.

### AWS IAM (Identity and Access Management)
AWS servislerinin birbirine erişim izinlerini yönetir.
Lambda'nın S3'e erişebilmesi için `AmazonS3ReadOnlyAccess`
politikası tanımlanmıştır.

### AWS CloudShell
AWS'nin tarayıcı tabanlı Linux terminalidir. Lambda paketinin
Linux ortamında derlenmesi için kullanılmıştır.

---

## 7. API KULLANIMI

### İstek Formatı
```bash
POST https://l7om4ms6bi.execute-api.eu-central-1.amazonaws.com/default/titanic-predict
Content-Type: application/json

{
    "Pclass": 3,       # Yolcu sınıfı: 1, 2 veya 3
    "Sex": "male",     # Cinsiyet: "male" veya "female"
    "Age": 25,         # Yaş
    "SibSp": 0,        # Kardeş/eş sayısı
    "Parch": 0,        # Ebeveyn/çocuk sayısı
    "Fare": 7.25,      # Bilet ücreti ($)
    "Embarked": "S"    # Biniş limanı: C, Q veya S
}
```

### Cevap Formatı
```json
{
    "tahmin": 0,
    "hayatta_kaldi": false,
    "olasilik": {
        "hayatini_kaybetti": 0.9189,
        "hayatta_kaldi": 0.0811
    },
    "mesaj": "❌ Hayatini kaybederdi."
}
```

---

## 8. SONUÇ VE DEĞERLENDİRME

Bu projede makine öğrenmesi ve bulut bilişim kavramları
bir arada uygulanmıştır.

**Teknik Kazanımlar:**
- Gerçek veri seti üzerinde EDA ve veri ön işleme
- Üç farklı ML algoritmasının karşılaştırmalı değerlendirmesi
- REST API geliştirme (Flask)
- Serverless mimari (AWS Lambda)
- Nesne depolama (AWS S3)
- API yönetimi (AWS API Gateway)
- Linux ortamında paket derleme (AWS CloudShell)
- CORS güvenlik mekanizması

**Karşılaşılan Zorluklar ve Çözümler:**

| Sorun | Çözüm |
|-------|-------|
| Windows/Linux uyumsuzluğu | AWS CloudShell ile Linux'ta paket derleme |
| Lambda timeout (3 sn) | Timeout 60 saniyeye çıkarıldı |
| Lambda bellek yetersizliği | 128 MB'dan 1024 MB'a çıkarıldı |
| CORS hatası | API Gateway'de CORS etkinleştirildi |
| S3 erişim reddi | Bucket policy ve public access ayarlandı |

**Sonuç:** Geliştirilen sistem, Titanic yolcularının hayatta
kalıp kalmayacağını %80.3 doğrulukla tahmin etmektedir.
Model AWS Lambda üzerinde serverless olarak çalışmakta,
API Gateway aracılığıyla internet üzerinden erişilebilmekte
ve S3 üzerinde barındırılan web arayüzü ile kullanıcılara
sunulmaktadır.

---

*Rapor Tarihi: 28 Mayıs 2026*  
*GitHub: https://github.com/Ebrar3/Bulut-proje/tree/main/FİNAL/PROJE-3*
