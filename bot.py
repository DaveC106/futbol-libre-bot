import telebot
from flask import Flask
import threading
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import os
import re
import time

TOKEN = "7640481513:AAG9lbUvQGRjLYaHmp91LFKJo3O_YIY7RIw"
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# ========================
# PARTIDOS DIRECTAMENTE EN EL CÓDIGO
# ========================
PARTIDOS_JSON = {
  "partidos": [
    {
      "partido": "UEFA Europa League: FCSB vs Bologna",
      "link": "https://futbolibretv.pages.dev/#partido-26474"
    },
    {
      "partido": "UEFA Europa League: Salzburg vs Ferencváros",
      "link": "https://futbolibretv.pages.dev/#partido-26477"
    },
    {
      "partido": "UEFA Europa League: Feyenoord vs Panathinaikos",
      "link": "https://futbolibretv.pages.dev/#partido-26478"
    },
    {
      "partido": "UEFA Conference League: Drita vs Omonia Nicosia",
      "link": "https://futbolibretv.pages.dev/#partido-26491"
    },
    {
      "partido": "UEFA Conference League: Strasbourg vs Jagiellonia Białystok",
      "link": "https://futbolibretv.pages.dev/#partido-26495"
    },
    {
      "partido": "UEFA Europa League: Brann vs Rangers",
      "link": "https://futbolibretv.pages.dev/#partido-26472"
    },
    {
      "partido": "UEFA Europa League: Sporting Braga vs Crvena Zvezda",
      "link": "https://futbolibretv.pages.dev/#partido-26475"
    },
    {
      "partido": "UEFA Europa League: Go Ahead Eagles vs Aston Villa",
      "link": "https://futbolibretv.pages.dev/#partido-26480"
    },
    {
      "partido": "UEFA Conference League: Shakhtar Donetsk vs Legia Warszawa",
      "link": "https://futbolibretv.pages.dev/#partido-26492"
    },
    {
      "partido": "UEFA Conference League: Rijeka vs Sparta Praha",
      "link": "https://futbolibretv.pages.dev/#partido-26496"
    },
    {
      "partido": "UEFA Conference League: Häcken vs Rayo Vallecano",
      "link": "https://futbolibretv.pages.dev/#partido-26498"
    },
    {
      "partido": "UEFA Europa League: Fenerbahçe vs Stuttgart",
      "link": "https://futbolibretv.pages.dev/#partido-26473"
    },
    {
      "partido": "UEFA Europa League: Olympique Lyonnais vs Basel",
      "link": "https://futbolibretv.pages.dev/#partido-26476"
    },
    {
      "partido": "UEFA Europa League: Genk vs Real Betis",
      "link": "https://futbolibretv.pages.dev/#partido-26479"
    },
    {
      "partido": "UEFA Conference League: AEK Athens vs Aberdeen",
      "link": "https://futbolibretv.pages.dev/#partido-26490"
    },
    {
      "partido": "UEFA Conference League: Škendija 79 vs Shelbourne",
      "link": "https://futbolibretv.pages.dev/#partido-26493"
    },
    {
      "partido": "UEFA Conference League: Rapid Wien vs Fiorentina",
      "link": "https://futbolibretv.pages.dev/#partido-26494"
    },
    {
      "partido": "UEFA Conference League: Breidablik vs KuPS",
      "link": "https://futbolibretv.pages.dev/#partido-26497"
    },
    {
      "partido": "UEFA Conference League: Crystal Palace vs AEK Larnaca",
      "link": "https://futbolibretv.pages.dev/#partido-26501"
    },
    {
      "partido": "UEFA Conference League: Mainz 05 vs Zrinjski",
      "link": "https://futbolibretv.pages.dev/#partido-26503"
    },
    {
      "partido": "UEFA Conference League: Sigma Olomouc vs Raków Częstochowa",
      "link": "https://futbolibretv.pages.dev/#partido-26505"
    },
    {
      "partido": "League One: Exeter City vs Plymouth Argyle",
      "link": "https://futbolibretv.pages.dev/#partido-26511"
    },
    {
      "partido": "División Profesional: Oriente Petrolero vs Wilstermann",
      "link": "https://futbolibretv.pages.dev/#partido-26514"
    },
    {
      "partido": "UEFA Europa League: Lille vs PAOK",
      "link": "https://futbolibretv.pages.dev/#partido-26483"
    },
    {
      "partido": "UEFA Europa League: Maccabi Tel Aviv vs Midtjylland",
      "link": "https://futbolibretv.pages.dev/#partido-26484"
    },
    {
      "partido": "UEFA Europa League: Young Boys vs Ludogorets",
      "link": "https://futbolibretv.pages.dev/#partido-26488"
    },
    {
      "partido": "UEFA Conference League: Samsunspor vs Dynamo Kyiv",
      "link": "https://futbolibretv.pages.dev/#partido-26499"
    },
    {
      "partido": "UEFA Conference League: Hamrun Spartans vs Lausanne Sport",
      "link": "https://futbolibretv.pages.dev/#partido-26502"
    },
    {
      "partido": "UEFA Conference League: Lincoln Red Imps vs Lech Poznań",
      "link": "https://futbolibretv.pages.dev/#partido-26506"
    },
    {
      "partido": "UEFA Conference League: AZ vs Slovan Bratislava",
      "link": "https://futbolibretv.pages.dev/#partido-26507"
    },
    {
      "partido": "UEFA Europa League: Freiburg vs Utrecht",
      "link": "https://futbolibretv.pages.dev/#partido-26481"
    },
    {
      "partido": "UEFA Europa League: Nottingham Forest vs Porto",
      "link": "https://futbolibretv.pages.dev/#partido-26485"
    },
    {
      "partido": "UEFA Europa League: Roma vs Viktoria Plzeň",
      "link": "https://futbolibretv.pages.dev/#partido-26486"
    },
    {
      "partido": "UEFA Europa League: Celta de Vigo vs Nice",
      "link": "https://futbolibretv.pages.dev/#partido-26489"
    },
    {
      "partido": "UEFA Conference League: Shamrock Rovers vs Celje",
      "link": "https://futbolibretv.pages.dev/#partido-26500"
    },
    {
      "partido": "UEFA Conference League: CSU Craiova vs Noah",
      "link": "https://futbolibretv.pages.dev/#partido-26504"
    },
    {
      "partido": "UEFA Europa League: Malmö FF vs Dinamo Zagreb",
      "link": "https://futbolibretv.pages.dev/#partido-26482"
    },
    {
      "partido": "UEFA Europa League: Celtic vs Sturm Graz",
      "link": "https://futbolibretv.pages.dev/#partido-26487"
    },
    {
      "partido": "Copa Paraguay: Cerro Porteño vs General Caballero JLM",
      "link": "https://futbolibretv.pages.dev/#partido-26516"
    },
    {
      "partido": "Copa Sudamericana: Universidad Chile vs Lanús",
      "link": "https://futbolibretv.pages.dev/#partido-26508"
    },
    {
      "partido": "Copa Caribe de la Concacaf: Universidad O&M vs Cibao",
      "link": "https://futbolibretv.pages.dev/#partido-26513"
    },
    {
      "partido": "Amistoso Internacional Femenino: EE. UU. vs Portugal",
      "link": "https://futbolibretv.pages.dev/#partido-26517"
    },
    {
      "partido": "División Profesional: Gualberto Villarroel SJ vs The Strongest",
      "link": "https://futbolibretv.pages.dev/#partido-26515"
    },
    {
      "partido": "Copa Argentina: Belgrano vs Argentinos Juniors",
      "link": "https://futbolibretv.pages.dev/#partido-26510"
    },
    {
      "partido": "Copa Libertadores: LDU Quito vs Palmeiras",
      "link": "https://futbolibretv.pages.dev/#partido-26509"
    },
    {
      "partido": "Liga 1: Sporting Cristal vs Universitario",
      "link": "https://futbolibretv.pages.dev/#partido-26471"
    },
    {
      "partido": "Copa Centroamericana: Alajuelense vs Olimpia",
      "link": "https://futbolibretv.pages.dev/#partido-26512"
    },
    {
      "partido": "Amistoso Internacional Femenino: México vs Nueva Zelanda",
      "link": "https://futbolibretv.pages.dev/#partido-26518"
    }
  ]
}

# ========================
# FUNCIONES PARA FORMATEAR PARTIDOS
# ========================
def formato_limpio(partido_completo):
    """Quita la liga/torneo, deja solo equipos vs equipos"""
    # Busca el patron "liga: equipo vs equipo"
    match = re.search(r':\s*(.+)', partido_completo)
    if match:
        return match.group(1).strip()  # Solo "equipo vs equipo"
    return partido_completo  # Si no encuentra ":", devuelve completo

def formato_completo(partido_completo):
    """Mantiene el formato completo con liga/torneo"""
    return partido_completo

# ========================
# FOOTER PARA TODOS LOS MENSAJES (EXCEPTO START/MENU)
# ========================
def add_footer():
    return "\n\n🤔 *¿Quieres hacer algo más?*\nVolver al menú principal /menu"

def add_search_footer():
    return "\n\n🤔 *¿Quieres hacer algo más?*\nBuscar otro partido o /menu"

# ========================
# COMANDO /start Y /menu (SIN FOOTER)
# ========================
@bot.message_handler(commands=['start', 'menu'])
def send_welcome(message):
    user_name = message.from_user.first_name
    welcome_text = f"""¡Hola {user_name}! 👋

Soy *FulbiBot*, tu asistente para ver partidos gratis.

✅ *Comandos disponibles:*
/partidos - Ver los partidos de hoy
/ayuda - Guía completa y soluciones

*¿Buscas un partido específico?* 🔍
¡Solo escribe el nombre del equipo o una palabra clave relacionada! ⚡

¡Elige un comando y disfruta del fútbol! 🎉"""

    # SIN FOOTER en start/menu
    bot.reply_to(message, welcome_text, parse_mode='Markdown')
    print(f"✅ /{message.text[1:]} enviado a {user_name}")

# ========================
# COMANDO /partidos (CON FOOTER - FORMATO LIMPIO)
# ========================
@bot.message_handler(commands=['partidos'])
def send_matches(message):
    try:
        partidos = PARTIDOS_JSON["partidos"]

        if partidos:
            partidos_text = "⚽️ *PARTIDOS DE HOY* ⚽️\n\n"

            for i, partido in enumerate(partidos, 1):
                # FORMATO LIMPIO: solo equipos vs equipos
                partido_limpio = formato_limpio(partido['partido'])
                partidos_text += f"*{i}. {partido_limpio}*\n"
                partidos_text += f"🔗 {partido['link']}\n\n"

            partidos_text += "\n\n**Para buscar un partido en específico, escribí directamente el nombre de tu equipo o el de su liga.** ⭐"
        else:
            partidos_text = "❌ *No hay partidos disponibles en este momento.*\n\nIntenta más tarde o usa /ayuda para soporte."

        full_message = partidos_text + add_footer()
        bot.reply_to(message, full_message, parse_mode='Markdown')
        print("✅ /partidos enviado (formato limpio)")

    except Exception as e:
        print(f"Error en /partidos: {e}")
        error_message = "❌ Error al cargar los partidos. Intenta más tarde." + add_footer()
        bot.reply_to(message, error_message, parse_mode='Markdown')

# ========================
# COMANDO /ayuda CON INLINE KEYBOARD (BOTONES UNO ENCIMA DE OTRO)
# ========================
@bot.message_handler(commands=['ayuda'])
def send_help(message):
    # Crear inline keyboard con botones uno encima del otro (row_width=1)
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        InlineKeyboardButton("📱 Solución Celular (VPN)", callback_data="help_vpn"),
        InlineKeyboardButton("💻 Solución PC/TV (DNS)", callback_data="help_dns"),
        InlineKeyboardButton("🌐 Modo Incógnito", callback_data="help_incognito")
    )

    help_text = """📖 *AYUDA RÁPIDA* 📖

❌ *¿No puedes ver el partido?*
👉 Prueba primero estas soluciones:

📱 *En celular* → usar VPN (desbloquea los links)
💻 *En PC/TV* → cambiar DNS (arregla pantalla negra)
⚽️ *También te recomendamos usar modo incógnito*

📝 *Nota:* Si ninguna opción te funciona, puede ser un fallo del proveedor del servidor. Espera un momento y vuelve a intentar.

👇 *Elige una opción:*"""

    full_message = help_text + add_footer()
    bot.send_message(message.chat.id, full_message, 
                    parse_mode='Markdown', reply_markup=keyboard)
    print("✅ /ayuda enviado con inline keyboard")

# ========================
# MANEJAR CALLBACKS DE INLINE KEYBOARD
# ========================
@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    if call.data == "help_vpn":
        response = """📱 *SOLUCIÓN CELULAR - VPN*

*¿Problema?* ❌ Links bloqueados o no cargan

*Solución:* Usar VPN para desbloquear

1. *Descarga una app VPN gratis:*
   📲 Turbo VPN (Android/iOS)
   📲 Windscribe 
   📲 Hotspot Shield
   📲 Cloudflare WARP (1.1.1.1)

2. *Pasos a seguir:*
   • Abre la app VPN
   • Toca "Conectar" o "Connect"
   • Elige cualquier país
   • Listo ✅ Ahora prueba el link

*Nota:* La VPN evita que tu compañía de internet bloquee los partidos.

💡 *Esta solución es 100% efectiva. Si aún así no te funciona, puede deberse a tu conexión a internet.*"""

    elif call.data == "help_dns":
        response = """💻 *SOLUCIÓN PC/TV - DNS*

*¿Problema?* ❌ Pantalla negra o "stream no disponible"

*Solución:* Cambiar DNS para saltar restricciones

*DNS Recomendados:*
🔹 Google: 8.8.8.8 y 8.8.4.4
🔹 Cloudflare: 1.1.1.1 y 1.0.0.1

*¿Cómo cambiar DNS?*

📱 *En Android:*
   Ajustes → Redes → DNS privado → Ingresa: 1.1.1.1

💻 *En Windows:*
   Panel Control → Red → Adaptador → Propiedades → IPv4 → Usar DNS

📺 *En Smart TV:*
   Configuración → Red → DNS manual

🔄 *Reinicia el navegador después de cambiar DNS*

💡 *Esta solución es 100% efectiva. Si aún así no te funciona, puede deberse a tu conexión a internet.*"""

    elif call.data == "help_incognito":
        response = """🌐 *MODO INCÓGNITO*

*¿Problema?* ❌ Página carga mal o da error

*Solución:* Probar en modo incógnito

*Pasos rápidos:*

📱 *En Chrome/Edge:*
   • Toca los 3 puntos ⋮
   • "Nueva pestaña incógnito"
   • O usa: Ctrl+Shift+N (PC)

📱 *En Firefox:*
   • Toca los 3 puntos ⋮  
   • "Nueva pestaña privada"
   • O usa: Ctrl+Shift+P (PC)

📱 *En Safari:*
   • Toca los cuadrados []
   • "Privado"
   • O usa: Cmd+Shift+N (Mac)

*¿Por qué funciona?*
El modo incógnito evita problemas de cache, cookies y extensiones que pueden bloquear el stream.

💡 *Esta solución es 100% efectiva. Si aún así no te funciona, puede deberse a tu conexión a internet.*"""

    # Enviar respuesta
    full_response = response + add_footer()
    bot.send_message(call.message.chat.id, full_response, parse_mode='Markdown')
    bot.answer_callback_query(call.id)

# ========================
# SISTEMA DE BÚSQUEDA INTELIGENTE MEJORADO
# ========================
def search_matches(message, search_term):
    """Buscar partidos que coincidan con el término de búsqueda - VERSIÓN MEJORADA"""
    try:
        partidos = PARTIDOS_JSON["partidos"]
        matches = []
        
        # Limpiar y normalizar el término de búsqueda
        search_clean = re.sub(r'[-–—vsVS]', ' ', search_term)  # Reemplaza "-", "vs", etc. por espacios
        search_clean = re.sub(r'\s+', ' ', search_clean).strip().lower()  # Normaliza espacios
        
        print(f"🔍 Búsqueda original: '{search_term}' → Normalizada: '{search_clean}'")
        
        for partido in partidos:
            partido_text = partido['partido'].lower()
            
            # BUSQUEDA MEJORADA - Múltiples estrategias:
            
            # 1. Búsqueda exacta original (para compatibilidad)
            if search_term in partido_text:
                matches.append(partido)
                continue
                
            # 2. Búsqueda con términos normalizados
            if search_clean in partido_text:
                matches.append(partido)
                continue
                
            # 3. Búsqueda por palabras individuales (si el usuario puso varios equipos)
            search_words = search_clean.split()
            if len(search_words) >= 2:
                # Si el usuario escribió algo como "real madrid juventus"
                all_words_match = all(word in partido_text for word in search_words)
                if all_words_match:
                    matches.append(partido)
                    continue
            
            # 4. Búsqueda flexible para casos como "real madrid - juventus" vs "real madrid vs juventus"
            partido_clean = re.sub(r'[-–—vsVS:]', ' ', partido_text)  # Limpia el texto del partido también
            partido_clean = re.sub(r'\s+', ' ', partido_clean).strip()
            
            if search_clean in partido_clean:
                matches.append(partido)
                continue
        
        # Eliminar duplicados por si alguna estrategia encontró el mismo partido múltiples veces
        unique_matches = []
        seen_links = set()
        for match in matches:
            if match['link'] not in seen_links:
                unique_matches.append(match)
                seen_links.add(match['link'])
        
        if unique_matches:
            # Mostrar resultados de búsqueda CON FORMATO COMPLETO
            result_text = f"🔍 *Resultados para '{search_term}'*:\n\n"
            
            for i, match in enumerate(unique_matches, 1):
                # FORMATO COMPLETO: con liga/torneo
                result_text += f"*{i}. {match['partido']}*\n"
                result_text += f"🔗 {match['link']}\n\n"
            
            result_text += f"_📊 Encontré {len(unique_matches)} partido(s)_"
            
            full_message = result_text + add_search_footer()
            bot.reply_to(message, full_message, parse_mode='Markdown')
            print(f"🔍 Búsqueda exitosa: '{search_term}' → {len(unique_matches)} resultados")
            
        else:
            # Si no encuentra resultados - ESTO NO ES UN ERROR, es normal
            result_text = f"❌ *No encontré '*'{search_term}'* en la agenda de hoy*\n\n"
            result_text += "💡 *Sugerencias:*\n"
            result_text += "• Escribe solo un equipo (ej: 'real madrid')\n"
            result_text += "• O escribe solo 'champions' para ver todos\n"
            result_text += "• Usa /partidos para ver toda la agenda\n\n"
            result_text += "⚽ *Equipos disponibles hoy:* Real Madrid, Juventus, Barcelona, Liverpool, etc."
            
            full_message = result_text + add_search_footer()
            bot.reply_to(message, full_message, parse_mode='Markdown')
            print(f"🔍 Búsqueda sin resultados: '{search_term}'")
        
    except Exception as e:
        # SOLO mostrar error si es una excepción real
        print(f"❌ ERROR REAL en búsqueda: {e}")
        
        # Si hay error, mostrar mensaje simple
        error_message = "❌ Error temporal. Intenta con términos más simples como 'real madrid' o 'juventus'." + add_footer()
        bot.reply_to(message, error_message, parse_mode='Markdown')

# ========================
# MANEJAR TODOS LOS MENSAJES
# ========================
@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    text = message.text.strip().lower()

    # Si es un comando conocido, manejarlo primero
    if text in ["/start", "/partidos", "/ayuda", "/menu"]:
        return

    # Si no es comando, es una búsqueda
    search_matches(message, text)

# ========================
# MANTENER BOT ACTIVO (CON MEJOR MANEJO)
# ========================
def run_bot():
    print("🤖 Bot iniciado en Render - 24/7 activo")

    while True:
        try:
            # Timeout más corto para mejor respuesta
            bot.polling(none_stop=True, timeout=30, skip_pending=True)

        except Exception as e:
            error_msg = str(e)
            print(f"❌ Error en polling: {error_msg}")

            if "409" in error_msg:
                print("🚨 CONFLICTO: Otra instancia detectada")
                time.sleep(30)
            elif "Timed out" in error_msg or "Timeout" in error_msg:
                print("⏰ Timeout, reconectando...")
                time.sleep(5)
            else:
                print("🔧 Error genérico, reconectando en 10s...")
                time.sleep(10)

@app.route('/')
def home():
    return "✅ Bot activo - Render 24/7"

# Iniciar todo
if __name__ == "__main__":
    # Bot en hilo separado
    bot_thread = threading.Thread(target=run_bot)
    bot_thread.daemon = True
    bot_thread.start()

    # Web server
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
