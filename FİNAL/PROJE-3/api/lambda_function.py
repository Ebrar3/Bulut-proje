"""
PROJE-3: Akıllı Veri Analitiği ve Makine Öğrenmesi
AŞAMA 4: AWS Lambda Handler

Bu fonksiyon:
1. S3'ten modeli yükler (her çağrıda cache'e alır)
2. API Gateway'den gelen HTTP isteğini işler
3. Tahmin sonucunu JSON olarak döndürür

Deploy adımları:
  1. pip install scikit-learn numpy joblib -t ./lambda_package/
  2. cp lambda_function.py ./lambda_package/
  3. cd lambda_package && zip -r ../lambda.zip .
  4. AWS Lambda'ya yükle (Python 3.11 runtime)
  5. Environment Variables:
       S3_BUCKET_NAME = titanic-ml-model-[ismin]
       MODEL_KEY      = titanic_model.pkl
"""

import json
import boto3
import joblib
import numpy as np
import os
import io

# ─── Sabitler (Lambda Environment Variables'dan alınır) ───────
S3_BUCKET = os.environ.get('S3_BUCKET_NAME', 'titanic-ml-model')
MODEL_KEY = os.environ.get('MODEL_KEY', 'titanic_model.pkl')

# ─── Global cache (Lambda container re-use için) ──────────────
_model_info = None


def load_model_from_s3():
    """S3'ten modeli indir ve önbelleğe al."""
    global _model_info

    if _model_info is not None:
        print("[Cache] Model önbellekten yüklendi.")
        return _model_info

    print(f"[S3] Model indiriliyor: s3://{S3_BUCKET}/{MODEL_KEY}")
    s3 = boto3.client('s3')
    response = s3.get_object(Bucket=S3_BUCKET, Key=MODEL_KEY)
    model_bytes = response['Body'].read()
    _model_info = joblib.load(io.BytesIO(model_bytes))
    print(f"[✓] Model yüklendi: {_model_info['model_name']} | Accuracy: {_model_info['accuracy']:.4f}")
    return _model_info


def preprocess_input(data: dict, features: list) -> list:
    """Ham giriş verisini model için hazırla."""
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


def lambda_handler(event, context):
    """
    Ana Lambda giriş noktası.

    API Gateway proxy entegrasyonu beklenir.
    """
    print(f"[Event] {json.dumps(event)}")

    # CORS headers
    headers = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Allow-Methods': 'POST, GET, OPTIONS'
    }

    # OPTIONS preflight isteği
    if event.get('httpMethod') == 'OPTIONS':
        return {'statusCode': 200, 'headers': headers, 'body': ''}

    # GET → sağlık kontrolü
    if event.get('httpMethod') == 'GET':
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({
                'durum': 'aktif',
                'servis': 'Titanic ML API (AWS Lambda)',
                'model_bucket': S3_BUCKET
            })
        }

    # POST → tahmin
    try:
        # Model yükle
        model_info = load_model_from_s3()
        model = model_info['model']
        features = model_info['features']

        # İstek gövdesini ayrıştır
        body = event.get('body', '{}')
        if isinstance(body, str):
            data = json.loads(body)
        else:
            data = body

        # Veriyi işle ve tahmin yap
        input_features = preprocess_input(data, features)
        input_array = np.array([input_features])
        prediction = int(model.predict(input_array)[0])
        probability = model.predict_proba(input_array)[0]

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
            )
        }

        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps(result, ensure_ascii=False)
        }

    except json.JSONDecodeError:
        return {
            'statusCode': 400,
            'headers': headers,
            'body': json.dumps({'hata': 'Geçersiz JSON formatı'})
        }
    except Exception as e:
        print(f"[HATA] {str(e)}")
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'hata': str(e)})
        }
