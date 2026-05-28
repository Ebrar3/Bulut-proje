"""
PROJE-3: Akıllı Veri Analitiği ve Makine Öğrenmesi
AŞAMA 2: Model Eğitimi — Titanic Hayatta Kalma Tahmini

Model: Gradient Boosting Classifier (en iyi sonuç verir)
Kaydetme: titanic_model.pkl (joblib ile)
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import joblib
import os
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (accuracy_score, precision_score, recall_score,
                             f1_score, confusion_matrix, classification_report)

print("=" * 60)
print("PROJE-3: Model Eğitimi Başlıyor")
print("=" * 60)

# ─────────────────────────────────────────
# 1. VERİ YÜKLEME
# ─────────────────────────────────────────
data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'titanic.csv')

if not os.path.exists(data_path):
    print("[!] Veri seti bulunamadı. Önce data_analysis.py çalıştırın!")
    exit(1)

df = pd.read_csv(data_path)
print(f"[✓] Veri yüklendi: {df.shape[0]} satır, {df.shape[1]} sütun")

# ─────────────────────────────────────────
# 2. VERİ ÖN İŞLEME (PREPROCESSING)
# ─────────────────────────────────────────
print("\n[1] Veri ön işleme...")

# Sütun isimlerini kontrol et ve normalize et
df.columns = df.columns.str.strip()

# Hedef değişken kontrolü
target_col = 'Survived'
if target_col not in df.columns:
    print(f"[!] '{target_col}' sütunu bulunamadı. Sütunlar: {list(df.columns)}")
    exit(1)

# Kullanılacak özellikler (feature engineering)
features_to_use = []

# Pclass
if 'Pclass' in df.columns:
    features_to_use.append('Pclass')

# Sex → sayısal
if 'Sex' in df.columns:
    df['Sex_encoded'] = df['Sex'].map({'male': 0, 'female': 1})
    features_to_use.append('Sex_encoded')

# Age — eksik değerleri ortalama ile doldur
if 'Age' in df.columns:
    df['Age'] = df['Age'].fillna(df['Age'].median())
    features_to_use.append('Age')

# SibSp (kardeş/eş sayısı)
# Stanford CSV'sinde bu sütun 'Siblings/Spouses Aboard' olarak geliyor
if 'SibSp' in df.columns:
    sibsp_col = 'SibSp'
elif 'Siblings/Spouses Aboard' in df.columns:
    sibsp_col = 'Siblings/Spouses Aboard'
    df['SibSp'] = df[sibsp_col]   # standart isimle kopyala
    sibsp_col = 'SibSp'
else:
    sibsp_col = None

if sibsp_col:
    features_to_use.append('SibSp')

# Parch (ebeveyn/çocuk sayısı)
# Stanford CSV'sinde 'Parents/Children Aboard' olarak geliyor
if 'Parch' in df.columns:
    parch_col = 'Parch'
elif 'Parents/Children Aboard' in df.columns:
    parch_col = 'Parents/Children Aboard'
    df['Parch'] = df[parch_col]   # standart isimle kopyala
    parch_col = 'Parch'
else:
    parch_col = None

if parch_col:
    features_to_use.append('Parch')

# Fare — eksik değerleri medyan ile doldur
if 'Fare' in df.columns:
    df['Fare'] = df['Fare'].fillna(df['Fare'].median())
    features_to_use.append('Fare')

# Embarked → sayısal (C=0, Q=1, S=2)  [Stanford CSV'sinde bu sütun yok, if korumalı]
if 'Embarked' in df.columns:
    df['Embarked'] = df['Embarked'].fillna(df['Embarked'].mode()[0])
    df['Embarked_encoded'] = df['Embarked'].map({'C': 0, 'Q': 1, 'S': 2})
    features_to_use.append('Embarked_encoded')

# Aile büyüklüğü (feature engineering) — SibSp + Parch + 1
if sibsp_col and parch_col:
    df['FamilySize'] = df['SibSp'] + df['Parch'] + 1
    features_to_use.append('FamilySize')

print(f"  Kullanılan özellikler: {features_to_use}")

X = df[features_to_use]
y = df[target_col]

print(f"  X şekli: {X.shape}")
print(f"  y dağılımı: {y.value_counts().to_dict()}")

# ─────────────────────────────────────────
# 3. EĞİTİM / TEST BÖLME
# ─────────────────────────────────────────
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
print(f"\n[2] Eğitim/Test bölme:")
print(f"  Eğitim seti : {X_train.shape[0]} örnek")
print(f"  Test seti   : {X_test.shape[0]} örnek")

# ─────────────────────────────────────────
# 4. 3 MODELİ KARŞILAŞTIR
# ─────────────────────────────────────────
print("\n[3] Modeller karşılaştırılıyor...")

models = {
    'Logistic Regression': LogisticRegression(max_iter=1000, random_state=42),
    'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42),
    'Gradient Boosting': GradientBoostingClassifier(n_estimators=100, random_state=42)
}

results = {}
for name, model in models.items():
    cv_scores = cross_val_score(model, X_train, y_train, cv=5, scoring='accuracy')
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    results[name] = {
        'model': model,
        'cv_mean': cv_scores.mean(),
        'cv_std': cv_scores.std(),
        'test_accuracy': acc
    }
    print(f"  {name}:")
    print(f"    CV Accuracy : {cv_scores.mean():.4f} ± {cv_scores.std():.4f}")
    print(f"    Test Accuracy: {acc:.4f}")

# ─────────────────────────────────────────
# 5. EN İYİ MODEL: Gradient Boosting
# ─────────────────────────────────────────
best_model_name = max(results, key=lambda k: results[k]['test_accuracy'])
best_model = results[best_model_name]['model']
print(f"\n[4] En iyi model: {best_model_name}")

y_pred_best = best_model.predict(X_test)

print("\n[5] DETAYLI PERFORMANS METRİKLERİ")
print(f"  Accuracy  : {accuracy_score(y_test, y_pred_best):.4f}")
print(f"  Precision : {precision_score(y_test, y_pred_best):.4f}")
print(f"  Recall    : {recall_score(y_test, y_pred_best):.4f}")
print(f"  F1-Score  : {f1_score(y_test, y_pred_best):.4f}")
print(f"\n  Sınıflandırma Raporu:")
print(classification_report(y_test, y_pred_best,
                            target_names=['Hayatını Kaybetti', 'Hayatta Kaldı']))

# ─────────────────────────────────────────
# 6. GRAFİKLER
# ─────────────────────────────────────────
print("[6] Performans grafikleri oluşturuluyor...")

fig, axes = plt.subplots(1, 3, figsize=(16, 5))
fig.suptitle('Model Performans Analizi — Gradient Boosting', fontsize=14, fontweight='bold')

# Grafik 1: Confusion Matrix
cm = confusion_matrix(y_test, y_pred_best)
im = axes[0].imshow(cm, interpolation='nearest', cmap='Blues')
axes[0].set_title('Confusion Matrix', fontweight='bold')
axes[0].set_xlabel('Tahmin')
axes[0].set_ylabel('Gerçek')
axes[0].set_xticks([0, 1])
axes[0].set_yticks([0, 1])
axes[0].set_xticklabels(['Hayatını\nKaybetti', 'Hayatta\nKaldı'])
axes[0].set_yticklabels(['Hayatını\nKaybetti', 'Hayatta\nKaldı'])
for i in range(2):
    for j in range(2):
        axes[0].text(j, i, str(cm[i, j]), ha='center', va='center',
                    fontsize=16, fontweight='bold',
                    color='white' if cm[i, j] > cm.max()/2 else 'black')

# Grafik 2: Model Karşılaştırması
model_names = list(results.keys())
accuracies = [results[n]['test_accuracy'] for n in model_names]
short_names = ['Logistic\nRegression', 'Random\nForest', 'Gradient\nBoosting']
bars = axes[1].bar(short_names, accuracies,
                   color=['#3498db', '#2ecc71', '#e67e22'], edgecolor='white')
axes[1].set_title('Model Karşılaştırması (Test Accuracy)', fontweight='bold')
axes[1].set_ylabel('Accuracy')
axes[1].set_ylim(0.7, 1.0)
for bar, acc in zip(bars, accuracies):
    axes[1].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.005,
                f'{acc:.3f}', ha='center', fontweight='bold')

# Grafik 3: Özellik Önem Skoru (Feature Importance)
if hasattr(best_model, 'feature_importances_'):
    importances = best_model.feature_importances_
    indices = np.argsort(importances)[::-1]
    feat_names = [features_to_use[i] for i in indices]
    axes[2].barh(range(len(indices)), importances[indices], color='#9b59b6', edgecolor='white')
    axes[2].set_yticks(range(len(indices)))
    axes[2].set_yticklabels(feat_names)
    axes[2].set_title('Özellik Önem Skorları', fontweight='bold')
    axes[2].set_xlabel('Önem Skoru')
    axes[2].invert_yaxis()

plt.tight_layout()
output_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
plt.savefig(os.path.join(output_dir, 'model_performans.png'), dpi=150, bbox_inches='tight')
print(f"  [✓] Grafik kaydedildi: data/model_performans.png")

# ─────────────────────────────────────────
# 7. MODELİ KAYDET
# ─────────────────────────────────────────
model_dir = os.path.dirname(__file__)
model_path = os.path.join(model_dir, 'titanic_model.pkl')
model_info = {
    'model': best_model,
    'features': features_to_use,
    'model_name': best_model_name,
    'accuracy': accuracy_score(y_test, y_pred_best)
}
joblib.dump(model_info, model_path)
print(f"\n[7] Model kaydedildi: {model_path}")

print("\n" + "=" * 60)
print("MODEL EĞİTİMİ TAMAMLANDI!")
print(f"  En iyi model  : {best_model_name}")
print(f"  Test Accuracy : {accuracy_score(y_test, y_pred_best):.4f}")
print(f"  Model dosyası : model/titanic_model.pkl")
print(f"  Sonraki adım  : api/app.py çalıştırın")
print("=" * 60)
