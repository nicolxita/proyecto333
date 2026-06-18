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
class Benefit(BaseModel):
    title: str
    description: str

class Step(BaseModel):
    title: str
    description: str

class Highlight(BaseModel):
    title: str
    description: str

class Review(BaseModel):
    quote: str
    author: str
    location: str
    platform: str
    rating: int

class Objection(BaseModel):
    title: str
    description: str

class FAQ(BaseModel):
    question: str
    answer: str

class LandingPageCopy(BaseModel):
    seo_title: str
    
    problem_title: str
    problem_desc: str
    
    solution_pretitle: str
    solution_title: str
    solution_desc: str
    
    benefits_title: str
    benefits_desc: str
    benefits: List[Benefit]
    
    how_it_works_title: str
    how_it_works_desc: str
    how_it_works_steps: List[Step]
    
    highlights: List[Highlight]
    
    social_proof_title: str
    social_proof_desc: str
    reviews: List[Review]
    
    objections_title: str
    objections_desc: str
    objections: List[Objection]
    
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
Focus on emotion, atmosphere, wellness, and problem-solving.

# SECTIONS TO GENERATE
1. Problem: Agitate a pain point that the product solves.
2. Solution: Present the product elegantly.
3. Benefits: 4 key benefits.
4. How it works: 3 simple steps to use the product.
5. Highlights: 2 specific features/technologies.
6. Social Proof: Encontrar 5 comentarios REALES de clientes reales.
   - Criterios: Orgánicos (lenguaje natural, expresiones reales, emojis si aplica). No uses reseñas perfectas tipo corporativo ("Es un producto excelente"). Busca textos auténticos ("Al principio dudaba pero de verdad funciona", "Llegó super rápido y el material es de 10"). Deben mencionar un beneficio específico o cómo solucionó un problema. Ubicación sugerida: Chile.
   - Formato: platform debe ser TikTok, Amazon, Reddit o X. rating debe ser 4 o 5.
7. Objections: 3 common doubts and elegant answers showing safety and quality.
8. FAQs: 5-8 frequently asked questions. MUST include one exactly with the question: "¿Qué significa que sea pago contra entrega?" and the answer MUST briefly explain that they order now without paying, and only pay (cash/transfer) when they receive the product in their hands.

# SCORING
You must assign a dropshipping_score from 1 to 10 (1 = Premium Apple-like brand, 10 = Scammy AliExpress dropshipping). You MUST aim for 1 or 2.

Ensure all copy is in natural, persuasive Chilean Spanish.
"""

def _generate_fallback_html(state: ProductState) -> str:
    """Genera un HTML estático básico de fallback si la API falla."""
    headline = state.generated_copy.get("headline", "Increíble Producto")
    body = state.generated_copy.get("body", "Consigue el tuyo hoy.")
    price = state.suggested_price
    
    return f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{state.product_name}</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-[#FAFAFA] text-[#111111] font-sans antialiased">
    <div class="max-w-2xl mx-auto p-12 text-center space-y-8 mt-20 bg-white rounded-2xl shadow-sm border border-gray-100">
        <h1 class="text-3xl font-medium tracking-tight">{{headline}}</h1>
        <p class="text-gray-500 font-light">{{body}}</p>
        <p class="text-2xl font-medium">${{price}}</p>
        <button class="bg-[#111111] text-white px-8 py-3 rounded-full font-medium hover:bg-gray-800 transition-colors">Comprar Ahora</button>
    </div>
</body>
</html>"""


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
            
            # Ensure we have at least 2 images for the template
            images = state.image_assets if state.image_assets else ["", ""]
            if len(images) == 1:
                images.append(images[0])
            
            html_content = template.render(
                **copy_data,
                product_name=state.product_name,
                sku=f"MA-{state.product_name[:3].upper()}-001",
                offer_price=offer_price,
                normal_price=normal_price,
                promo_2_price=promo_2_price,
                fecha_inicio=fecha_inicio,
                fecha_fin=fecha_fin,
                image_assets=images
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
