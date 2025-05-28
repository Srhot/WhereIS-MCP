# Python 3.8 base image
FROM python:3.8-slim

# Çalışma dizinini ayarla
WORKDIR /app

# Önce sadece requirements.txt'yi kopyala
COPY requirements.txt .

# Bağımlılıkları yükle
RUN pip install --no-cache-dir -r requirements.txt

# Sonra diğer dosyaları kopyala
COPY . .

# Port ayarı
ENV PORT=80

# Gunicorn ile çalıştır (Komut smithery.yaml tarafından sağlanacak)
# CMD gunicorn mcp_server.server:app --bind 0.0.0.0:$PORT --worker-class uvicorn.workers.UvicornWorker --workers 1 --timeout 120 