#!/bin/bash
# ============================================================
# PROJE-4: EC2 User Data Script (Otomatik Kurulum)
# ============================================================
# Bu script, yeni bir EC2 sunucusu açıldığında otomatik
# çalışır. GitHub'dan projeyi indirir ve Flask uygulamasını
# başlatır. Auto Scaling Group bunu kullanacak.
# ============================================================

# Sistem güncellemeleri
yum update -y

# Python ve pip
yum install -y python3 python3-pip git

# GitHub'dan proje kodlarını indir
cd /home/ec2-user
git clone https://github.com/Ebrar3/Bulut-proje.git
cd Bulut-proje/FİNAL/PROJE-4

# Gereksinimleri yükle
pip3 install -r requirements.txt

# Flask uygulamasını 80 portunda başlat (arka planda)
# nohup: terminal kapansa bile çalışmaya devam eder
nohup python3 app.py > /var/log/cloudshop.log 2>&1 &

echo "CloudShop başarıyla başlatıldı!" >> /var/log/cloudshop.log
