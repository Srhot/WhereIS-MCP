from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict, Any, Optional
import os
from dotenv import load_dotenv
from .services.geological_service import GeologicalService
from .schemas.geological_schemas import LocationResponse, LocationData
import asyncio
import json
import websockets
import httpx

# .env dosyasını yükle
load_dotenv()

app = FastAPI(
    title="Konum Veri MCP Sunucusu",
    description="Konum verilerini işleyen ve sunan Model Context Protocol sunucusu",
    version="1.0.0"
)

# CORS ayarları
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Geliştirme için tüm originlere izin ver
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Servis bağımlılığı
def get_location_service():
    return GeologicalService()

# API endpoint'leri
@app.get("/")
async def root():
    return {"message": "Konum Veri MCP Sunucusuna Hoş Geldiniz"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/location/{location_name}", response_model=LocationResponse)
async def get_location_data(
    location_name: str,
    location_service: GeologicalService = Depends(get_location_service)
):
    """
    Belirtilen konum için detaylı lokasyon verilerini getirir.
    
    Args:
        location_name (str): Aranacak konum adı
        
    Returns:
        LocationResponse: Konum verileri
    """
    try:
        return await location_service.get_location_data(location_name)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

class GeologicalApp:
    def __init__(self, base_url: str = None):
        # Smithery URL'sini çevre değişkeninden al veya varsayılan değeri kullan
        self.base_url = base_url or os.getenv("MCP_SERVER_URL", "http://localhost:8000")
        self.client = httpx.AsyncClient(base_url=self.base_url)
        
    async def get_location_data(self, location: str) -> Dict:
        """Belirtilen konum için veri alır"""
        try:
            response = await self.client.post(
                "/api/geological-data",
                json={"location": location}
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {
                "status": "error",
                "message": f"Veri alınamadı: {str(e)}"
            }
        
    async def update_context(self, context_data: Dict) -> Dict:
        """İstemci bağlamını günceller"""
        try:
            response = await self.client.post(
                "/api/context-update",
                json={"context": context_data}
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {
                "status": "error",
                "message": f"Bağlam güncellenemedi: {str(e)}"
            }
            
    async def close(self):
        """HTTP istemcisini kapatır"""
        await self.client.aclose()

# Örnek kullanım
async def main():
    app = GeologicalApp()
    
    try:
        # Konum verisi al
        location_data = await app.get_location_data("Istanbul")
        print("Konum verisi:", location_data)
        
        # Bağlam güncelle
        await app.update_context({
            "last_search": "Istanbul",
            "preferences": {
                "language": "tr",
                "units": "metric"
            }
        })
        
    finally:
        await app.close()

if __name__ == "__main__":
    asyncio.run(main()) 