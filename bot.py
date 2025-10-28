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
      "partido": "Copa del Rey de Arabia Saudita: Al Akhdoud vs Al Hilal",
      "link": "https://futbolibretv.pages.dev/#partido-26813"
    },
    {
      "partido": "Copa Mundial Femenina Sub-17 de la FIFA: Estados Unidos vs Países Bajos",
      "link": "https://futbolibretv.pages.dev/#partido-26815"
    },
    {
      "partido": "Copa Mundial Femenina Sub-17 de la FIFA: Brasil vs China PR",
      "link": "https://futbolibretv.pages.dev/#partido-26816"
    },
    {
      "partido": "Serie A: Lecce vs Napoli",
      "link": "https://futbolibretv.pages.dev/#partido-26780"
    },
    {
      "partido": "DFB Pokal: Eintracht Frankfurt vs Borussia Dortmund",
      "link": "https://futbolibretv.pages.dev/#partido-26785"
    },
    {
      "partido": "DFB Pokal: Heidenheim vs Hamburger SV",
      "link": "https://futbolibretv.pages.dev/#partido-26786"
    },
    {
      "partido": "Copa KNVB: Gemert vs Fortuna Sittard",
      "link": "https://futbolibretv.pages.dev/#partido-26811"
    },
    {
      "partido": "Copa del Rey: Constància vs Girona",
      "link": "https://futbolibretv.pages.dev/#partido-26789"
    },
    {
      "partido": "Copa del Rey de Arabia Saudita: Al Nassr vs Al Ittihad",
      "link": "https://futbolibretv.pages.dev/#partido-26814"
    },
    {
      "partido": "UEFA Nations League Femenina: Suecia vs España",
      "link": "https://futbolibretv.pages.dev/#partido-26801"
    },
    {
      "partido": "Copa del Rey: Ourense CF vs Real Oviedo",
      "link": "https://futbolibretv.pages.dev/#partido-26790"
    },
    {
      "partido": "Amistoso Internacional Femenino: Inglaterra vs Australia",
      "link": "https://futbolibretv.pages.dev/#partido-26798"
    },
    {
      "partido": "Copa del Rey: Maracena vs Valencia",
      "link": "https://futbolibretv.pages.dev/#partido-26792"
    },
    {
      "partido": "Copa Mundial Femenina Sub-17 de la FIFA: Italia vs Nigeria",
      "link": "https://futbolibretv.pages.dev/#partido-26818"
    },
    {
      "partido": "Copa KNVB: Helmond Sport vs PEC Zwolle",
      "link": "https://futbolibretv.pages.dev/#partido-26812"
    },
    {
      "partido": "Copa del Rey: Inter de Valdemoro vs Getafe",
      "link": "https://futbolibretv.pages.dev/#partido-26791"
    },
    {
      "partido": "Copa Mundial Femenina Sub-17 de la FIFA: Corea del Norte vs Marruecos",
      "link": "https://futbolibretv.pages.dev/#partido-26817"
    },
    {
      "partido": "UEFA Nations League Femenina: Bélgica vs Republic of Ireland",
      "link": "https://futbolibretv.pages.dev/#partido-26802"
    },
    {
      "partido": "EFL Cup: Wycombe Wanderers vs Fulham",
      "link": "https://futbolibretv.pages.dev/#partido-26783"
    },
    {
      "partido": "Serie A: Atalanta vs Milan",
      "link": "https://futbolibretv.pages.dev/#partido-26781"
    },
    {
      "partido": "DFB Pokal: Borussia M'gladbach vs Karlsruher SC",
      "link": "https://futbolibretv.pages.dev/#partido-26787"
    },
    {
      "partido": "EFL Cup: Grimsby Town vs Brentford",
      "link": "https://futbolibretv.pages.dev/#partido-26782"
    },
    {
      "partido": "DFB Pokal: Energie Cottbus vs RB Leipzig",
      "link": "https://futbolibretv.pages.dev/#partido-26788"
    },
    {
      "partido": "Copa del Rey: Negreira vs Real Sociedad",
      "link": "https://futbolibretv.pages.dev/#partido-26793"
    },
    {
      "partido": "EFL Cup: Wrexham vs Cardiff City",
      "link": "https://futbolibretv.pages.dev/#partido-26784"
    },
    {
      "partido": "Copa del Rey: Toledo vs Sevilla",
      "link": "https://futbolibretv.pages.dev/#partido-26794"
    },
    {
      "partido": "UEFA Nations League Femenina: Francia vs Alemania",
      "link": "https://futbolibretv.pages.dev/#partido-26803"
    },
    {
      "partido": "Primera A: Rionegro Águilas vs Envigado",
      "link": "https://futbolibretv.pages.dev/#partido-26795"
    },
    {
      "partido": "CONMEBOL Nations League Femenina: Uruguay vs Argentina",
      "link": "https://futbolibretv.pages.dev/#partido-26805"
    },
    {
      "partido": "Amistoso Internacional Femenino: Perú vs Panamá",
      "link": "https://futbolibretv.pages.dev/#partido-26799"
    },
    {
      "partido": "CONMEBOL Nations League Femenina: Chile vs Bolivia",
      "link": "https://futbolibretv.pages.dev/#partido-26804"
    },
    {
      "partido": "Copa de la División Profesional: Aurora vs Guabirá",
      "link": "https://futbolibretv.pages.dev/#partido-26809"
    },
    {
      "partido": "Major League Soccer: Charlotte vs New York City",
      "link": "https://futbolibretv.pages.dev/#partido-26808"
    },
    {
      "partido": "CONMEBOL Nations League Femenina: Ecuador vs Colombia",
      "link": "https://futbolibretv.pages.dev/#partido-26806"
    },
    {
      "partido": "CONMEBOL Nations League Femenina: Paraguay vs Venezuela",
      "link": "https://futbolibretv.pages.dev/#partido-26807"
    },
    {
      "partido": "Primera A: Deportivo Cali vs Alianza",
      "link": "https://futbolibretv.pages.dev/#partido-26796"
    },
    {
      "partido": "Copa de la División Profesional: Blooming vs Always Ready",
      "link": "https://futbolibretv.pages.dev/#partido-26810"
    },
    {
      "partido": "Copa Sudamericana: Atlético Mineiro vs Independiente del Valle",
      "link": "https://futbolibretv.pages.dev/#partido-26797"
    },
    {
      "partido": "Copa Centroamericana: Motagua vs Cartaginés",
      "link": "https://futbolibretv.pages.dev/#partido-26800"
    }
  ]
}

def formato_limpio(partido_completo):
    match = re.search(r':\s*(.+)', partido_completo)
    if match:
        return match.group(1).strip()
    return partido_completo

def add_footer():
    return "\n\nEscribe el nombre del partido que quieres ver, o vuelve al /menu"

def add_search_footer():
    return "\n\n🤔 *¿Quieres hacer algo más?*\nBuscar otro partido o /menu"

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
    bot.reply_to(message, welcome_text, parse_mode='Markdown')
    print(f"✅ /{message.text[1:]} enviado a {user_name}")

@bot.message_handler(commands=['partidos'])
def send_matches(message):
    try:
        partidos = PARTIDOS_JSON["partidos"]

        if partidos:
            bloque = ""
            contador = 1
            max_chars = 3500  # Telegram tiene límite ~4096, dejar margen
            for partido in partidos:
                partido_limpio = formato_limpio(partido['partido'])
                texto = f"*{contador}. {partido_limpio}*\n🔗 {partido['link']}\n\n"
                if len(bloque) + len(texto) > max_chars:
                    bot.reply_to(message, bloque, parse_mode='Markdown')
                    bloque = ""
                bloque += texto
                contador += 1

            if bloque:  # Enviar el bloque final
                bot.reply_to(message, bloque, parse_mode='Markdown')

            footer = add_footer()
            bot.reply_to(message, footer, parse_mode='Markdown')
            print("✅ /partidos enviado en bloques")

        else:
            bot.reply_to(message, "❌ *No hay partidos disponibles en este momento.*\n\nIntenta más tarde o usa /ayuda para soporte.", parse_mode='Markdown')

    except Exception as e:
        print(f"Error en /partidos: {e}")
        bot.reply_to(message, "❌ Error al cargar los partidos. Intenta más tarde." + add_footer(), parse_mode='Markdown')


@bot.message_handler(commands=['ayuda'])
def send_help(message):
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
    bot.send_message(message.chat.id, full_message, parse_mode='Markdown', reply_markup=keyboard)
    print("✅ /ayuda enviado con inline keyboard")

@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    if call.data == "help_vpn":
        response = """📱 *SOLUCIÓN CELULAR - VPN*

¿Problema? ❌ Links bloqueados o no cargan

Solución: Usar VPN para desbloquear

1. Descarga una app VPN gratis:
   📲 Turbo VPN (Android/iOS)
   📲 Windscribe 
   📲 Hotspot Shield
   📲 Cloudflare WARP (1.1.1.1)

2. Pasos a seguir:
   • Abre la app VPN
   • Toca "Conectar" o "Connect"
   • Elige cualquier país
   • Listo ✅ Ahora prueba el link

Nota: La VPN evita que tu compañía de internet bloquee los partidos.

💡 Esta solución es 100% efectiva. Si aún así no te funciona, puede deberse a tu conexión a internet."""

    elif call.data == "help_dns":
        response = """💻 *SOLUCIÓN PC/TV - DNS*

¿Problema? ❌ Pantalla negra o "stream no disponible"

Solución: Cambiar DNS para saltar restricciones

DNS Recomendados:
🔹 Google: 8.8.8.8 y 8.8.4.4
🔹 Cloudflare: 1.1.1.1 y 1.0.0.1

¿Cómo cambiar DNS?

📱 En Android:
   Ajustes → Redes → DNS privado → Ingresa: 1.1.1.1

💻 En Windows:
   Panel Control → Red → Adaptador → Propiedades → IPv4 → Usar DNS

📺 En Smart TV:
   Configuración → Red → DNS manual

🔄 Reinicia el navegador después de cambiar DNS

💡 Esta solución es 100% efectiva. Si aún así no te funciona, puede deberse a tu conexión a internet."""

    elif call.data == "help_incognito":
        response = """🌐 *MODO INCÓGNITO*

¿Problema? ❌ Página carga mal o da error

Solución: Probar en modo incógnito

Pasos rápidos:

📱 En Chrome/Edge:
   • Toca los 3 puntos ⋮
   • "Nueva pestaña incógnito"
   • O usa: Ctrl+Shift+N (PC)

📱 En Firefox:
   • Toca los 3 puntos ⋮  
   • "Nueva pestaña privada"
   • O usa: Ctrl+Shift+P (PC)

📱 En Safari:
   • Toca los cuadrados []
   • "Privado"
   • O usa: Cmd+Shift+N (Mac)

¿Por qué funciona?
El modo incógnito evita problemas de cache, cookies y extensiones que pueden bloquear el stream.

💡 Esta solución es 100% efectiva. Si aún así no te funciona, puede deberse a tu conexión a internet."""

    full_response = response + add_footer()
    bot.send_message(call.message.chat.id, full_response, parse_mode='Markdown')
    bot.answer_callback_query(call.id)

# ========================
# BUSCADOR SUPER SIMPLE - SIN COMPLICACIONES
# ========================
def search_matches(message, search_term):
    try:
        partidos = PARTIDOS_JSON["partidos"]
        matches = []

        search_clean = search_term.strip().lower()
        print(f"🔍 Búsqueda simple: '{search_term}'")

        for partido in partidos:
            partido_text = partido['partido'].lower()
            
            # BUSQUEDA SIMPLE: Si la palabra aparece en cualquier parte del partido
            if search_clean in partido_text:
                matches.append(partido)

        if matches:
            result_text = f"🔍 *Resultados para '{search_term}'*:\n\n"
            for i, match in enumerate(matches, 1):
                result_text += f"*{i}. {match['partido']}*\n"
                result_text += f"🔗 {match['link']}\n\n"
            result_text += f"_📊 Encontré {len(matches)} partido(s)_"
            full_message = result_text + add_search_footer()
            bot.reply_to(message, full_message, parse_mode='Markdown')
            print(f"🔍 Búsqueda exitosa: '{search_term}' → {len(matches)} resultados")
        else:
            result_text = f"❌ *No encontré '{search_term}' en la agenda de hoy*\n\n"
            result_text += "💡 *Sugerencias:*\n• Escribe el nombre del equipo o liga\n• Ejemplos: 'premier', 'sevilla', 'champions'\n• Usa /partidos para ver toda la agenda"
            full_message = result_text + add_search_footer()
            bot.reply_to(message, full_message, parse_mode='Markdown')
            print(f"🔍 Búsqueda sin resultados: '{search_term}'")

    except Exception as e:
        print(f"❌ ERROR en búsqueda: {e}")
        error_message = "❌ Error temporal. Intenta de nuevo." + add_footer()
        bot.reply_to(message, error_message, parse_mode='Markdown')

@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    text = message.text.strip().lower()
    if text in ["/start", "/partidos", "/ayuda", "/menu"]:
        return
    search_matches(message, text)

def run_bot():
    print("🤖 Bot iniciado en Render - 24/7 activo")
    while True:
        try:
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

if __name__ == "__main__":
    bot_thread = threading.Thread(target=run_bot)
    bot_thread.daemon = True
    bot_thread.start()
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
