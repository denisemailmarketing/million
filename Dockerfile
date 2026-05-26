FROM python:3.11-slim

# Çalışma dizini
WORKDIR /app

# Önce sadece requirements kopyala (Docker cache'den faydalanmak için)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Proje dosyalarını kopyala
COPY . .

# DB_PATH ortam değişkeni Railway Variables'tan gelir
# Varsayılan: /app/game.db (Railway Volumes ile override edilebilir)
ENV DB_PATH=/app/game.db

CMD ["python", "main.py"]
