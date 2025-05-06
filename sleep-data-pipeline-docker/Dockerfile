# 1. Hafif bir Python imajı
FROM python:3.10-slim

# 2. Çalışma dizinini oluştur ve ayarla
WORKDIR /app

# 3. Bağımlılıkları kopyala ve yükle
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Uygulamayı kopyala
COPY ingest.py .

# 5. Container başladığında çalıştır
CMD ["python", "ingest.py"]

