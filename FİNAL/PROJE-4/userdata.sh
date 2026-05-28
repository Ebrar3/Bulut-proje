#!/bin/bash
set -e

# Logları kaydet
exec > /var/log/cloudshop-setup.log 2>&1
echo "=== CloudShop Kurulum Basladi: $(date) ==="

# Sistem güncellemeleri
yum update -y
yum install -y python3 python3-pip git

echo "=== Python ve Git kuruldu ==="

# GitHub'dan projeyi indir
cd /home/ec2-user
git clone https://github.com/Ebrar3/Bulut-proje.git

echo "=== GitHub clone tamam ==="

# PROJE-4 klasorune gec (ASCII path ile)
# Turkce karakter sorunu icin find kullan
PROJE4_PATH=$(find /home/ec2-user/Bulut-proje -type d -name "PROJE-4" | head -1)
echo "PROJE-4 yolu: $PROJE4_PATH"
cd "$PROJE4_PATH"

echo "=== Dizin: $(pwd) ==="

# Gereksinimleri yukle
pip3 install flask requests

echo "=== Python paketler kuruldu ==="

# Flask uygulamasini 80 portunda baslat
nohup python3 app.py > /var/log/cloudshop-app.log 2>&1 &
APP_PID=$!
echo "=== Flask basladi, PID: $APP_PID ==="

# 5 saniye bekle ve kontrol et
sleep 5
if kill -0 $APP_PID 2>/dev/null; then
    echo "=== BASARILI: Flask calisiyor ==="
else
    echo "=== HATA: Flask cakti! Log: ==="
    cat /var/log/cloudshop-app.log
fi

echo "=== Kurulum Tamamlandi: $(date) ==="
