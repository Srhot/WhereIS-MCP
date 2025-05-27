# Python 3.8 base image
FROM python:3.8-slim

# Sistem bağımlılıklarını yükle
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Çalışma dizinini ayarla
WORKDIR /app

# Önce sadece requirements.txt'yi kopyala
COPY requirements.txt .

# Bağımlılıkları yükle
RUN pip install --no-cache-dir -r requirements.txt

# Sonra diğer dosyaları kopyala
COPY . .

# Port ayarı
ENV PORT=8081
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Uygulamayı çalıştır
CMD ["sh", "-c", "uvicorn mcp_server.server:app --host 0.0.0.0 --port ${PORT:-8081} --workers 1"] 