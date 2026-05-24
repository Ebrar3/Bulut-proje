import boto3
import json
import random
import time
from datetime import datetime

# Kinesis istemcisini oluşturuyoruz
kinesis = boto3.client('kinesis', region_name='us-east-1') # Bölgeni kontrol et
STREAM_NAME = 'HavaKalitesiAkisi'

def generate_sensor_data():
    """Rastgele hava kalitesi verisi üretir."""
    sensors = ['SENSOR_ANK_01', 'SENSOR_ANK_02', 'SENSOR_ANK_03']
    return {
        'sensor_id': random.choice(sensors),
        'temperature': round(random.uniform(15.0, 30.0), 2),
        'pm25': round(random.uniform(5.0, 50.0), 2), # Hava kirliliği oranı
        'co2': random.randint(350, 1000), # Karbon oranı
        'timestamp': datetime.now().isoformat()
    }

def start_simulating():
    print(f"📡 {STREAM_NAME} kanalına veri gönderimi başlıyor...")
    try:
        while True:
            data = generate_sensor_data()
            
            # Veriyi Kinesis'e gönderiyoruz
            response = kinesis.put_record(
                StreamName=STREAM_NAME,
                Data=json.dumps(data),
                PartitionKey=data['sensor_id']
            )
            
            print(f"✅ Veri Gönderildi: {data['sensor_id']} -> PM2.5: {data['pm25']}")
            time.sleep(2) # 2 saniyede bir veri gönder
            
    except KeyboardInterrupt:
        print("\n🛑 Simülasyon durduruldu.")

if __name__ == "__main__":
    start_simulating()