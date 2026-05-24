"""
PROJE-3: Akıllı Veri Analitiği ve Makine Öğrenmesi
AŞAMA 3: Flask REST API — Yerel Tahmin Servisi

Endpoint: POST /predict
Çalıştır: python api/app.py
Test     : http://localhost:5000
"""

from flask import Flask, request, jsonify
import joblib
import numpy as np
import os

app = Flask(__name__)

# ─── Model Yükleme ────────────────────────────────────────────
model_path = os.path.join(os.path.dirname(__file__), '..', 'model', 'titanic_model.pkl')

try:
    model_info = joblib.load(model_path)
    model = model_info['model']
    features = model_info['features']
    print(f"[✓] Model yüklendi: {model_info['model_name']}")
    print(f"    Accuracy: {model_info['accuracy']:.4f}")
    print(f"    Features: {features}")
except FileNotFoundError:
    print("[!] Model bulunamadı! Önce model/train_model.py çalıştırın.")
    model = None
    features = []


def preprocess_input(data: dict) -> list:
    """
    Ham giriş verilerini model için hazırlar.
    Aynı preprocessing adımları train_model.py ile uyumlu olmalı.
    """
    pclass = int(data.get('Pclass', 3))
    sex_encoded = 1 if str(data.get('Sex', 'male')).lower() == 'female' else 0
    age = float(data.get('Age', 30))
    sibsp = int(data.get('SibSp', 0))
    parch = int(data.get('Parch', 0))
    fare = float(data.get('Fare', 15.0))
    embarked_map = {'C': 0, 'Q': 1, 'S': 2}
    embarked_encoded = embarked_map.get(str(data.get('Embarked', 'S')).upper(), 2)
    family_size = sibsp + parch + 1

    feature_map = {
        'Pclass': pclass,
        'Sex_encoded': sex_encoded,
        'Age': age,
        'SibSp': sibsp,
        'Parch': parch,
        'Fare': fare,
        'Embarked_encoded': embarked_encoded,
        'FamilySize': family_size
    }

    return [feature_map[f] for f in features]


# ─── Rotalar ──────────────────────────────────────────────────
@app.route('/', methods=['GET'])
def index():
    """Ana sayfa — API kullanım kılavuzu"""
    return jsonify({
        'proje': 'PROJE-3: Titanic Hayatta Kalma Tahmini API',
        'versiyon': '1.0.0',
        'model': model_info.get('model_name', 'Bilinmiyor') if model else 'Yüklenmedi',
        'accuracy': round(model_info.get('accuracy', 0), 4) if model else 0,
        'endpoints': {
            'GET  /': 'Bu kılavuz',
            'POST /predict': 'Tahmin yap',
            'GET  /health': 'Servis sağlık kontrolü'
        },
        'ornek_istek': {
            'url': 'POST /predict',
            'body': {
                'Pclass': 3,
                'Sex': 'male',
                'Age': 25,
                'SibSp': 0,
                'Parch': 0,
                'Fare': 7.25,
                'Embarked': 'S'
            }
        }
    }), 200


@app.route('/health', methods=['GET'])
def health():
    """Servis sağlık kontrolü"""
    return jsonify({
        'durum': 'aktif',
        'model_yuklendi': model is not None,
        'servis': 'Titanic ML API'
    }), 200


@app.route('/predict', methods=['POST'])
def predict():
    """
    Titanic yolcusunun hayatta kalıp kalmayacağını tahmin eder.

    İstek gövdesi (JSON):
    {
        "Pclass"  : 1 | 2 | 3          (Yolcu sınıfı)
        "Sex"     : "male" | "female"  (Cinsiyet)
        "Age"     : float              (Yaş)
        "SibSp"   : int                (Kardeş/eş sayısı)
        "Parch"   : int                (Ebeveyn/çocuk sayısı)
        "Fare"    : float              (Bilet ücreti)
        "Embarked": "C" | "Q" | "S"   (Biniş limanı)
    }
    """
    if model is None:
        return jsonify({'hata': 'Model yüklenmedi. train_model.py çalıştırın.'}), 500

    # Gelen JSON verisini al
    if not request.is_json:
        return jsonify({'hata': 'İstek Content-Type: application/json olmalıdır.'}), 400

    data = request.get_json()

    try:
        # Veriyi işle
        input_features = preprocess_input(data)
        input_array = np.array([input_features])

        # Tahmin yap
        prediction = int(model.predict(input_array)[0])
        probability = model.predict_proba(input_array)[0]

        # Sonucu döndür
        result = {
            'tahmin': prediction,
            'hayatta_kaldi': bool(prediction == 1),
            'olasilik': {
                'hayatini_kaybetti': round(float(probability[0]), 4),
                'hayatta_kaldi': round(float(probability[1]), 4)
            },
            'mesaj': (
                '✅ Bu yolcu hayatta kalabilirdi!' if prediction == 1
                else '❌ Bu yolcu ne yazık ki hayatını kaybederdi.'
            ),
            'girdi': data
        }

        return jsonify(result), 200

    except KeyError as e:
        return jsonify({'hata': f'Eksik alan: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'hata': f'İşlem hatası: {str(e)}'}), 500


# ─── Çalıştır ─────────────────────────────────────────────────
if __name__ == '__main__':
    print("\n" + "=" * 50)
    print("  Titanic ML API Başlatılıyor...")
    print("  URL: http://localhost:5000")
    print("  Test: POST http://localhost:5000/predict")
    print("=" * 50 + "\n")
    app.run(host='0.0.0.0', port=5000, debug=True)
