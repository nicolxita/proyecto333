"""
Creative Agent: Generación de copy persuasivo y assets visuales.
Integra con la API de Google Gemini (Gemini 1.5 Flash e Imagen 3) en AI Studio.
Incluye un mecanismo de fallback para ejecución simulada en caso de no contar con API key.
"""
import os
import asyncio
import logging
from pydantic import BaseModel, Field
from models import ProductState
from config import settings

# Intentar importar el SDK de Google Gemini
try:
    from google import genai
    from google.genai import types
    GEMINI_SDK_AVAILABLE = True
except ImportError:
    GEMINI_SDK_AVAILABLE = False

logger = logging.getLogger(__name__)

# Definir esquemas para salidas estructuradas
class MarketingCopy(BaseModel):
    headline: str = Field(description="Un titular extremadamente persuasivo y magnético para el anuncio de dropshipping")
    body: str = Field(description="El texto principal del anuncio describiendo los beneficios clave, puntos de dolor, oferta y escasez")
    cta: str = Field(description="Llamada a la acción clara y directa para incentivar la compra")

class MarketingAngles(BaseModel):
    angles: list[str] = Field(description="Una lista de exactamente 5 ángulos de marketing basados en psicología del consumidor")


def _is_api_key_valid() -> bool:
    """Verifica si la clave de API de Gemini es válida y no es un placeholder."""
    key = settings.gemini_api_key
    return bool(key and key.strip() and "placeholder" not in key.lower())


async def _generate_marketing_copy(product_name: str) -> dict:
    """
    Genera copy persuasivo para el producto usando Gemini 1.5 Flash (real o simulado).
    """
    if GEMINI_SDK_AVAILABLE and _is_api_key_valid():
        logger.info("📝 [CREATIVE] Llamando a Gemini API para generar copy estructurado...")
        try:
            client = genai.Client(api_key=settings.gemini_api_key)
            prompt = (
                f"Genera copy de marketing en español para un producto de dropshipping llamado '{product_name}'. "
                "El copy debe ser persuasivo, resaltar los beneficios clave, usar gatillos mentales (como escasez u oferta) "
                "y tener una llamada a la acción irrefutable."
            )
            # Ejecutar llamada bloqueante de la API en un executor para no bloquear el loop de eventos asíncrono
            loop = asyncio.get_running_loop()
            response = await loop.run_in_executor(
                None,
                lambda: client.models.generate_content(
                    model='gemini-3.1-flash-lite',
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        response_mime_type="application/json",
                        response_schema=MarketingCopy,
                        temperature=0.7,
                    )
                )
            )
            copy_data = response.parsed
            copy = {
                "headline": copy_data.headline,
                "body": copy_data.body,
                "cta": copy_data.cta
            }
            logger.info(f"✅ [CREATIVE] Copy generado por Gemini: {copy['headline'][:50]}...")
            return copy
        except Exception as e:
            logger.error(f"❌ [CREATIVE] Error al llamar a Gemini API para copy: {str(e)}. Usando simulación.")
    
    # Fallback / Simulación
    logger.info("📝 [CREATIVE] Generando copy (SIMULADO)...")
    await asyncio.sleep(1.2)
    return {
        "headline": f"Transforma tu espacio con {product_name} en 60 segundos",
        "body": (
            f"Experimenta la mejor calidad y diseño con {product_name}. "
            "Perfecto para el hogar, oficina o regalo. "
            "Más de 10,000 clientes satisfechos. Stock muy limitado con envío gratis hoy."
        ),
        "cta": "Consigue el tuyo con 50% de descuento hoy →"
    }


async def _generate_image_assets(product_name: str) -> list:
    """
    Genera imágenes del producto usando Imagen 3 (real o simulado).
    Las imágenes reales se guardan en la carpeta local 'generated_assets/'.
    """
    if GEMINI_SDK_AVAILABLE and _is_api_key_valid():
        logger.info("🎨 [CREATIVE] Llamando a Imagen 3 API para generar imágenes del producto...")
        try:
            client = genai.Client(api_key=settings.gemini_api_key)
            prompt = (
                f"A professional high-end lifestyle e-commerce product photograph of '{product_name}', "
                "clean aesthetic, dramatic studio lighting, 8k resolution, photorealistic, no watermarks"
            )
            
            loop = asyncio.get_running_loop()
            response = await loop.run_in_executor(
                None,
                lambda: client.models.generate_images(
                    model='imagen-4.0-generate-001',
                    prompt=prompt,
                    config=types.GenerateImagesConfig(
                        number_of_images=2,
                        output_mime_type="image/jpeg",
                        aspect_ratio="1:1"
                    )
                )
            )
            
            # Crear directorio local
            os.makedirs("generated_assets", exist_ok=True)
            sanitized_name = product_name.lower().replace(" ", "_").replace("°", "")
            sanitized_name = "".join(c for c in sanitized_name if c.isalnum() or c == "_")[:20]
            
            saved_images = []
            for i, generated_image in enumerate(response.generated_images):
                file_path = f"generated_assets/{sanitized_name}_image_{i}.jpg"
                with open(file_path, "wb") as f:
                    f.write(generated_image.image.image_bytes)
                
                # Obtener ruta absoluta para cargar localmente en el HTML
                abs_path = os.path.abspath(file_path)
                # Formatear como file URI
                file_url = f"file:///{abs_path.replace(os.sep, '/')}"
                saved_images.append(file_url)
                logger.info(f"💾 [CREATIVE] Imagen {i} guardada en: {file_path}")
                
            if saved_images:
                logger.info(f"✅ [CREATIVE] {len(saved_images)} imágenes reales generadas por Imagen 3")
                return saved_images
        except Exception as e:
            logger.error(f"❌ [CREATIVE] Error al generar imágenes con Imagen 3: {str(e)}. Usando simulación.")
            
    # Fallback / Simulación
    logger.info("🎨 [CREATIVE] Generando assets visuales (SIMULADO)...")
    await asyncio.sleep(2.0)
    
    local_llama_path = os.path.abspath("generated_assets/humidificador_llama.png")
    if os.path.exists(local_llama_path):
        hero_img = "generated_assets/humidificador_llama.png"
    else:
        hero_img = "https://dropship-assets.s3.amazonaws.com/galaxy-projector-hero.jpg"
        
    return [
        hero_img,
        "https://dropship-assets.s3.amazonaws.com/galaxy-projector-lifestyle-1.jpg",
        "https://dropship-assets.s3.amazonaws.com/galaxy-projector-lifestyle-2.jpg",
        "https://dropship-assets.s3.amazonaws.com/galaxy-projector-features.jpg"
    ]


async def _identify_marketing_angles(product_name: str, price: float) -> list:
    """
    Identifica ángulos de marketing usando Gemini 1.5 Flash (real o simulado).
    """
    if GEMINI_SDK_AVAILABLE and _is_api_key_valid():
        logger.info("🎯 [CREATIVE] Llamando a Gemini API para identificar ángulos de marketing...")
        try:
            client = genai.Client(api_key=settings.gemini_api_key)
            prompt = (
                f"Identifica exactamente 5 ángulos de marketing basados en psicología del consumidor "
                f"para vender el producto '{product_name}' a un precio sugerido de ${price} USD. "
                "Devuelve una lista de frases cortas de gancho de marketing."
            )
            
            loop = asyncio.get_running_loop()
            response = await loop.run_in_executor(
                None,
                lambda: client.models.generate_content(
                    model='gemini-3.1-flash-lite',
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        response_mime_type="application/json",
                        response_schema=MarketingAngles,
                        temperature=0.7,
                    )
                )
            )
            angles_data = response.parsed
            logger.info(f"✅ [CREATIVE] {len(angles_data.angles)} ángulos generados por Gemini")
            return angles_data.angles
        except Exception as e:
            logger.error(f"❌ [CREATIVE] Error al generar ángulos de marketing con Gemini: {str(e)}. Usando simulación.")
            
    # Fallback / Simulación
    logger.info("🎯 [CREATIVE] Identificando ángulos de marketing (SIMULADO)...")
    await asyncio.sleep(0.5)
    return [
        "Transformación instantánea del espacio (antes/después)",
        "Experiencia premium a precio accesible (ancla de valor)",
        "Escasez artificial (stock limitado, oferta temporal)",
        "Prueba social (miles de reviews positivas)",
        "Múltiples casos de uso (versatilidad del producto)"
    ]


async def run_creative_agent(state: ProductState) -> ProductState:
    """
    Agente creativo que genera todos los assets de marketing.
    Ejecuta la generación en paralelo para optimizar tiempo.
    """
    logger.info("🎨 [CREATIVE] Iniciando generación de contenido creativo...")
    
    # Ejecutar tareas en paralelo
    copy_task = _generate_marketing_copy(state.product_name)
    images_task = _generate_image_assets(state.product_name)
    angles_task = _identify_marketing_angles(state.product_name, state.suggested_price)
    
    copy, images, angles = await asyncio.gather(copy_task, images_task, angles_task)
    
    # Actualizar estado global
    state.generated_copy = copy
    state.image_assets = images
    state.marketing_angles = angles
    state.pipeline_stage = "creative_completed"
    
    logger.info(
        f"✅ [CREATIVE] Contenido generado exitosamente: "
        f"{len(images)} imágenes, {len(angles)} ángulos, copy completo"
    )
    
    return state
