import re

def modify_html(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Add Pixel in <head>
    if "TU_PIXEL_ID" not in content:
        head_end = r'</head>'
        pixel_code = """<!-- Meta Pixel Code -->
<script>
!function(f,b,e,v,n,t,s)
{if(f.fbq)return;n=f.fbq=function(){n.callMethod?
n.callMethod.apply(n,arguments):n.queue.push(arguments)};
if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
n.queue=[];t=b.createElement(e);t.async=!0;
t.src=v;s=b.getElementsByTagName(e)[0];
s.parentNode.insertBefore(t,s)}(window, document,'script',
'https://connect.facebook.net/en_US/fbevents.js');
fbq('init', 'TU_PIXEL_ID'); // REEMPLAZA TU_PIXEL_ID CON TU ID REAL
fbq('track', 'PageView');
</script>
<noscript><img height="1" width="1" style="display:none"
src="https://www.facebook.com/tr?id=TU_PIXEL_ID&ev=PageView&noscript=1"
/></noscript>
<!-- End Meta Pixel Code -->
</head>"""
        content = re.sub(head_end, pixel_code, content)

    # 2. Urgency Message in checkout modal
    # Find: <span class="block text-[9px] text-indigo-600 font-bold uppercase mt-0.5">ENVÍO GRATIS</span>
    # And add the urgency below it inside the flex container or outside.
    # The container is: <div class="bg-gray-50 p-3 rounded-xl border border-gray-100 flex items-center gap-3 mb-5">
    
    # We can place it right below that container.
    urgency_pattern = r'(<div class="bg-gray-50 p-3 rounded-xl border border-gray-100 flex items-center gap-3 mb-5">.*?\n\s*</div>)'
    urgency_html = r'\1\n          <div class="bg-rose-50 border border-rose-200 rounded-lg p-2 mb-5 flex items-center justify-center gap-2 animate-pulse">\n            <svg class="w-4 h-4 text-rose-600" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 18.657A8 8 0 016.343 7.343S7 9 9 10c0-2 .5-5 2.986-7C14 5 16.09 5.777 17.656 7.343A7.975 7.975 0 0120 13a7.975 7.975 0 01-2.343 5.657z" /><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.879 16.121A3 3 0 1012.015 11L11 14H9c0 .768.293 1.536.879 2.121z" /></svg>\n            <span class="text-rose-600 text-[11px] font-bold">¡Alta demanda! Solo quedan 14 unidades.</span>\n          </div>'
    if "¡Alta demanda!" not in content:
        content = re.sub(urgency_pattern, urgency_html, content, flags=re.DOTALL)

    # 3. Add RUT Formatter and Error HTML
    # RUT input: <input type="text" id="codRut" required class="..." placeholder="12.345.678-9">
    rut_input_pattern = r'(<input type="text" id="codRut" required class="[^"]+" placeholder="12\.345\.678-9">)'
    rut_input_replacement = r'<input type="text" id="codRut" required class="w-full bg-white border border-gray-200 rounded-lg px-3 py-2.5 text-sm text-gray-900 focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500 outline-none transition-colors" placeholder="12.345.678-9" oninput="formatRut(this)">\n                    <p id="rutError" class="text-red-500 text-[10px] mt-1 hidden">RUT inválido. Verifícalo.</p>'
    content = re.sub(rut_input_pattern, rut_input_replacement, content)

    # 4. Add Javascript for RUT formatting and Validation, and Purchase Pixel
    js_funcs = """
        function formatRut(input) {
            let rut = input.value.replace(/[^0-9kK]/g, '').toUpperCase();
            if (rut.length > 1) {
                input.value = rut.slice(0, -1).replace(/\\B(?=(\\d{3})+(?!\\d))/g, ".") + "-" + rut.slice(-1);
            } else {
                input.value = rut;
            }
        }

        function validarRut(rutCompleto) {
            let rut = rutCompleto.replace(/[^0-9kK]/g, '').toUpperCase();
            if (rut.length < 8) return false;
            let cuerpo = rut.slice(0, -1);
            let dv = rut.slice(-1);
            let suma = 0;
            let multiplo = 2;
            for (let i = 1; i <= cuerpo.length; i++) {
                let index = multiplo * cuerpo.charAt(cuerpo.length - i);
                suma = suma + index;
                if (multiplo < 7) { multiplo = multiplo + 1; } else { multiplo = 2; }
            }
            let dvEsperado = 11 - (suma % 11);
            dv = (dv == 'K') ? 10 : dv;
            dv = (dv == 0) ? 11 : dv;
            if (dvEsperado == 11) dvEsperado = '0';
            else if (dvEsperado == 10) dvEsperado = 'K';
            else dvEsperado = dvEsperado.toString();
            return dvEsperado === dv.toString();
        }

        function submitCODOrder(event) {
"""
    
    content = content.replace("function submitCODOrder(event) {", js_funcs)

    # Add RUT validation in submitCODOrder
    # Find: const phone = document.getElementById('codPhone').value;
    rut_val_code = """
            const rutInput = document.getElementById('codRut').value;
            if (!validarRut(rutInput)) {
                document.getElementById('rutError').classList.remove('hidden');
                return;
            }
            document.getElementById('rutError').classList.add('hidden');
            
            const phone = document.getElementById('codPhone').value;"""
            
    content = content.replace("const phone = document.getElementById('codPhone').value;", rut_val_code)

    # Add Purchase event in fetch .then
    # Find: document.getElementById('successModal').classList.remove('hidden');
    pixel_purchase_code = """document.getElementById('successModal').classList.remove('hidden');
                
                if(typeof fbq === 'function') {
                    fbq('track', 'Purchase', {value: selectedPrice, currency: 'CLP'});
                }"""
    content = content.replace("document.getElementById('successModal').classList.remove('hidden');", pixel_purchase_code)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Updated {filepath}")

modify_html('index.html')
modify_html('templates/landing.html')
