# PROJE-3: Akıllı Veri Analitiği ve Makine Öğrenmesi Uygulaması

## 📌 Proje Özeti
Bu projede Titanic veri seti üzerinde bir **sınıflandırma (classification)** modeli geliştirilmiştir. 
Python ve Scikit-learn kullanılarak eğitilen model, AWS Lambda + API Gateway ile bulut ortamına dağıtılmıştır.

## 🛠️ Kullanılan Teknolojiler
- **Backend Dili:** Python 3.x
- **ML Kütüphaneleri:** Scikit-learn, Pandas, NumPy, Matplotlib, Seaborn
- **API:** Flask
- **Veritabanı:** —
- **Bulut Platformu:** AWS (S3, Lambda, API Gateway)

## ☁️ AWS Mimarisi
```
Kullanıcı → API Gateway → Lambda Fonksiyonu → S3 (model.pkl) → Tahmin Sonucu
```

## 📁 Klasör Yapısı
```
PROJE-3/
├── data/               → Veri seti (titanic.csv)
├── model/              → Model eğitim kodu ve .pkl dosyası
├── api/                → Flask API ve Lambda handler
├── frontend/           → Web arayüzü (S3 static hosting)
├── docs/               → Rapor
├── requirements.txt    → Python bağımlılıkları
└── README.md
```

## 📊 Model Performansı
*(Model eğitildikten sonra burası güncellenecektir)*

## 🔗 Linkler
- API Endpoint: *(deploy sonrası eklenecek)*
- Web Arayüzü: *(S3 URL deploy sonrası eklenecek)*
- Demo Video: *(video sonrası eklenecek)*
