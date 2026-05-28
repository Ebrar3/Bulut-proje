"""
PROJE-4: Auto Scaling CPU Stres Testi
======================================
Bu script, Load Balancer adresine sürekli istek atarak
sunucu CPU kullanımını artırır ve Auto Scaling'i tetikler.

Kullanım:
    python stress_test.py --url http://<ALB_DNS_ADRESİ> --workers 10 --duration 120

Parametreler:
    --url       : Load Balancer'ın DNS adresi (http://... ile başlamalı)
    --workers   : Aynı anda çalışacak thread sayısı (varsayılan: 10)
    --duration  : Test süresi saniye cinsinden (varsayılan: 120)
"""

import threading
import time
import argparse
import requests
import sys
from datetime import datetime

# ─────────────────────────────────────────
# Argüman Ayarları
# ─────────────────────────────────────────
parser = argparse.ArgumentParser(description="CloudShop Auto Scaling Stres Testi")
parser.add_argument("--url", type=str, default="http://localhost:80",
                    help="Load Balancer DNS adresi (örn: http://my-alb-123.eu-central-1.elb.amazonaws.com)")
parser.add_argument("--workers", type=int, default=10,
                    help="Eş zamanlı istek gönderen thread sayısı (varsayılan: 10)")
parser.add_argument("--duration", type=int, default=120,
                    help="Test süresi (saniye) (varsayılan: 120)")
args = parser.parse_args()

# ─────────────────────────────────────────
# Global Sayaçlar
# ─────────────────────────────────────────
stats = {
    "total_requests": 0,
    "successful": 0,
    "failed": 0,
    "servers_seen": set(),
    "lock": threading.Lock()
}

start_time = time.time()
stop_event = threading.Event()

# ─────────────────────────────────────────
# İstek Gönderici (Her Thread Bunu Çalıştırır)
# ─────────────────────────────────────────
def send_requests(worker_id):
    """Sürekli istek gönderen thread fonksiyonu."""
    session = requests.Session()

    while not stop_event.is_set():
        try:
            # Ana sayfaya istek at
            response = session.get(args.url, timeout=5)

            with stats["lock"]:
                stats["total_requests"] += 1

                if response.status_code == 200:
                    stats["successful"] += 1
                else:
                    stats["failed"] += 1

            # Ayrıca /stress endpoint'ini de tetikle (CPU yükü oluşturur)
            try:
                session.get(f"{args.url}/stress?duration=10", timeout=3)
            except Exception:
                pass

        except requests.exceptions.RequestException:
            with stats["lock"]:
                stats["total_requests"] += 1
                stats["failed"] += 1

        time.sleep(0.05)  # Çok agresif olmamak için kısa bekleme

# ─────────────────────────────────────────
# Sunucu ID Takipçisi
# ─────────────────────────────────────────
def track_servers():
    """Hangi sunuculara bağlandığımızı takip eder."""
    session = requests.Session()

    while not stop_event.is_set():
        try:
            response = session.get(f"{args.url}/server-info", timeout=5)
            if response.status_code == 200:
                data = response.json()
                instance_id = data.get("instance_id", "bilinmiyor")
                ip = data.get("ip", "")

                with stats["lock"]:
                    if instance_id not in stats["servers_seen"]:
                        stats["servers_seen"].add(instance_id)
                        print(f"\n  🆕 YENİ SUNUCU ALGILANDI: {instance_id} ({ip})")
        except Exception:
            pass

        time.sleep(5)  # Her 5 saniyede bir kontrol

# ─────────────────────────────────────────
# İstatistik Gösterici
# ─────────────────────────────────────────
def print_stats():
    """Her 10 saniyede bir özet gösterir."""
    while not stop_event.is_set():
        time.sleep(10)
        if stop_event.is_set():
            break

        elapsed = time.time() - start_time
        remaining = max(0, args.duration - elapsed)

        with stats["lock"]:
            total = stats["total_requests"]
            success = stats["successful"]
            failed = stats["failed"]
            rps = total / max(elapsed, 1)
            servers = len(stats["servers_seen"])

        print(f"\n  ─── [{datetime.now().strftime('%H:%M:%S')}] İstatistikler ───")
        print(f"  ⏱  Geçen süre   : {elapsed:.0f}s / {args.duration}s (kalan: {remaining:.0f}s)")
        print(f"  📊 Toplam istek  : {total}")
        print(f"  ✅ Başarılı      : {success}")
        print(f"  ❌ Başarısız     : {failed}")
        print(f"  ⚡ İstek/saniye  : {rps:.1f}")
        print(f"  🖥  Görülen sunucu: {servers} adet {list(stats['servers_seen'])}")

# ─────────────────────────────────────────
# ANA PROGRAM
# ─────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 60)
    print("  ☁️  CLOUDSHOP AUTO SCALING STRES TESTİ")
    print("=" * 60)
    print(f"  Hedef URL   : {args.url}")
    print(f"  Thread sayısı: {args.workers}")
    print(f"  Test süresi  : {args.duration} saniye")
    print()
    print("  ℹ️  Bu test:")
    print("     1. Load Balancer'a çok sayıda istek gönderir")
    print("     2. /stress endpoint'ini tetikleyerek CPU'yu artırır")
    print("     3. CPU > %%50 olunca AWS otomatik yeni sunucu açar")
    print("     4. Yeni sunucular algılandığında bildirim verir")
    print()
    print("  AWS Console → EC2 → Auto Scaling Groups → Activity")
    print("  sekmesini açık tutun ve yeni instance'ların açıldığını izleyin!")
    print()
    print("  Başlıyor...")
    print("=" * 60)

    # Threadleri başlat
    threads = []

    # İstek gönderici thread'ler
    for i in range(args.workers):
        t = threading.Thread(target=send_requests, args=(i,), daemon=True)
        t.start()
        threads.append(t)

    # Sunucu takipçisi
    tracker = threading.Thread(target=track_servers, daemon=True)
    tracker.start()

    # İstatistik gösterici
    stats_printer = threading.Thread(target=print_stats, daemon=True)
    stats_printer.start()

    # Test süresince bekle
    try:
        time.sleep(args.duration)
    except KeyboardInterrupt:
        print("\n\n  ⚠️  Test kullanıcı tarafından durduruldu.")

    # Testleri durdur
    stop_event.set()
    time.sleep(2)

    # Final raporu
    elapsed = time.time() - start_time
    print("\n" + "=" * 60)
    print("  📋 TEST TAMAMLANDI — ÖZET RAPOR")
    print("=" * 60)
    print(f"  Toplam süre    : {elapsed:.1f} saniye")
    print(f"  Toplam istek   : {stats['total_requests']}")
    print(f"  Başarılı       : {stats['successful']}")
    print(f"  Başarısız      : {stats['failed']}")
    print(f"  Ort. istek/sn  : {stats['total_requests']/elapsed:.1f}")
    print(f"  Görülen sunucu : {len(stats['servers_seen'])} adet")
    for srv in stats["servers_seen"]:
        print(f"                   → {srv}")
    print()
    if len(stats["servers_seen"]) > 1:
        print("  ✅ AUTO SCALING ÇALIŞTI! Birden fazla sunucu tespit edildi.")
        print("     AWS otomatik olarak yeni EC2 instance'ları açtı.")
    else:
        print("  ⏳ Tek sunucu görüldü. Auto Scaling henüz tetiklenmedi.")
        print("     CPU alarm süresi 3-5 dakika sürebilir. Konsolu kontrol edin.")
    print("=" * 60)
