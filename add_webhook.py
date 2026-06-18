import re

def add_webhook(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Insert Email field before Telephone
    # We find:
    # <div>
    #     <label class="block text-[10px] font-bold text-gray-700 uppercase tracking-wider mb-1">Teléfono (WhatsApp)</label>
    
    phone_div_pattern = r'(<div>\s*<label class="block text-\[10px\] font-bold text-gray-700 uppercase tracking-wider mb-1">Teléfono \(WhatsApp\)</label>)'
    
    email_div = """<div>
                <label class="block text-[10px] font-bold text-gray-700 uppercase tracking-wider mb-1">Correo Electrónico</label>
                <input type="email" id="codEmail" required class="w-full bg-white border border-gray-200 rounded-lg px-3 py-2.5 text-sm text-gray-900 focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500 outline-none transition-colors" placeholder="Ej: nombre@correo.com">
            </div>
            """
            
    content = re.sub(phone_div_pattern, email_div + r'\1', content)

    # 2. Replace submitCODOrder
    # Find from "function submitCODOrder(event) {" to the next function or closing tag
    
    old_func_pattern = r'function submitCODOrder\(event\) \{.*?(?=function closeCODModal)'
    
    new_func = """function submitCODOrder(event) {
            event.preventDefault();
            
            const phone = document.getElementById('codPhone').value;
            if (phone.length < 8 || phone.includes('12345678') || phone.includes('00000000') || /^(\d)\\1+$/.test(phone.replace(/\D/g, ''))) {
                document.getElementById('phoneError').classList.remove('hidden');
                return;
            }
            document.getElementById('phoneError').classList.add('hidden');
            
            const submitBtn = document.querySelector('#codForm button[type="submit"]');
            submitBtn.innerText = 'Procesando...';
            submitBtn.disabled = true;

            const orderData = {
                nombre: document.getElementById('codName').value,
                correo: document.getElementById('codEmail').value,
                telefono: phone,
                direccion: document.getElementById('codAddress').value,
                region: document.getElementById('region').options[document.getElementById('region').selectedIndex].text,
                comuna: document.getElementById('comuna').value,
                producto: "Humidificador Llama 3D",
                total: selectedPrice,
                unidades: selectedUnits
            };

            fetch('https://hook.us1.make.com/TU_WEBHOOK_AQUI', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(orderData)
            })
            .then(response => {
                document.getElementById('checkoutModal').classList.add('hidden');
                document.getElementById('codForm').reset();
                submitBtn.innerText = 'Confirmar Compra • Pago Contra Entrega';
                submitBtn.disabled = false;

                document.getElementById('successModal').classList.remove('hidden');
                
                if(typeof confetti === 'function') {
                    confetti({
                        zIndex: 999999,
                        particleCount: 150,
                        spread: 80,
                        origin: { y: 0.6 },
                        colors: ['#fbcfe8', '#f9a8d4', '#f472b6', '#db2777', '#fdf2f8']
                    });
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Hubo un problema procesando tu pedido. Por favor intenta de nuevo.');
                submitBtn.innerText = 'Confirmar Compra • Pago Contra Entrega';
                submitBtn.disabled = false;
            });
        }

        """
        
    content = re.sub(old_func_pattern, lambda m: new_func, content, flags=re.DOTALL)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Updated form and JS in {filepath}")

add_webhook('index.html')
add_webhook('templates/landing.html')
