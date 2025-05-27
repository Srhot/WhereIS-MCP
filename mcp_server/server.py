import asyncio
import json
import os
from datetime import datetime
from typing import Dict, Any, Optional
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

class MCPServer:
    def __init__(self):
        self.clients: Dict[str, Dict] = {}
        self.context: Dict[str, Any] = {}
        
    async def connect_client(self, client_id: str):
        """Yeni istemci bağlantısını yönetir"""
        self.clients[client_id] = {
            "connected_at": datetime.now(),
            "context": {},
            "websocket": None
        }
        
    async def disconnect_client(self, client_id: str):
        """İstemci bağlantısını sonlandırır"""
        if client_id in self.clients:
            del self.clients[client_id]
            
    async def update_context(self, client_id: str, context_data: Dict):
        """İstemci bağlamını günceller"""
        if client_id in self.clients:
            self.clients[client_id]["context"].update(context_data)
            
    async def handle_request(self, request: Dict) -> Dict:
        """MCP isteklerini işler"""
        request_type = request.get("type")
        data = request.get("data", {})
        
        if request_type == "geological_data":
            return await self.handle_geological_request(data)
        elif request_type == "context_update":
            return await self.handle_context_update(data)
        else:
            return {
                "status": "error",
                "message": f"Bilinmeyen istek tipi: {request_type}"
            }
            
    async def handle_geological_request(self, data: Dict) -> Dict:
        """Jeolojik veri isteklerini işler"""
        location = data.get("location")
        if not location:
            return {
                "status": "error",
                "message": "Konum bilgisi gerekli"
            }
            
        # Örnek yanıt (gerçek API entegrasyonu burada yapılacak)
        return {
            "status": "success",
            "data": {
                "location": location,
                "coordinates": {
                    "latitude": 41.007107,
                    "longitude": 28.972182
                },
                "type": "locality",
                "name": location,
                "country": "Turkey",
                "country_code": "TUR"
            }
        }
        
    async def handle_context_update(self, data: Dict) -> Dict:
        """Bağlam güncelleme isteklerini işler"""
        client_id = data.get("client_id")
        context_data = data.get("context", {})
        
        if not client_id:
            return {
                "status": "error",
                "message": "İstemci ID'si gerekli"
            }
            
        await self.update_context(client_id, context_data)
        return {
            "status": "success",
            "message": "Bağlam güncellendi"
        }

# FastAPI uygulaması
app = FastAPI(title="MCP Sunucusu")

# CORS ayarları
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MCP sunucu örneği
mcp_server = MCPServer()

# HTTP endpoint'leri
@app.get("/")
async def root():
    return {"message": "MCP Sunucusu Çalışıyor"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/api/geological-data")
async def get_geological_data(request: Request):
    try:
        data = await request.json()
        response = await mcp_server.handle_geological_request(data)
        return JSONResponse(content=response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/context-update")
async def update_context(request: Request):
    try:
        data = await request.json()
        response = await mcp_server.handle_context_update(data)
        return JSONResponse(content=response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# WebSocket endpoint'i (opsiyonel, Smithery'de WebSocket desteği varsa)
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    client_id = str(id(websocket))
    
    try:
        await mcp_server.connect_client(client_id)
        mcp_server.clients[client_id]["websocket"] = websocket
        
        while True:
            data = await websocket.receive_text()
            request = json.loads(data)
            response = await mcp_server.handle_request(request)
            await websocket.send_json(response)
            
    except WebSocketDisconnect:
        await mcp_server.disconnect_client(client_id)
    except Exception as e:
        await websocket.send_json({
            "status": "error",
            "message": str(e)
        })
        await mcp_server.disconnect_client(client_id)

# Smithery için port yapılandırması
port = int(os.getenv("PORT", 8081))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=port) 