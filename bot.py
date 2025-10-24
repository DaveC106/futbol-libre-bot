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

def formato_limpio(partido_completo):
    match = re.search(r':\s*(.+)', partido_completo)
    if match:
        return match.group(1).strip()
    return partido_completo

def add_footer():
    return "\n\n🤔 *¿Quieres hacer algo más?*\nVolver al menú principal /menu"

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
            partidos_text = "⚽️ *PARTIDOS DE HOY* ⚽️\n\n"
            for i, partido in enumerate(partidos, 1):
                partido_limpio = formato_limpio(partido['partido'])
                partidos_text += f"*{i}. {partido_limpio}*\n"
                partidos_text += f"🔗 {partido['link']}\n\n"
            partidos_text += "\n\n**Para buscar un partido en específico, escribe directamente el nombre de tu equipo o el de su liga.** ⭐"
        else:
            partidos_text = "❌ *No hay partidos disponibles en este momento.*\n\nIntenta más tarde o usa /ayuda para soporte."

        full_message = partidos_text + add_footer()
        bot.reply_to(message, full_message, parse_mode='Markdown')
        print("✅ /partidos enviado (formato limpio)")

    except Exception as e:
        print(f"Error en /partidos: {e}")
        error_message = "❌ Error al cargar los partidos. Intenta más tarde." + add_footer()
        bot.reply_to(message, error_message, parse_mode='Markdown')

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
        response = """📱 *SOLUCIÓN CELULAR - VPN*"""
    elif call.data == "help_dns":
        response = """💻 *SOLUCIÓN PC/TV - DNS*"""
    elif call.data == "help_incognito":
        response = """🌐 *MODO INCÓGNITO*"""

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
