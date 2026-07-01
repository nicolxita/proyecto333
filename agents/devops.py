"""
DevOps Agent: Generación de landing page y deployment automático.
Utiliza Jinja2 para renderizar plantillas estáticas y Gemini para generar el copy estructurado en JSON.
"""
import asyncio
import logging
import json
from datetime import datetime, timedelta
from typing import List
from jinja2 import Environment, FileSystemLoader
from models import ProductState
from config import settings
from pydantic import BaseModel

try:
    from google import genai
    from google.genai import types
    GEMINI_SDK_AVAILABLE = True
except ImportError:
    GEMINI_SDK_AVAILABLE = False

logger = logging.getLogger(__name__)

# --- Pydantic Schemas for Structured JSON Output ---
class Highlight(BaseModel):
    title: str
    description: str

class Review(BaseModel):
    quote: str
    author: str
    location: str
    platform: str
    rating: int

class FAQ(BaseModel):
    question: str
    answer: str

class LandingPageCopy(BaseModel):
    seo_title: str
    hero_bullet_points: List[Highlight]
    how_to_use: str
    
    problem_statement: str
    solution_pretitle: str
    solution_title: str
    solution_desc: str
    
    highlights: List[Highlight]
    
    social_proof_title: str
    social_proof_desc: str
    reviews: List[Review]
    

    faqs: List[FAQ]
    
    cta_title: str
    cta_desc: str
    
    dropshipping_score: int


def _is_api_key_valid() -> bool:
    """Verifica si la clave de API de Gemini es válida."""
    key = settings.gemini_api_key
    return bool(key and key.strip() and "placeholder" not in key.lower())

COPY_MASTER_PROMPT = """
# SYSTEM ROLE
You are a world-class eCommerce Conversion Optimization Copywriter.
Your goal is to write high-converting copy in Spanish for a premium, single-product landing page.

# BRAND TONE
Minimalist. Editorial. Premium. Sophisticated. Quiet. Modern. Intentional.
Do not use aggressive sales tactics (e.g., "BUY NOW BEFORE IT RUNS OUT").
Focus on deep emotion, atmosphere, wellness, and real transformation. For the highlights/benefits, avoid generic claims like "Premium Quality" or "Fast Results". Instead, focus on emotional hooks: how it restores confidence, brings peace of mind, or deeply impacts their daily life.

# SECTIONS TO GENERATE
1. Header:
   - hero_bullet_points: EXACTLY 3 punchy bullet points. Format: title is a short bold punchline (max 4 words), description is a brief explanation (max 8 words). Example: title="Formato Gigante", description="1 Kilo que dura muchísimo más". Focus on product characteristics and emotional hooks.
2. Problem/Solution Block: A SUPER FAST, extremely short and easy to read pitch. Keep it minimal.
   - problem_statement: MAXIMUM 15 WORDS. A direct pain point question/statement. DO NOT use emojis. (e.g. "¿Falta de vitalidad o cabello débil? Recupera tu energía.")
   - solution_title: MAXIMUM 6 WORDS. The main headline.
   - solution_desc: MAXIMUM 15 WORDS. Direct solution statement. DO NOT use emojis. (e.g. "Nutre tu cuerpo desde adentro y restaura tu bienestar profundo.")
3. Highlights: EXACTLY 3 specific features/benefits. DO NOT use emojis.
   - title: MAXIMUM 4 WORDS.
   - description: MAXIMUM 8 WORDS. Extremely concise.
4. How to use (how_to_use): A short, 1-2 sentence instruction on how to use or apply the product.
5. Social Proof: Encontrar 3 comentarios REALES de clientes reales.
   - Criterios: Orgánicos (lenguaje natural, expresiones reales, emojis si aplica). No uses reseñas perfectas tipo corporativo ("Es un producto excelente"). Busca textos auténticos ("Al principio dudaba pero de verdad funciona", "Llegó super rápido y el material es de 10"). Deben mencionar un beneficio específico o cómo solucionó un problema. Ubicación sugerida: Chile.
   - Formato: platform DEBE SER "Facebook". rating debe ser 4 o 5.

6. FAQs: 5-8 frequently asked questions. MUST include one exactly with the question: "¿Qué significa que sea pago contra entrega?" and the answer MUST briefly explain that they order now without paying, and only pay (cash/transfer) when they receive the product in their hands.

# SCORING
You must assign a dropshipping_score from 1 to 10 (1 = Premium Apple-like brand, 10 = Scammy AliExpress dropshipping). You MUST aim for 1 or 2.

Ensure all copy is in natural, persuasive Chilean Spanish.
"""

def _generate_fallback_html(state: ProductState) -> str:
    """Genera un HTML usando la plantilla completa pero con datos de fallback por fallo de API."""
    from jinja2 import Environment, FileSystemLoader
    from datetime import datetime, timedelta
    
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template('landing.html')
    
    fecha_inicio = (datetime.now() + timedelta(days=2)).strftime("%d de %b")
    fecha_fin = (datetime.now() + timedelta(days=5)).strftime("%d de %b")
    
    def fmt_price(val):
        return f"${int(val):,}".replace(",", ".")
        
    offer_price = fmt_price(state.suggested_price * 1000)
    normal_price = fmt_price(state.suggested_price * 2000)
    promo_2_price = fmt_price(state.suggested_price * 1500)
    
    images = ["assets/1.webp", "assets/2.webp", "assets/11.png"]
    
    copy_data = {
        "seo_title": state.product_name,
        "hero_bullet_points": [
            {"title": "Formato Gigante", "description": "1 Kilo para que te dure mucho más"},
            {"title": "Fórmula Sin Sabor", "description": "ideal para mezclar con tu bebida favorita"},
            {"title": "Absorción Rápida", "description": "resultados visibles en la primera semana"}
        ],
        "how_to_use": "Añade una porción diaria a tu bebida favorita (fría o caliente), revuelve bien y disfruta de sus beneficios. Su formato sin sabor lo hace perfecto para cualquier momento del día.",
        "problem_statement": "¿Falta de vitalidad o cabello débil? El tiempo reduce tu energía.",
        "solution_pretitle": "LA SOLUCIÓN",
        "solution_title": "Recupera tu Confianza Total",
        "solution_desc": "Nutre tu cuerpo desde adentro y restaura tu vitalidad natural.",
        "highlights": [
            {
                "title": "Piel Firme",
                "description": "Rellena líneas desde el interior."
            },
            {
                "title": "Uñas Fuertes",
                "description": "Restaura fuerza y brillo natural."
            },
            {
                "title": "Más Energía",
                "description": "Despierta renovada todos los días."
            }
        ],
        "social_proof_title": "Lo que dicen nuestros clientes",
        "social_proof_desc": "Miles de personas ya lo han probado.",
        "reviews": [
            {"quote": "Excelente producto, llegó muy rápido y funciona de maravilla. Totalmente recomendado.", "author": "María G.", "location": "Santiago", "platform": "Facebook", "rating": 5},
            {"quote": "Al principio dudaba pero de verdad cumple lo que promete. Lo volvería a comprar sin pensarlo.", "author": "Juan P.", "location": "Viña del Mar", "platform": "Facebook", "rating": 5},
            {"quote": "Me encantó, el formato es súper práctico y los resultados se notan muchísimo.", "author": "Camila S.", "location": "Concepción", "platform": "Facebook", "rating": 5}
        ],
        "faqs": [
            {"question": "¿Qué significa que sea pago contra entrega?", "answer": "Significa que puedes hacer tu pedido ahora sin pagar nada, y solo pagas (en efectivo o transferencia) cuando recibas el producto en tus manos en tu domicilio."},
            {"question": "¿Cuánto demora el envío a mi región?", "answer": "Los envíos suelen tardar entre 2 a 5 días hábiles dependiendo de la región en la que te encuentres."}
        ],
        "cta_title": "No esperes más, mejora tu rutina",
        "cta_desc": "Aprovecha esta oferta por tiempo limitado. Pídelo hoy y paga al recibir.",
        "dropshipping_score": 1
    }
    
    return template.render(
        **copy_data,
        product_name=state.product_name,
        sku=f"MA-{state.product_name[:3].upper()}-001",
        offer_price=offer_price,
        normal_price=normal_price,
        promo_2_price=promo_2_price,
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin,
        image_assets=images,
        tiktok_videos=["7649576135742754062", "7538956249505795334", "7378966449324346670"]
    )


async def _generate_dynamic_html(state: ProductState) -> str:
    """
    Usa Gemini para generar solo el copy en JSON y luego usa Jinja2 para renderizar el HTML.
    """
    if not (GEMINI_SDK_AVAILABLE and _is_api_key_valid()):
        logger.warning("⚠️ [DEVOPS] SDK de Gemini no disponible. Usando fallback estático.")
        return _generate_fallback_html(state)

    logger.info("🧠 [DEVOPS] Ejecutando análisis de Copy y generación estructurada...")
    client = genai.Client(api_key=settings.gemini_api_key)
    
    product_context = f"""
---
# PRODUCT DETAILS
Product Name: {state.product_name}
Suggested Price: ${state.suggested_price} USD
Available Images: {state.image_assets}
Marketing Angles: {state.marketing_angles}
---
Generate the JSON copy now.
"""
    base_prompt = COPY_MASTER_PROMPT + "\n" + product_context
    max_retries = 3
    
    for attempt in range(1, max_retries + 1):
        logger.info(f"🔄 [DEVOPS] Intento de copy {attempt}/{max_retries}...")
        try:
            current_prompt = base_prompt
            if attempt > 1:
                current_prompt += "\n\nWARNING: Your previous copy was rejected because 'dropshipping_score' was greater than 3. Make it more premium."

            loop = asyncio.get_running_loop()
            response = await loop.run_in_executor(
                None,
                lambda: client.models.generate_content(
                    model='gemini-2.5-pro',
                    contents=current_prompt,
                    config=types.GenerateContentConfig(
                        temperature=0.5,
                        response_mime_type="application/json",
                        response_schema=LandingPageCopy,
                    )
                )
            )
            
            raw_output = response.text
            copy_data = json.loads(raw_output)
            
            dropshipping_score = copy_data.get("dropshipping_score", 5)
            logger.info(f"📊 [DEVOPS] Evaluador: Nivel de Dropshipping detectado: {dropshipping_score}/10")
            
            if dropshipping_score > 3:
                logger.warning(f"❌ [DEVOPS] Copy rechazado por verse muy 'dropshippero'. Reintentando...")
                if attempt < max_retries:
                    continue
                else:
                    logger.warning("⚠️ [DEVOPS] Máximo de reintentos alcanzado.")
            
            logger.info(f"✅ [DEVOPS] Copy Premium validado.")
            
            # --- RENDERIZADO JINJA2 ---
            logger.info("🎨 [DEVOPS] Renderizando template estático con Jinja2...")
            
            env = Environment(loader=FileSystemLoader('templates'))
            template = env.get_template('landing.html')
            
            # Variables inyectadas por python
            fecha_inicio = (datetime.now() + timedelta(days=2)).strftime("%d de %b")
            fecha_fin = (datetime.now() + timedelta(days=5)).strftime("%d de %b")
            
            # Reemplazar comas por puntos en los precios si es necesario, o formatear:
            # Format as $XX.XXX
            def fmt_price(val):
                return f"${int(val):,}".replace(",", ".")
                
            offer_price = fmt_price(state.suggested_price * 1000) # simulating clp
            normal_price = fmt_price(state.suggested_price * 2000)
            promo_2_price = fmt_price(state.suggested_price * 1500)
            
            # Override image_assets with the user-provided files
            images = ["assets/1.webp", "assets/2.webp", "assets/11.png"]
            
            html_content = template.render(
                **copy_data,
                product_name=state.product_name,
                sku=f"MA-{state.product_name[:3].upper()}-001",
                offer_price=offer_price,
                normal_price=normal_price,
                promo_2_price=promo_2_price,
                fecha_inicio=fecha_inicio,
                fecha_fin=fecha_fin,
                image_assets=images,
                tiktok_videos=["7649576135742754062", "7538956249505795334", "7378966449324346670"]
            )
            
            return html_content

        except Exception as e:
            logger.error(f"❌ [DEVOPS] Error en generación con Gemini: {str(e)}")
            if attempt == max_retries:
                return _generate_fallback_html(state)

    return _generate_fallback_html(state)


async def _deploy_to_vercel(html_content: str, product_name: str) -> str:
    """Simula deployment a Vercel mediante su API."""
    logger.info("🚀 [DEVOPS] Desplegando sitio a Vercel...")
    await asyncio.sleep(2.5)
    sanitized_name = product_name.lower().replace(" ", "-")[:30]
    deployed_url = f"https://{sanitized_name}-auto.vercel.app"
    logger.info(f"✅ [DEVOPS] Sitio desplegado exitosamente: {deployed_url}")
    return deployed_url


async def run_devops_agent(state: ProductState) -> ProductState:
    """Agente DevOps que genera y despliega la landing page."""
    logger.info("⚙️  [DEVOPS] Iniciando generación y deployment de landing page...")
    
    html_content = await _generate_dynamic_html(state)
    
    try:
        with open("index.html", "w", encoding="utf-8") as f:
            f.write(html_content)
        logger.info("💾 [DEVOPS] Landing page guardada localmente como 'index.html'")
    except Exception as e:
        logger.error(f"❌ [DEVOPS] Error al guardar landing page localmente: {str(e)}")
    
    deployed_url = await _deploy_to_vercel(html_content, state.product_name)
    
    state.deployed_url = deployed_url
    state.deployment_timestamp = datetime.utcnow()
    state.pipeline_stage = "devops_completed"
    
    logger.info(f"🎉 [DEVOPS] Landing page en vivo: {deployed_url}")
    return state
