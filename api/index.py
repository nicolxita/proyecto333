"""
Función Serverless para Vercel.
Recibe pedidos de la Landing Page y los envía de forma segura a Dropi Chile.
"""
import logging
import aiohttp
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from config import settings

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("VercelDropi")

app = FastAPI()


class OrderRequest(BaseModel):
    name: str
    phone: str
    address: str
    city: str


@app.post("/api/order")
async def create_order(order: OrderRequest):
    """
    Endpoint seguro de procesamiento de pedidos COD.
    """
    logger.info(f"📥 Pedido Vercel recibido: {order.name} - {order.phone} - {order.city}")
    
    # 1. Comprobar si tenemos configurada la clave real de Dropi
    is_placeholder = (
        not settings.dropi_api_key or 
        settings.dropi_api_key == "your-dropi-api-key-here" or 
        "placeholder" in settings.dropi_api_key.lower()
    )
    
    if is_placeholder:
        # Modo Simulado (No hay API key configurada)
        logger.info("[MODO SIMULACIÓN] Creando orden ficticia en Dropi Chile")
        return {
            "status": "success",
            "message": "Pedido simulado registrado exitosamente en Dropi Chile (Modo Desarrollo en Vercel)",
            "order_id": "VERCEL-SIM-COD-12345"
        }
        
    # Modo Producción (Llamada real a la API de Dropi Chile)
    logger.info(f"🚀 Enviando orden real a Dropi Chile (Producto ID: {settings.dropi_product_id})...")
    
    url = "https://api.dropi.cl/api/v1/orders"
    
    headers = {
        "Authorization": f"Bearer {settings.dropi_api_key}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    payload = {
        "product_id": settings.dropi_product_id,
        "quantity": 1,
        "shipping_method": "COD",
        "customer": {
            "name": order.name,
            "phone": order.phone,
            "address": order.address,
            "city": order.city,
            "country": "Chile"
        }
    }
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=payload, timeout=10) as response:
                response_text = await response.text()
                status_code = response.status
                
                if status_code in [200, 201]:
                    data = await response.json()
                    dropi_order_id = data.get("order_id") or data.get("id") or "OK"
                    logger.info(f"✅ Pedido creado en Dropi con éxito. ID: {dropi_order_id}")
                    return {
                        "status": "success",
                        "message": "Pedido registrado exitosamente en Dropi Chile.",
                        "order_id": dropi_order_id
                    }
                else:
                    logger.error(f"❌ Error en API de Dropi (Status {status_code}): {response_text}")
                    return JSONResponse(
                        status_code=400,
                        content={
                            "status": "error",
                            "message": f"Dropi API devolvió error (Código {status_code})",
                            "detail": response_text
                        }
                    )
    except Exception as e:
        logger.error(f"❌ Excepción al conectar con Dropi: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error de conexión con el proveedor Dropi: {str(e)}"
        )
