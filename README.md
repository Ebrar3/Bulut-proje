# 📝 Bulut Not Uygulaması

AWS üzerinde çalışan, MongoDB veritabanı kullanan tam yığın not tutma uygulaması.

- **Backend:** Python / FastAPI
- **Veritabanı:** MongoDB (Motor async driver)
- **Frontend:** React (Vite)
- **Altyapı:** AWS ECS Fargate + CloudFormation

---

## 🏗️ Mimari

```
[React Frontend]  →  [FastAPI Backend]  →  [MongoDB]
     nginx               uvicorn            Atlas / Docker
       ↕
  AWS ALB  →  ECS Fargate (Fargate tasks)
```

---

## 🚀 Yerel Geliştirme (Docker Compose)

### Gereksinimler
- Docker & Docker Compose

### Başlatma

```bash
# Tüm servisleri başlat (MongoDB + Backend + Frontend)
docker-compose up --build

# Arka planda çalıştır
docker-compose up -d --build
```

Uygulamaya erişim:
| Servis | URL |
|---|---|
| Frontend | http://localhost:3000 |
| Backend API | http://localhost:8000 |
| API Docs | http://localhost:8000/docs |

---

## 💻 Manuel Geliştirme

### Backend

```bash
cd backend

# Sanal ortam oluştur
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Bağımlılıkları yükle
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Ortam değişkenlerini ayarla
cp .env.example .env

# Sunucuyu başlat
uvicorn app.main:app --reload --port 8000
```

### Backend Testleri

```bash
cd backend
pytest
```

### Frontend

```bash
cd frontend

# Bağımlılıkları yükle
npm install

# Ortam değişkenlerini ayarla
cp .env.example .env

# Geliştirme sunucusunu başlat
npm run dev
```

---

## 🌐 AWS Dağıtımı

### Ön Koşullar
- AWS CLI yapılandırılmış
- Docker imajları ECR'ye yüklenmiş
- MongoDB Atlas veya AWS DocumentDB hazır

### ECR'ye İmaj Yükleme

```bash
# Backend
aws ecr create-repository --repository-name notes-backend
docker build -t notes-backend ./backend
docker tag notes-backend:latest <AWS_ACCOUNT_ID>.dkr.ecr.<REGION>.amazonaws.com/notes-backend:latest
docker push <AWS_ACCOUNT_ID>.dkr.ecr.<REGION>.amazonaws.com/notes-backend:latest

# Frontend
aws ecr create-repository --repository-name notes-frontend
docker build -t notes-frontend ./frontend
docker tag notes-frontend:latest <AWS_ACCOUNT_ID>.dkr.ecr.<REGION>.amazonaws.com/notes-frontend:latest
docker push <AWS_ACCOUNT_ID>.dkr.ecr.<REGION>.amazonaws.com/notes-frontend:latest
```

### CloudFormation ile Dağıtım

```bash
aws cloudformation deploy \
  --template-file aws/cloudformation.yml \
  --stack-name notes-app \
  --capabilities CAPABILITY_NAMED_IAM \
  --parameter-overrides \
    MongoDBURL="mongodb+srv://user:pass@cluster.mongodb.net" \
    BackendImage="<AWS_ACCOUNT_ID>.dkr.ecr.<REGION>.amazonaws.com/notes-backend:latest" \
    FrontendImage="<AWS_ACCOUNT_ID>.dkr.ecr.<REGION>.amazonaws.com/notes-frontend:latest" \
    VpcId="vpc-xxxxxxxx" \
    SubnetIds="subnet-aaaa,subnet-bbbb"
```

---

## 📡 API Endpointleri

| Yöntem | Endpoint | Açıklama |
|---|---|---|
| GET | `/api/notes/` | Tüm notları listele |
| GET | `/api/notes/{id}` | Tek not getir |
| POST | `/api/notes/` | Yeni not oluştur |
| PUT | `/api/notes/{id}` | Notu güncelle |
| DELETE | `/api/notes/{id}` | Notu sil |
| GET | `/api/notes/tags/all` | Tüm etiketleri getir |
| GET | `/health` | Sağlık kontrolü |

Tam API dokümantasyonu: `http://localhost:8000/docs`

---

## 📁 Proje Yapısı

```
.
├── backend/
│   ├── app/
│   │   ├── main.py          # FastAPI uygulaması
│   │   ├── database.py      # MongoDB bağlantısı
│   │   ├── models.py        # Pydantic modelleri
│   │   └── routes/
│   │       └── notes.py     # Not CRUD endpoint'leri
│   ├── tests/
│   │   └── test_notes.py    # API testleri
│   ├── Dockerfile
│   ├── requirements.txt
│   └── requirements-dev.txt
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── NoteCard.jsx
│   │   │   ├── NoteDetail.jsx
│   │   │   ├── NoteForm.jsx
│   │   │   └── NoteList.jsx
│   │   ├── services/
│   │   │   └── notesApi.js
│   │   ├── App.jsx
│   │   └── App.css
│   ├── Dockerfile
│   └── nginx.conf
├── aws/
│   └── cloudformation.yml   # AWS altyapı şablonu
└── docker-compose.yml       # Yerel geliştirme
```
