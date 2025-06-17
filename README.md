[![MseeP.ai Security Assessment Badge](https://mseep.net/pr/srhot-whereis-mcp-badge.png)](https://mseep.ai/app/srhot-whereis-mcp)

# Jeolojik Veri MCP Sunucusu

Bu proje, jeolojik verileri işleyen ve sunan bir Model Context Protocol (MCP) sunucusudur. Sunucu, konum bazlı jeolojik verileri HTTP ve WebSocket protokolleri üzerinden sunar.

## Özellikler

- HTTP ve WebSocket desteği
- Konum bazlı jeolojik veri sorgulama
- Bağlam (context) yönetimi
- Asenkron işlem desteği
- RESTful API endpoint'leri
- CORS desteği
- Hata yönetimi
- Çevre değişkenleri ile yapılandırma

## Teknolojiler

- Python 3.8+
- FastAPI
- Uvicorn
- HTTPX
- Pydantic
- Python-dotenv

## Kurulum

1. Projeyi klonlayın:
```bash
git clone https://github.com/kullanici-adi/WhereIs.git
cd WhereIs
```

2. Sanal ortam oluşturun ve aktive edin:
```bash
# Windows için:
python -m venv venv
venv\Scripts\activate

# Linux/Mac için:
python -m venv venv
source venv/bin/activate
```

3. Gerekli paketleri yükleyin:
```bash
pip install -r requirements.txt
```

4. `.env` dosyasını oluşturun:
```bash
# .env dosyası örneği
GEOLOGICAL_API_KEY=your_api_key_here
GEOLOGICAL_API_BASE_URL=https://api.example.com
APP_ENV=development
DEBUG=True
PORT=8000
```

## Kullanım

### Sunucuyu Başlatma

```bash
python -m mcp_server.server
```

Sunucu varsayılan olarak http://localhost:8000 adresinde çalışacaktır.

### Uygulamayı Çalıştırma

```bash
python -m app.main
```

### API Endpoint'leri

#### HTTP Endpoint'leri

- `GET /`: Ana sayfa
- `GET /health`: Sağlık kontrolü
- `POST /api/geological-data`: Jeolojik veri sorgulama
- `POST /api/context-update`: Bağlam güncelleme

#### WebSocket Endpoint'i

- `WS /ws`: WebSocket bağlantısı

### Örnek İstekler

#### Jeolojik Veri Sorgulama

```bash
curl -X POST http://localhost:8000/api/geological-data \
  -H "Content-Type: application/json" \
  -d '{"location": "Istanbul"}'
```

#### Bağlam Güncelleme

```bash
curl -X POST http://localhost:8000/api/context-update \
  -H "Content-Type: application/json" \
  -d '{"context": {"language": "tr", "units": "metric"}}'
```

## Proje Yapısı

```
WhereIs/
├── app/                    # Uygulama kodu
│   ├── __init__.py
│   └── main.py            # Ana uygulama
├── mcp_server/            # MCP sunucu kodu
│   ├── __init__.py
│   └── server.py          # Sunucu uygulaması
├── .env                   # Çevre değişkenleri (git'e eklenmez)
├── .gitignore            # Git tarafından yok sayılacak dosyalar
├── README.md             # Bu dosya
└── requirements.txt      # Proje bağımlılıkları
```

## Geliştirme

1. Yeni bir branch oluşturun:
```bash
git checkout -b feature/yeni-ozellik
```

2. Değişikliklerinizi yapın ve commit edin:
```bash
git add .
git commit -m "Yeni özellik: [özellik açıklaması]"
```

3. Branch'inizi push edin:
```bash
git push origin feature/yeni-ozellik
```

## Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Detaylar için [LICENSE](LICENSE) dosyasına bakın.

## Katkıda Bulunma

1. Bu repository'yi fork edin
2. Yeni bir branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Değişikliklerinizi commit edin (`git commit -m 'Add some amazing feature'`)
4. Branch'inizi push edin (`git push origin feature/amazing-feature`)
5. Bir Pull Request oluşturun 