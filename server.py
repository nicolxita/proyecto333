"""
Servidor Backend de Enlace Seguro para Landing Page y Dropi Chile.
Protege las claves de API y maneja la lógica de pedidos tanto en local como en producción.
"""
import os
import logging
import aiohttp
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
from config import settings

# Configurar logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("DropiServer")

app = FastAPI(title="Dropshipping COD Backend")

# Montar carpeta de assets generados para poder servir la imagen del producto
if os.path.exists("generated_assets"):
    app.mount("/generated_assets", StaticFiles(directory="generated_assets"), name="generated_assets")
else:
    logger.warning("⚠️  La carpeta 'generated_assets' no existe. Asegúrate de correr 'python main.py' primero.")


class OrderRequest(BaseModel):
    name: str
    phone: str
    address: str
    city: str


@app.get("/")
async def serve_landing():
    """Sirve la landing page autogenerada index.html."""
    if os.path.exists("index.html"):
        return FileResponse("index.html")
    else:
        return JSONResponse(
            status_code=404,
            content={
                "status": "error",
                "message": "Landing page index.html no encontrada. Ejecuta 'python main.py' para generarla."
            }
        )


@app.post("/api/order")
async def create_order(order: OrderRequest):
    """
    Recibe los datos del cliente de forma segura y los envía a Dropi Chile.
    Utiliza las credenciales guardadas en el archivo .env de forma oculta.
    """
    logger.info(f"📥 Pedido recibido: {order.name} - {order.phone} - {order.city}")
    
    # 1. Comprobar si tenemos configurada la clave real de Dropi
    is_placeholder = (
        not settings.dropi_api_key or 
        settings.dropi_api_key == "your-dropi-api-key-here" or 
        "placeholder" in settings.dropi_api_key.lower()
    )
    
    if is_placeholder:
        # Modo Simulado (No hay API key configurada)
        logger.info(
            f"🧪 [MODO SIMULACIÓN] Creando orden ficticia en Dropi Chile:\n"
            f"  - Producto ID: {settings.dropi_product_id}\n"
            f"  - Cliente: {order.name}\n"
            f"  - Fono: {order.phone}\n"
            f"  - Destino: {order.address}, {order.city}\n"
            f"  - Pago: Pago Contra Entrega (COD)"
        )
        return {
            "status": "success",
            "message": "Pedido simulado registrado exitosamente en Dropi Chile (Modo Desarrollo)",
            "order_id": "SIM-COD-98274"
        }
        
    # Modo Producción (Llamada real a la API de Dropi Chile)
    logger.info(f"🚀 Enviando orden a la API de Dropi Chile (Producto ID: {settings.dropi_product_id})...")
    
    # URL de la API de Dropi Chile
    url = "https://api.dropi.cl/api/v1/orders"
    
    headers = {
        "Authorization": f"Bearer {settings.dropi_api_key}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    # Formatear el payload con el formato exacto requerido por Dropi
    payload = {
        "product_id": settings.dropi_product_id,
        "quantity": 1,
        "shipping_method": "COD",  # Pago contra entrega
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


if __name__ == "__main__":
    import uvicorn
    logger.info("⚡ Iniciando servidor local en http://localhost:8000")
    uvicorn.run("server:app", host="127.0.0.1", port=8000, reload=True)
