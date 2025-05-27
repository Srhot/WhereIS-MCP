# Python 3.8 base image
FROM python:3.8-slim

# Çalışma dizinini ayarla
WORKDIR /app

# Gerekli dosyaları kopyala
COPY requirements.txt .
COPY . .

# Bağımlılıkları yükle
RUN pip install --no-cache-dir -r requirements.txt

# Port ayarı
ENV PORT=8081

# Uygulamayı çalıştır
CMD uvicorn mcp_server.server:app --host 0.0.0.0 --port $PORT 