# PROJE-3: Akıllı Veri Analitiği ve Makine Öğrenmesi Uygulaması

## 📌 Proje Özeti
Titanic veri seti üzerinde **Gradient Boosting** sınıflandırma modeli geliştirilmiştir.
Model, AWS Lambda + API Gateway ile bulut ortamına dağıtılmış, AWS S3 üzerinde
web arayüzü olarak yayınlanmıştır.

## 🌐 Canlı Demo
**Web Arayüzü:** http://bulut-proje-titanic-ml-titanic-ebrar.s3-website.eu-central-1.amazonaws.com/

**API Endpoint:** https://l7om4ms6bi.execute-api.eu-central-1.amazonaws.com/default/titanic-predict

## 🛠️ Kullanılan Teknolojiler
- **Backend Dili:** Python 3.13
- **ML Kütüphaneleri:** Scikit-learn, Pandas, NumPy, Matplotlib, Seaborn
- **API:** Flask (yerel) → AWS Lambda (bulut)
- **Bulut Platformu:** AWS (S3, Lambda, API Gateway)

## ☁️ AWS Mimarisi
```
Kullanıcı → S3 (Web) → API Gateway → Lambda → S3 (model.pkl) → Tahmin
```

## 📊 Model Performansı
| Model | Test Accuracy |
|-------|--------------|
| Logistic Regression | %77.5 |
| Random Forest | %78.1 |
| **Gradient Boosting** ⭐ | **%80.3** |

## 📁 Klasör Yapısı
```
PROJE-3/
├── data/               → Veri seti + EDA grafikleri
├── model/              → Model eğitim kodu + titanic_model.pkl
├── api/                → Flask API + Lambda handler
├── frontend/           → Web arayüzü (S3 static hosting)
└── requirements.txt    → Python bağımlılıkları
```

## 🔗 API Kullanımı
```bash
curl -X POST https://l7om4ms6bi.execute-api.eu-central-1.amazonaws.com/default/titanic-predict \
  -H "Content-Type: application/json" \
  -d '{"Pclass": 3, "Sex": "male", "Age": 25, "SibSp": 0, "Parch": 0, "Fare": 7.25, "Embarked": "S"}'
```

**Örnek Cevap:**
```json
{
  "tahmin": 0,
  "hayatta_kaldi": false,
  "olasilik": {"hayatini_kaybetti": 0.9189, "hayatta_kaldi": 0.0811},
  "mesaj": "❌ Hayatini kaybederdi."
}
```
