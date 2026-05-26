FROM python:3.11-slim

# Çalışma dizini
WORKDIR /app

# Önce sadece requirements kopyala (Docker cache'den faydalanmak için)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Proje dosyalarını kopyala
COPY . .

# SQLite dosyası için volume mount noktası
VOLUME ["/app/data"]

# Ortam değişkeni: DB yolunu /app/data altına taşı
# (Railway'de /app yazılabilir, ama data klasörü daha temiz)
ENV DB_PATH=/app/data/game.db

CMD ["python", "main.py"]
