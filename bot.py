import telebot
from flask import Flask
import threading
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import os
import re
import time

TOKEN = os.environ.get('BOT_TOKEN')
if not TOKEN:
    raise ValueError("❌ BOT_TOKEN no encontrado en variables de entorno")

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# ========================
# PARTIDOS DIRECTAMENTE EN EL CÓDIGO.
# ========================
PARTIDOS_JSON = {
  "partidos": [
    {
      "partido": "Copa Mundial Femenina Sub-17 de la FIFA: Ecuador vs China PR",
      "link": "https://futbolibretv.pages.dev/#partido-26539"
    },
    {
      "partido": "UEFA Nations League Femenina: Alemania vs Francia",
      "link": "https://futbolibretv.pages.dev/#partido-26540"
    },
    {
      "partido": "2. Bundesliga: Schalke 04 vs Darmstadt 98",
      "link": "https://futbolibretv.pages.dev/#partido-26537"
    },
    {
      "partido": "2. Bundesliga: Greuther Fürth vs Karlsruher SC",
      "link": "https://futbolibretv.pages.dev/#partido-26538"
    },
    {
      "partido": "Eredivisie: Heerenveen vs NAC Breda",
      "link": "https://futbolibretv.pages.dev/#partido-26549"
    },
    {
      "partido": "Eerste Divisie: Vitesse vs Roda JC",
      "link": "https://futbolibretv.pages.dev/#partido-26550"
    },
    {
      "partido": "Pro League: Al Ittihad vs Al Hilal",
      "link": "https://futbolibretv.pages.dev/#partido-26551"
    },
    {
      "partido": "UEFA Nations League Femenina: España vs Suecia",
      "link": "https://futbolibretv.pages.dev/#partido-26541"
    },
    {
      "partido": "Bundesliga: Werder Bremen vs Union Berlin",
      "link": "https://futbolibretv.pages.dev/#partido-26525"
    },
    {
      "partido": "LaLiga SmartBank: Huesca vs Las Palmas",
      "link": "https://futbolibretv.pages.dev/#partido-26556"
    },
    {
      "partido": "Ligue 1: Paris vs Nantes",
      "link": "https://futbolibretv.pages.dev/#partido-26526"
    },
    {
      "partido": "Serie A: Milan vs Pisa",
      "link": "https://futbolibretv.pages.dev/#partido-26524"
    },
    {
      "partido": "Premier League: Leeds United vs West Ham United",
      "link": "https://futbolibretv.pages.dev/#partido-26522"
    },
    {
      "partido": "LaLiga: Real Sociedad vs Sevilla",
      "link": "https://futbolibretv.pages.dev/#partido-26523"
    },
    {
      "partido": "Liga Profesional: Sarmiento vs Rosario Central",
      "link": "https://futbolibretv.pages.dev/#partido-26527"
    },
    {
      "partido": "Liga 1: Juan Pablo II College vs Comerciantes Unidos",
      "link": "https://futbolibretv.pages.dev/#partido-26521"
    },
    {
      "partido": "Primera División: Palestino vs Everton",
      "link": "https://futbolibretv.pages.dev/#partido-26529"
    },
    {
      "partido": "CONMEBOL Nations League Femenina: Amazon Prime Video, ViX",
      "link": "https://futbolibretv.pages.dev/#partido-26552"
    },
    {
      "partido": "Primera A: Alianza vs La Equidad",
      "link": "https://futbolibretv.pages.dev/#partido-26530"
    },
    {
      "partido": "CONMEBOL Nations League Femenina: Venezuela vs Chile",
      "link": "https://futbolibretv.pages.dev/#partido-26553"
    },
    {
      "partido": "Liga Profesional: Independiente vs Platense",
      "link": "https://futbolibretv.pages.dev/#partido-26528"
    },
    {
      "partido": "Serie B: Novorizontino vs Botafogo SP",
      "link": "https://futbolibretv.pages.dev/#partido-26544"
    },
    {
      "partido": "Primera División: Defensor Sporting vs Torque",
      "link": "https://futbolibretv.pages.dev/#partido-26535"
    },
    {
      "partido": "Primera A: Fortaleza CEIF vs Deportivo Pasto",
      "link": "https://futbolibretv.pages.dev/#partido-26531"
    },
    {
      "partido": "CONMEBOL Nations League Femenina: Colombia vs Perú",
      "link": "https://futbolibretv.pages.dev/#partido-26555"
    },
    {
      "partido": "CONMEBOL Nations League Femenina: Argentina vs Paraguay",
      "link": "https://futbolibretv.pages.dev/#partido-26554"
    },
    {
      "partido": "Serie A: Orense vs Universidad Católica",
      "link": "https://futbolibretv.pages.dev/#partido-26534"
    },
    {
      "partido": "Major League Soccer: Inter Miami vs Nashville SC",
      "link": "https://futbolibretv.pages.dev/#partido-26543"
    },
    {
      "partido": "Serie B: Cuiabá vs Remo",
      "link": "https://futbolibretv.pages.dev/#partido-26545"
    },
    {
      "partido": "Liga de Expansión MX: Alebrijes de Oaxaca vs Tepatitlán",
      "link": "https://futbolibretv.pages.dev/#partido-26542"
    },
    {
      "partido": "Primera División: San Carlos vs Guadalupe",
      "link": "https://futbolibretv.pages.dev/#partido-26546"
    },
    {
      "partido": "Liga MX: Juárez vs Puebla",
      "link": "https://futbolibretv.pages.dev/#partido-26547"
    },
    {
      "partido": "Primera A: Deportivo Pereira vs Rionegro Águilas",
      "link": "https://futbolibretv.pages.dev/#partido-26533"
    },
    {
      "partido": "Copa Argentina: Independiente Rivadavia vs River Plate",
      "link": "https://futbolibretv.pages.dev/#partido-26536"
    },
    {
      "partido": "Primera A: América de Cali vs Junior",
      "link": "https://futbolibretv.pages.dev/#partido-26532"
    },
    {
      "partido": "Liga MX: Mazatlán vs América",
      "link": "https://futbolibretv.pages.dev/#partido-26548"
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
    """Buscar partidos que coincidan con el término de búsqueda - VERSIÓN BALANCEADA"""
    try:
        partidos = PARTIDOS_JSON["partidos"]
        matches = []
        
        search_clean = re.sub(r'[-–—vsVS]', ' ', search_term)
        search_clean = re.sub(r'\s+', ' ', search_clean).strip().lower()
        
        print(f"🔍 Búsqueda original: '{search_term}' → Normalizada: '{search_clean}'")
        
        for partido in partidos:
            partido_text = partido['partido'].lower()
            
            # SEPARAR LIGA Y EQUIPOS
            if ":" in partido_text:
                liga = partido_text.split(":")[0].strip()  # Ej: "premier league"
                equipos = partido_text.split(":")[1].strip()  # Ej: "leeds united vs west ham united"
            else:
                liga = ""
                equipos = partido_text
            
            # ESTRATEGIAS DE BÚSQUEDA BALANCEADAS:
            
            # 1. Búsqueda en LIGA (más permisiva)
            if search_clean in liga:
                matches.append(partido)
                continue
                
            # 2. Búsqueda en EQUIPOS (más estricta)
            search_words = search_clean.split()
            if len(search_words) == 1:
                # Una palabra: buscar como palabra completa en equipos
                if re.search(r'\b' + re.escape(search_clean) + r'\b', equipos):
                    matches.append(partido)
                    continue
            else:
                # Múltiples palabras: buscar que TODAS estén en equipos
                all_words_match = all(re.search(r'\b' + re.escape(word) + r'\b', equipos) for word in search_words)
                if all_words_match:
                    matches.append(partido)
                    continue
            
            # 3. Búsqueda flexible para nombres cortos (ej: "sev" → "sevilla")
            if len(search_clean) >= 3:
                equipos_list = re.split(r' vs | - ', equipos)
                for equipo in equipos_list:
                    equipo_limpio = equipo.strip()
                    if search_clean in equipo_limpio and any(palabra.startswith(search_clean) for palabra in equipo_limpio.split()):
                        matches.append(partido)
                        break
        
        # Eliminar duplicados
        unique_matches = []
        seen_links = set()
        for match in matches:
            if match['link'] not in seen_links:
                unique_matches.append(match)
                seen_links.add(match['link'])
        
        if unique_matches:
            result_text = f"🔍 *Resultados para '{search_term}'*:\n\n"
            
            for i, match in enumerate(unique_matches, 1):
                result_text += f"*{i}. {match['partido']}*\n"
                result_text += f"🔗 {match['link']}\n\n"
            
            result_text += f"_📊 Encontré {len(unique_matches)} partido(s)_"
            
            full_message = result_text + add_search_footer()
            bot.reply_to(message, full_message, parse_mode='Markdown')
            print(f"🔍 Búsqueda exitosa: '{search_term}' → {len(unique_matches)} resultados")
            
        else:
            result_text = f"❌ *No encontré '*'{search_term}'* en la agenda de hoy*\n\n"
            result_text += "💡 *Sugerencias:*\n"
            result_text += "• Escribe el nombre del equipo o liga\n"
            result_text += "• Ejemplos: 'premier', 'sevilla', 'champions'\n"
            result_text += "• Usa /partidos para ver toda la agenda"
            
            full_message = result_text + add_search_footer()
            bot.reply_to(message, full_message, parse_mode='Markdown')
            print(f"🔍 Búsqueda sin resultados: '{search_term}'")
        
    except Exception as e:
        print(f"❌ ERROR en búsqueda: {e}")
        error_message = "❌ Error temporal. Intenta con términos más específicos." + add_footer()
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
