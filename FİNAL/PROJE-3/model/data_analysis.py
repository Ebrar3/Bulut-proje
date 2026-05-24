"""
PROJE-3: Akıllı Veri Analitiği ve Makine Öğrenmesi
AŞAMA 1: Keşifsel Veri Analizi (Exploratory Data Analysis - EDA)

Veri Seti: Titanic - Machine Learning from Disaster (Kaggle)
Kaynak: https://web.stanford.edu/class/archive/cs/cs109/cs109.1166/stuff/titanic.csv
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # GUI olmadan grafik kaydetmek için
import seaborn as sns
import os

# ─────────────────────────────────────────
# 1. VERİ YÜKLEME
# ─────────────────────────────────────────
print("=" * 60)
print("PROJE-3: Titanic Veri Seti — EDA Başlıyor")
print("=" * 60)

# Veri setini internetten yükle (yoksa indir)
data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'titanic.csv')

url = "https://web.stanford.edu/class/archive/cs/cs109/cs109.1166/stuff/titanic.csv"

try:
    df = pd.read_csv(data_path)
    print(f"[✓] Veri yerel dosyadan yüklendi: {data_path}")
except FileNotFoundError:
    print("[!] Yerel dosya bulunamadı, internetten indiriliyor...")
    df = pd.read_csv(url)
    # Yerel olarak kaydet
    os.makedirs(os.path.join(os.path.dirname(__file__), '..', 'data'), exist_ok=True)
    df.to_csv(data_path, index=False)
    print(f"[✓] Veri indirildi ve kaydedildi: {data_path}")

# ─────────────────────────────────────────
# 2. GENEL BİLGİLER
# ─────────────────────────────────────────
print("\n[1] VERİ SETİ GENEL BİLGİLERİ")
print(f"  Satır sayısı  : {df.shape[0]}")
print(f"  Sütun sayısı  : {df.shape[1]}")
print(f"  Sütunlar      : {list(df.columns)}")

print("\n[2] İLK 5 SATIR")
print(df.head())

print("\n[3] EKSİK DEĞER ANALİZİ")
missing = df.isnull().sum()
missing_pct = (missing / len(df) * 100).round(2)
missing_df = pd.DataFrame({'Eksik Sayı': missing, 'Eksik %': missing_pct})
print(missing_df[missing_df['Eksik Sayı'] > 0])

print("\n[4] İSTATİSTİKSEL ÖZET")
print(df.describe())

print("\n[5] HAYATİ KALANIM ORANI")
survived_counts = df['Survived'].value_counts()
print(f"  Hayatta kalan     : {survived_counts.get(1, 0)} kişi")
print(f"  Hayatını kaybeden : {survived_counts.get(0, 0)} kişi")
print(f"  Hayatta kalma %   : {(survived_counts.get(1, 0) / len(df) * 100):.1f}%")

# ─────────────────────────────────────────
# 3. GRAFİKLER
# ─────────────────────────────────────────
print("\n[6] GRAFİKLER OLUŞTURULUYOR...")

output_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
os.makedirs(output_dir, exist_ok=True)

fig, axes = plt.subplots(2, 3, figsize=(16, 10))
fig.suptitle('Titanic Veri Seti — Keşifsel Veri Analizi (EDA)', fontsize=16, fontweight='bold')

# Grafik 1: Genel Hayatta Kalma Oranı
axes[0, 0].bar(['Hayatını Kaybetti', 'Hayatta Kaldı'],
               [survived_counts.get(0, 0), survived_counts.get(1, 0)],
               color=['#e74c3c', '#2ecc71'], edgecolor='white', linewidth=1.5)
axes[0, 0].set_title('Hayatta Kalma Durumu', fontweight='bold')
axes[0, 0].set_ylabel('Yolcu Sayısı')
for i, v in enumerate([survived_counts.get(0, 0), survived_counts.get(1, 0)]):
    axes[0, 0].text(i, v + 5, str(v), ha='center', fontweight='bold')

# Grafik 2: Cinsiyete Göre Hayatta Kalma
sex_survived = df.groupby(['Sex', 'Survived']).size().unstack(fill_value=0)
sex_survived.plot(kind='bar', ax=axes[0, 1],
                  color=['#e74c3c', '#2ecc71'],
                  edgecolor='white', legend=True)
axes[0, 1].set_title('Cinsiyete Göre Hayatta Kalma', fontweight='bold')
axes[0, 1].set_ylabel('Yolcu Sayısı')
axes[0, 1].set_xticklabels(['Kadın', 'Erkek'], rotation=0)
axes[0, 1].legend(['Hayatını Kaybetti', 'Hayatta Kaldı'])

# Grafik 3: Yolcu Sınıfına Göre Hayatta Kalma
pclass_survived = df.groupby(['Pclass', 'Survived']).size().unstack(fill_value=0)
pclass_survived.plot(kind='bar', ax=axes[0, 2],
                     color=['#e74c3c', '#2ecc71'],
                     edgecolor='white', legend=True)
axes[0, 2].set_title('Sınıfa Göre Hayatta Kalma', fontweight='bold')
axes[0, 2].set_ylabel('Yolcu Sayısı')
axes[0, 2].set_xticklabels(['1. Sınıf', '2. Sınıf', '3. Sınıf'], rotation=0)
axes[0, 2].legend(['Hayatını Kaybetti', 'Hayatta Kaldı'])

# Grafik 4: Yaş Dağılımı
axes[1, 0].hist(df[df['Survived'] == 1]['Age'].dropna(), bins=25,
                alpha=0.7, color='#2ecc71', label='Hayatta Kaldı')
axes[1, 0].hist(df[df['Survived'] == 0]['Age'].dropna(), bins=25,
                alpha=0.7, color='#e74c3c', label='Hayatını Kaybetti')
axes[1, 0].set_title('Yaşa Göre Hayatta Kalma Dağılımı', fontweight='bold')
axes[1, 0].set_xlabel('Yaş')
axes[1, 0].set_ylabel('Yolcu Sayısı')
axes[1, 0].legend()

# Grafik 5: Bilet Ücreti Dağılımı
axes[1, 1].hist(df['Fare'].dropna(), bins=40, color='#3498db', edgecolor='white')
axes[1, 1].set_title('Bilet Ücreti Dağılımı', fontweight='bold')
axes[1, 1].set_xlabel('Ücret ($)')
axes[1, 1].set_ylabel('Yolcu Sayısı')

# Grafik 6: Korelasyon Matrisi
numeric_cols = ['Survived', 'Pclass', 'Age', 'SibSp', 'Parch', 'Fare']
corr_data = df[numeric_cols].dropna()
corr_matrix = corr_data.corr()
sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='RdYlGn',
            ax=axes[1, 2], square=True, linewidths=0.5)
axes[1, 2].set_title('Korelasyon Matrisi', fontweight='bold')

plt.tight_layout()
output_path = os.path.join(output_dir, 'eda_grafikleri.png')
plt.savefig(output_path, dpi=150, bbox_inches='tight')
print(f"  [✓] Grafik kaydedildi: {output_path}")

print("\n" + "=" * 60)
print("EDA TAMAMLANDI!")
print("  → data/titanic.csv       : Veri seti")
print("  → data/eda_grafikleri.png: Görsel analiz grafikler")
print("  → Sonraki adım: model/train_model.py çalıştırın")
print("=" * 60)
