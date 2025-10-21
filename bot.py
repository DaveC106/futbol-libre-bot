import telebot
from flask import Flask
import threading
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import os

TOKEN = "7640481513:AAG9lbUvQGRjLYaHmp91LFKJo3O_YIY7RIw"
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# ========================
# PARTIDOS DIRECTAMENTE EN EL CÓDIGO
# ========================
PARTIDOS_JSON = {
  "partidos": [ 
    {
      "partido": "Barcelona vs Olympiakos Piraeus",
      "link": "https://futbolibretv.pages.dev/#partido-26394"
    },
    {
      "partido": "Kairat vs Paphos",
      "link": "https://futbolibretv.pages.dev/#partido-26395"
    },
    {
      "partido": "MVV vs Vitesse",
      "link": "https://futbolibretv.pages.dev/#partido-26423"
    },
    {
      "partido": "Oss vs Ajax II",
      "link": "https://futbolibretv.pages.dev/#partido-26421"
    },
    {
      "partido": "Den Bosch vs Helmond Sport",
      "link": "https://futbolibretv.pages.dev/#partido-26422"
    },
    {
      "partido": "Al Hilal vs Al Sadd",
      "link": "https://futbolibretv.pages.dev/#partido-26407"
    },
    {
      "partido": "PSV vs Napoli",
      "link": "https://futbolibretv.pages.dev/#partido-26396"
    },
    {
      "partido": "Villarreal vs Manchester City",
      "link": "https://futbolibretv.pages.dev/#partido-26401"
    },
    {
      "partido": "Noruega vs Ecuador",
      "link": "https://futbolibretv.pages.dev/#partido-26408"
    },
    {
      "partido": "Always Ready vs Blooming",
      "link": "https://futbolibretv.pages.dev/#partido-26418"
    },
    {
      "partido": "Union Saint-Gilloise vs Internazionale",
      "link": "https://futbolibretv.pages.dev/#partido-26397"
    },
    {
      "partido": "Newcastle United vs Benfica",
      "link": "https://futbolibretv.pages.dev/#partido-26402"
    },
    {
      "partido": "Bristol City vs Southampton",
      "link": "https://futbolibretv.pages.dev/#partido-26406"
    },
    {
      "partido": "Bayer Leverkusen vs PSG",
      "link": "https://futbolibretv.pages.dev/#partido-26398"
    },
    {
      "partido": "Arsenal vs Atlético Madrid",
      "link": "https://futbolibretv.pages.dev/#partido-26399"
    },
    {
      "partido": "København vs Borussia Dortmund",
      "link": "https://futbolibretv.pages.dev/#partido-26400"
    },
    {
      "partido": "Atlético Huila vs Real Cundinamarca",
      "link": "https://futbolibretv.pages.dev/#partido-26417"
    },
    {
      "partido": "Atlético Tembetary vs 2 de Mayo",
      "link": "https://futbolibretv.pages.dev/#partido-26424"
    },
    {
      "partido": "Unión Santa Fe vs Defensa y Justicia",
      "link": "https://futbolibretv.pages.dev/#partido-26403"
    },
    {
      "partido": "Portland Hearts of Pine vs Spokane Velocity",
      "link": "https://futbolibretv.pages.dev/#partido-26416"
    },
    {
      "partido": "Millonarios vs Atlético Bucaramanga",
      "link": "https://futbolibretv.pages.dev/#partido-26404"
    },
    {
      "partido": "Real Tomayapo vs Bolívar",
      "link": "https://futbolibretv.pages.dev/#partido-26419"
    },
    {
      "partido": "Independiente del Valle vs Atlético Mineiro",
      "link": "https://futbolibretv.pages.dev/#partido-26405"
    },
    {
      "partido": "Deportivo Pereira vs Envigado",
      "link": "https://futbolibretv.pages.dev/#partido-26420"
    },
    {
      "partido": "América vs Puebla",
      "link": "https://futbolibretv.pages.dev/#partido-26412"
    },
    {
      "partido": "Necaxa vs Cruz Azul",
      "link": "https://futbolibretv.pages.dev/#partido-26413"
    },
    {
      "partido": "Cartaginés vs Motagua",
      "link": "https://futbolibretv.pages.dev/#partido-26409"
    },
    {
      "partido": "Mazatlán vs Santos Laguna",
      "link": "https://futbolibretv.pages.dev/#partido-26414"
    },
    {
      "partido": "Monterrey vs Juárez",
      "link": "https://futbolibretv.pages.dev/#partido-26415"
    }
  ]
}

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
¡Solo escribe el nombre del equipo que quieres ver! ⚡

¡Elige un comando y disfruta del fútbol! 🎉"""
    
    # SIN FOOTER en start/menu
    bot.reply_to(message, welcome_text, parse_mode='Markdown')
    print(f"✅ /{message.text[1:]} enviado a {user_name}")

# ========================
# COMANDO /partidos (CON FOOTER)
# ========================
@bot.message_handler(commands=['partidos'])
def send_matches(message):
    try:
        partidos = PARTIDOS_JSON["partidos"]
        
        if partidos:
            partidos_text = "⚽️ *PARTIDOS DE HOY* ⚽️\n\n"
            
            for i, partido in enumerate(partidos, 1):
                partidos_text += f"*{i}. {partido['partido']}*\n"
                partidos_text += f"🔗 {partido['link']}\n\n"
            
            partidos_text += "_⚠️ Los links pueden requerir VPN/DNS_"
        else:
            partidos_text = "❌ *No hay partidos disponibles en este momento.*\n\nIntenta más tarde o usa /ayuda para soporte."
        
        full_message = partidos_text + add_footer()
        bot.reply_to(message, full_message, parse_mode='Markdown')
        print("✅ /partidos enviado")
        
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
        # ❌ ELIMINADO: Botón "Cerrar" - ya no es necesario
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
# MANEJAR CALLBACKS DE INLINE KEYBOARD (VERSIÓN MEJORADA)
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
# SISTEMA DE BÚSQUEDA INTELIGENTE (CON FOOTER)
# ========================
def search_matches(message, search_term):
    """Buscar partidos que coincidan con el término de búsqueda"""
    try:
        partidos = PARTIDOS_JSON["partidos"]
        matches = []
        
        for partido in partidos:
            # Buscar en el nombre del partido
            if search_term in partido['partido'].lower():
                matches.append(partido)
        
        if matches:
            # Mostrar resultados de búsqueda
            result_text = f"🔍 *Resultados para '{search_term.title()}'*:\n\n"
            
            for i, match in enumerate(matches, 1):
                result_text += f"*{i}. {match['partido']}*\n"
                result_text += f"🔗 {match['link']}\n\n"
            
            result_text += f"_📊 Encontré {len(matches)} partido(s)_"
            
        else:
            # Si no encuentra resultados
            result_text = f"❌ *No encontré partidos con '*'{search_term.title()}'*\n\n"
            result_text += "💡 *Sugerencias:*\n"
            result_text += "• Revisa la ortografía\n"
            result_text += "• Usa términos más generales (ej: 'boca', 'madrid')\n"
            result_text += "• Ver todos los partidos con /partidos"
        
        full_message = result_text + add_search_footer()
        bot.reply_to(message, full_message, parse_mode='Markdown')
        print(f"🔍 Búsqueda: '{search_term}' → {len(matches)} resultados")
        
    except Exception as e:
        print(f"Error en búsqueda: {e}")
        error_message = "❌ Error en la búsqueda. Vuelve a intentar o prueba más tarde." + add_footer()
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
# MANTENER BOT ACTIVO
# ========================
def run_bot():
    print("🤖 Bot iniciado en Render - 24/7 activo")
    while True:
        try:
            bot.polling(none_stop=True, timeout=60)
        except Exception as e:
            print(f"Error: {e}")

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
