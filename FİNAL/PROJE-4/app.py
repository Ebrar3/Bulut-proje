"""
PROJE-4: E-Ticaret Uygulaması
AWS EC2 + Application Load Balancer + Auto Scaling

Bu dosya Flask web uygulamasıdır.
Her sunucu kendi ID'sini ve IP'sini sayfada gösterir.
Bu sayede Load Balancer'ın bizi farklı sunuculara yönlendirdiğini görebiliriz.
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import socket
import requests
import os
import math
import threading
import time

app = Flask(__name__)
app.secret_key = "proje4-bulut-bilisim-2026"

# ─────────────────────────────────────────
# Sunucu bilgilerini al (EC2 metadata)
# ─────────────────────────────────────────
def get_instance_id():
    """AWS EC2 metadata servisinden instance ID'sini alır."""
    try:
        # IMDSv2 token al
        token_response = requests.put(
            "http://169.254.169.254/latest/api/token",
            headers={"X-aws-ec2-metadata-token-ttl-seconds": "21600"},
            timeout=2
        )
        token = token_response.text
        # Instance ID'yi al
        response = requests.get(
            "http://169.254.169.254/latest/meta-data/instance-id",
            headers={"X-aws-ec2-metadata-token": token},
            timeout=2
        )
        return response.text
    except Exception:
        return socket.gethostname()  # Yerel geliştirmede hostname döner

def get_instance_ip():
    """EC2 özel IP adresini alır."""
    try:
        token_response = requests.put(
            "http://169.254.169.254/latest/api/token",
            headers={"X-aws-ec2-metadata-token-ttl-seconds": "21600"},
            timeout=2
        )
        token = token_response.text
        response = requests.get(
            "http://169.254.169.254/latest/meta-data/local-ipv4",
            headers={"X-aws-ec2-metadata-token": token},
            timeout=2
        )
        return response.text
    except Exception:
        return socket.gethostbyname(socket.gethostname())

def get_az():
    """EC2 Availability Zone bilgisini alır."""
    try:
        token_response = requests.put(
            "http://169.254.169.254/latest/api/token",
            headers={"X-aws-ec2-metadata-token-ttl-seconds": "21600"},
            timeout=2
        )
        token = token_response.text
        response = requests.get(
            "http://169.254.169.254/latest/meta-data/placement/availability-zone",
            headers={"X-aws-ec2-metadata-token": token},
            timeout=2
        )
        return response.text
    except Exception:
        return "eu-central-1a"

# ─────────────────────────────────────────
# Ürün Kataloğu
# ─────────────────────────────────────────
PRODUCTS = [
    {
        "id": 1,
        "name": "AWS EC2 T3 Micro Kuponlu Laptop",
        "description": "Bulut bilişim öğrencilerine özel, yüksek performanslı geliştirici dizüstü bilgisayarı.",
        "price": 12999,
        "original_price": 15999,
        "emoji": "💻",
        "badge": "İndirim",
        "badge_color": "red",
        "stock": 8
    },
    {
        "id": 2,
        "name": "Auto Scaling Akıllı Monitör 27\"",
        "description": "Trafik yoğunluğuna göre otomatik parlaklık ayarlayan, gözlere zararsız 4K ekran.",
        "price": 6499,
        "original_price": 7999,
        "emoji": "🖥️",
        "badge": "Çok Satan",
        "badge_color": "blue",
        "stock": 15
    },
    {
        "id": 3,
        "name": "Load Balancer Mekanik Klavye",
        "description": "Tuş vuruşlarını tüm parmaklara eşit dağıtan, RGB aydınlatmalı mekanik klavye.",
        "price": 2199,
        "original_price": 2199,
        "emoji": "⌨️",
        "badge": "Yeni",
        "badge_color": "green",
        "stock": 23
    },
    {
        "id": 4,
        "name": "S3 Depolama Harici SSD 2TB",
        "description": "Sonsuz ölçeklenebilirlik konseptinden ilham alan, yüksek hızlı taşınabilir depolama.",
        "price": 1799,
        "original_price": 2299,
        "emoji": "💾",
        "badge": "İndirim",
        "badge_color": "red",
        "stock": 42
    },
    {
        "id": 5,
        "name": "Lambda Serverless Kulaklık",
        "description": "Sadece müzik çalarken güç tüketen, aktif gürültü engelleyici kablosuz kulaklık.",
        "price": 3299,
        "original_price": 3299,
        "emoji": "🎧",
        "badge": "Öne Çıkan",
        "badge_color": "purple",
        "stock": 11
    },
    {
        "id": 6,
        "name": "CloudWatch Akıllı Kamera",
        "description": "7/24 izleme, anlık uyarı ve otomatik kayıt özellikleriyle güvenlik kamerası.",
        "price": 899,
        "original_price": 1299,
        "emoji": "📷",
        "badge": "Fırsat",
        "badge_color": "orange",
        "stock": 5
    },
]

# ─────────────────────────────────────────
# Route'lar (URL Yönlendirmeleri)
# ─────────────────────────────────────────

@app.route("/")
def index():
    """Ana sayfa — ürün listeleme."""
    cart = session.get("cart", {})
    cart_count = sum(cart.values())

    server_info = {
        "instance_id": get_instance_id(),
        "ip": get_instance_ip(),
        "az": get_az(),
        "hostname": socket.gethostname()
    }

    return render_template(
        "index.html",
        products=PRODUCTS,
        cart_count=cart_count,
        server_info=server_info
    )

@app.route("/cart")
def cart():
    """Sepet sayfası."""
    cart_data = session.get("cart", {})
    cart_items = []
    total = 0

    for product_id, quantity in cart_data.items():
        product = next((p for p in PRODUCTS if p["id"] == int(product_id)), None)
        if product:
            subtotal = product["price"] * quantity
            cart_items.append({**product, "quantity": quantity, "subtotal": subtotal})
            total += subtotal

    server_info = {
        "instance_id": get_instance_id(),
        "ip": get_instance_ip(),
    }

    return render_template("cart.html", cart_items=cart_items, total=total, server_info=server_info)

@app.route("/add_to_cart/<int:product_id>", methods=["POST"])
def add_to_cart(product_id):
    """Ürünü sepete ekle."""
    cart = session.get("cart", {})
    key = str(product_id)
    cart[key] = cart.get(key, 0) + 1
    session["cart"] = cart
    session.modified = True
    return redirect(url_for("index"))

@app.route("/remove_from_cart/<int:product_id>", methods=["POST"])
def remove_from_cart(product_id):
    """Ürünü sepetten çıkar."""
    cart = session.get("cart", {})
    key = str(product_id)
    if key in cart:
        del cart[key]
    session["cart"] = cart
    session.modified = True
    return redirect(url_for("cart"))

@app.route("/clear_cart", methods=["POST"])
def clear_cart():
    """Sepeti temizle."""
    session["cart"] = {}
    return redirect(url_for("cart"))

@app.route("/health")
def health():
    """Load Balancer sağlık kontrolü — ALB bu endpoint'i sürekli kontrol eder."""
    return jsonify({
        "status": "healthy",
        "instance_id": get_instance_id(),
        "ip": get_instance_ip()
    }), 200

@app.route("/stress")
def stress():
    """
    CPU stres testi endpoint'i.
    Bu endpoint'e istek gelince CPU %100'e çıkar.
    Auto Scaling bunu tetiklemek için kullanılır.
    """
    duration = int(request.args.get("duration", 30))  # saniye cinsinden
    duration = min(duration, 120)  # maksimum 2 dakika

    def cpu_burner(seconds):
        end_time = time.time() + seconds
        while time.time() < end_time:
            # Matematiksel işlem yaparak CPU'yu meşgul et
            [math.sqrt(i) for i in range(10000)]

    thread = threading.Thread(target=cpu_burner, args=(duration,))
    thread.daemon = True
    thread.start()

    return jsonify({
        "status": "stress_started",
        "duration_seconds": duration,
        "instance_id": get_instance_id(),
        "message": f"CPU {duration} saniye boyunca %100'de çalışacak. Auto Scaling tetiklenecek!"
    })

@app.route("/server-info")
def server_info():
    """Sunucu bilgilerini JSON olarak döndür."""
    return jsonify({
        "instance_id": get_instance_id(),
        "ip": get_instance_ip(),
        "az": get_az(),
        "hostname": socket.gethostname()
    })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 80))
    app.run(host="0.0.0.0", port=port, debug=False)
