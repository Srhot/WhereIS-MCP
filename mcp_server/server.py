import asyncio
import json
import os
import logging
from datetime import datetime
from typing import Dict, Any, Optional
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# Logging yapılandırması
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class MCPServer:
    def __init__(self):
        logger.info("Initializing MCPServer...")
        self.clients: Dict[str, Dict] = {}
        self.context: Dict[str, Any] = {}
        logger.info("MCPServer initialized successfully")
        
    async def connect_client(self, client_id: str):
        """Yeni istemci bağlantısını yönetir"""
        logger.debug(f"Connecting client: {client_id}")
        self.clients[client_id] = {
            "connected_at": datetime.now(),
            "context": {},
            "websocket": None
        }
        logger.debug(f"Client {client_id} connected successfully")
        
    async def disconnect_client(self, client_id: str):
        """İstemci bağlantısını sonlandırır"""
        logger.debug(f"Disconnecting client: {client_id}")
        if client_id in self.clients:
            del self.clients[client_id]
            logger.debug(f"Client {client_id} disconnected successfully")
            
    async def update_context(self, client_id: str, context_data: Dict):
        """İstemci bağlamını günceller"""
        logger.debug(f"Updating context for client: {client_id}")
        if client_id in self.clients:
            self.clients[client_id]["context"].update(context_data)
            logger.debug(f"Context updated for client {client_id}")
            
    async def handle_request(self, request: Dict) -> Dict:
        """MCP isteklerini işler"""
        logger.debug(f"Handling request: {request}")
        request_type = request.get("type")
        data = request.get("data", {})
        
        if request_type == "geological_data":
            return await self.handle_geological_request(data)
        elif request_type == "context_update":
            return await self.handle_context_update(data)
        else:
            logger.warning(f"Unknown request type: {request_type}")
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

# Smithery için port yapılandırması
port = int(os.getenv("PORT", 80))
logger.info(f"Starting server on port {port}")

# Ana uygulama değişkeni (gunicorn için gerekli)
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

@app.on_event("startup")
async def startup_event():
    logger.info("Application startup...")
    logger.info(f"Environment: {os.getenv('APP_ENV', 'development')}")
    logger.info(f"Debug mode: {os.getenv('DEBUG', 'False')}")
    logger.info("Application startup complete")

# HTTP endpoint'leri
@app.get("/")
async def root():
    logger.debug("Root endpoint called")
    return {"message": "MCP Sunucusu Çalışıyor"}

@app.get("/health")
async def health_check():
    logger.debug("Health check endpoint called")
    return {"status": "healthy"}

@app.post("/api/geological-data")
async def get_geological_data(request: Request):
    logger.debug("Geological data endpoint called")
    try:
        data = await request.json()
        logger.debug(f"Received data: {data}")
        response = await mcp_server.handle_geological_request(data)
        logger.debug(f"Sending response: {response}")
        return JSONResponse(content=response)
    except Exception as e:
        logger.error(f"Error in geological data endpoint: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/context-update")
async def update_context(request: Request):
    logger.debug("Context update endpoint called")
    try:
        data = await request.json()
        logger.debug(f"Received context data: {data}")
        response = await mcp_server.handle_context_update(data)
        logger.debug(f"Sending response: {response}")
        return JSONResponse(content=response)
    except Exception as e:
        logger.error(f"Error in context update endpoint: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

# WebSocket endpoint'i (opsiyonel, Smithery'de WebSocket desteği varsa)
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    logger.debug("WebSocket connection attempt")
    await websocket.accept()
    client_id = str(id(websocket))
    logger.info(f"WebSocket client connected: {client_id}")
    
    try:
        await mcp_server.connect_client(client_id)
        mcp_server.clients[client_id]["websocket"] = websocket
        
        while True:
            data = await websocket.receive_text()
            logger.debug(f"Received WebSocket data from {client_id}: {data}")
            request = json.loads(data)
            response = await mcp_server.handle_request(request)
            await websocket.send_json(response)
            logger.debug(f"Sent WebSocket response to {client_id}: {response}")
            
    except WebSocketDisconnect:
        logger.info(f"WebSocket client disconnected: {client_id}")
        await mcp_server.disconnect_client(client_id)
    except Exception as e:
        logger.error(f"WebSocket error for client {client_id}: {str(e)}", exc_info=True)
        await websocket.send_json({
            "status": "error",
            "message": str(e)
        })
        await mcp_server.disconnect_client(client_id)

# Sadece doğrudan çalıştırıldığında uvicorn'u başlat
if __name__ == "__main__":
    import uvicorn
    logger.info("Starting uvicorn server directly...")
    uvicorn.run("mcp_server.server:app", host="0.0.0.0", port=port, reload=True) 