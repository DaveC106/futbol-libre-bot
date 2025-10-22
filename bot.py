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
      "partido": "AFC Champions League Two: Goa vs Al Nassr",
      "link": "https://futbolibretv.pages.dev/#partido-26445"
    },
    {
      "partido": "UEFA Champions League: Athletic Club vs Qarabağ",
      "link": "https://futbolibretv.pages.dev/#partido-26428"
    },
    {
      "partido": "UEFA Champions League: Galatasaray vs Bodø / Glimt",
      "link": "https://futbolibretv.pages.dev/#partido-26427"
    },
    {
      "partido": "Super Lig: Konyaspor vs Beşiktaş",
      "link": "https://futbolibretv.pages.dev/#partido-26454"
    },
    {
      "partido": "Championship: Watford vs West Bromwich Albion",
      "link": "https://futbolibretv.pages.dev/#partido-26441"
    },
    {
      "partido": "Championship: Wrexham vs Oxford United",
      "link": "https://futbolibretv.pages.dev/#partido-26442"
    },
    {
      "partido": "UEFA Champions League: Real Madrid vs Juventus",
      "link": "https://futbolibretv.pages.dev/#partido-26431"
    },
    {
      "partido": "UEFA Champions League: Eintracht Frankfurt vs Liverpool",
      "link": "https://futbolibretv.pages.dev/#partido-26432"
    },
    {
      "partido": "UEFA Champions League: Chelsea vs Ajax",
      "link": "https://futbolibretv.pages.dev/#partido-26433"
    },
    {
      "partido": "Championship: Sheffield Wednesday vs Middlesbrough",
      "link": "https://futbolibretv.pages.dev/#partido-26443"
    },
    {
      "partido": "UEFA Champions League: Bayern München vs Club Brugge",
      "link": "https://futbolibretv.pages.dev/#partido-26429"
    },
    {
      "partido": "UEFA Champions League: Atalanta vs Slavia Praha",
      "link": "https://futbolibretv.pages.dev/#partido-26434"
    },
    {
      "partido": "Copa Mundial Femenina Sub-17 de la FIFA: Ivory Coast vs Colombia",
      "link": "https://futbolibretv.pages.dev/#partido-26446"
    },
    {
      "partido": "División Profesional: ABB vs Real Oruro",
      "link": "https://futbolibretv.pages.dev/#partido-26457"
    },
    {
      "partido": "UEFA Champions League: Monaco vs Tottenham Hotspur",
      "link": "https://futbolibretv.pages.dev/#partido-26430"
    },
    {
      "partido": "UEFA Champions League: Sporting CP vs Olympique Marseille",
      "link": "https://futbolibretv.pages.dev/#partido-26435"
    },
    {
      "partido": "Major League Soccer: Chicago Fire vs Orlando City SC",
      "link": "https://futbolibretv.pages.dev/#partido-26455"
    },
    {
      "partido": "Major League Soccer: Portland Timbers vs Real Salt Lake",
      "link": "https://futbolibretv.pages.dev/#partido-26456"
    },
    {
      "partido": "Serie B: Cumbayá vs Atlético Vinotinto",
      "link": "https://futbolibretv.pages.dev/#partido-26462"
    },
    {
      "partido": "Serie B: San Antonio vs Gualaceo",
      "link": "https://futbolibretv.pages.dev/#partido-26460"
    },
    {
      "partido": "Copa Ecuador: Deportivo Cuenca Juniors vs Nueve de Octubre",
      "link": "https://futbolibretv.pages.dev/#partido-26439"
    },
    {
      "partido": "Serie B: Chacaritas vs Vargas Torres",
      "link": "https://futbolibretv.pages.dev/#partido-26461"
    },
    {
      "partido": "Copa Paraguay: Nacional Asunción vs 12 de Octubre",
      "link": "https://futbolibretv.pages.dev/#partido-26468"
    },
    {
      "partido": "Brasileirão: Bahia vs Internacional",
      "link": "https://futbolibretv.pages.dev/#partido-26437"
    },
    {
      "partido": "Copa Caribe de la Concacaf: Defence Force vs Mount Pleasant Academy",
      "link": "https://futbolibretv.pages.dev/#partido-26453"
    },
    {
      "partido": "División Profesional: Universitario de Vinto vs Nacional Potosí",
      "link": "https://futbolibretv.pages.dev/#partido-26458"
    },
    {
      "partido": "Liga Profesional: Huracán vs Central Córdoba SdE",
      "link": "https://futbolibretv.pages.dev/#partido-26436"
    },
    {
      "partido": "Copa Paraguay: Guaraní vs River Plate",
      "link": "https://futbolibretv.pages.dev/#partido-26469"
    },
    {
      "partido": "Copa Ecuador: Guayaquil City vs Emelec",
      "link": "https://futbolibretv.pages.dev/#partido-26440"
    },
    {
      "partido": "Copa Colombia: Atlético Nacional vs Once Caldas",
      "link": "https://futbolibretv.pages.dev/#partido-26459"
    },
    {
      "partido": "Copa Centroamericana: Sporting San Miguelito vs Plaza Amador",
      "link": "https://futbolibretv.pages.dev/#partido-26447"
    },
    {
      "partido": "Copa Libertadores: Flamengo vs Racing Club",
      "link": "https://futbolibretv.pages.dev/#partido-26438"
    },
    {
      "partido": "Liga MX: Querétaro vs Guadalajara",
      "link": "https://futbolibretv.pages.dev/#partido-26463"
    },
    {
      "partido": "Liga MX: Pachuca vs Tigres UANL",
      "link": "https://futbolibretv.pages.dev/#partido-26464"
    },
    {
      "partido": "Copa Centroamericana: Real España vs Xelajú",
      "link": "https://futbolibretv.pages.dev/#partido-26448"
    },
    {
      "partido": "Liga MX: Atlas vs León",
      "link": "https://futbolibretv.pages.dev/#partido-26466"
    },
    {
      "partido": "Liga MX: Tijuana vs Toluca",
      "link": "https://futbolibretv.pages.dev/#partido-26465"
    },
    {
      "partido": "Liga MX: Pumas UNAM vs Atlético San Luis",
      "link": "https://futbolibretv.pages.dev/#partido-26467"
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
# SISTEMA DE BÚSQUEDA INTELIGENTE (CON MEJOR MANEJO DE ERRORES)
# ========================
def search_matches(message, search_term):
    """Buscar partidos que coincidan con el término de búsqueda"""
    try:
        partidos = PARTIDOS_JSON["partidos"]
        matches = []
        
        for partido in partidos:
            # Buscar en el nombre COMPLETO del partido (con liga/torneo)
            if search_term in partido['partido'].lower():
                matches.append(partido)
        
        if matches:
            # Mostrar resultados de búsqueda CON FORMATO COMPLETO
            result_text = f"🔍 *Resultados para '{search_term.title()}'*:\n\n"
            
            for i, match in enumerate(matches, 1):
                # FORMATO COMPLETO: con liga/torneo
                result_text += f"*{i}. {match['partido']}*\n"
                result_text += f"🔗 {match['link']}\n\n"
            
            result_text += f"_📊 Encontré {len(matches)} partido(s)_"
            
            full_message = result_text + add_search_footer()
            bot.reply_to(message, full_message, parse_mode='Markdown')
            print(f"🔍 Búsqueda exitosa: '{search_term}' → {len(matches)} resultados")
            
        else:
            # Si no encuentra resultados - ESTO NO ES UN ERROR, es normal
            result_text = f"❌ *No encontré partidos con '*'{search_term.title()}'*\n\n"
            result_text += "💡 *Sugerencias:*\n"
            result_text += "• Revisa la ortografía\n"
            result_text += "• Usa términos más generales (ej: 'champions', 'liga mx')\n"
            result_text += "• Ver todos los partidos con /partidos"
            
            full_message = result_text + add_search_footer()
            bot.reply_to(message, full_message, parse_mode='Markdown')
            print(f"🔍 Búsqueda sin resultados: '{search_term}'")
        
    except Exception as e:
        # SOLO mostrar error si es una excepción real, no cuando no encuentra resultados
        print(f"❌ ERROR REAL en búsqueda: {e}")
        print(f"🔍 Tipo de error: {type(e).__name__}")
        
        # Intentar una vez más antes de mostrar error al usuario
        try:
            print("🔄 Reintentando búsqueda...")
            partidos = PARTIDOS_JSON["partidos"]
            matches = []
            
            for partido in partidos:
                if search_term in partido['partido'].lower():
                    matches.append(partido)
            
            if matches:
                result_text = f"🔍 *Resultados para '{search_term.title()}'*:\n\n"
                for i, match in enumerate(matches, 1):
                    result_text += f"*{i}. {match['partido']}*\n"
                    result_text += f"🔗 {match['link']}\n\n"
                result_text += f"_📊 Encontré {len(matches)} partido(s)_"
                
                full_message = result_text + add_search_footer()
                bot.reply_to(message, full_message, parse_mode='Markdown')
                print(f"🔍 Búsqueda recuperada: '{search_term}' → {len(matches)} resultados")
                return
                
        except Exception as retry_error:
            print(f"❌ Error también en reintento: {retry_error}")
        
        # Si llegamos aquí, es un error real después de reintentar
        error_message = "❌ Error temporal en la búsqueda. Vuelve a intentar en un momento." + add_footer()
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
