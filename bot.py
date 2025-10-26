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
      "partido": "Eredivisie: Twente vs Ajax",
      "link": "https://futbolibretv.pages.dev/#partido-26700"
    },
    {
      "partido": "Serie A: Torino vs Genoa",
      "link": "https://futbolibretv.pages.dev/#partido-26662"
    },
    {
      "partido": "2. Bundesliga: Eintracht Braunschweig vs Hannover 96",
      "link": "https://futbolibretv.pages.dev/#partido-26695"
    },
    {
      "partido": "2. Bundesliga: Magdeburg vs Preußen Münster",
      "link": "https://futbolibretv.pages.dev/#partido-26696"
    },
    {
      "partido": "2. Bundesliga: Kaiserslautern vs Nürnberg",
      "link": "https://futbolibretv.pages.dev/#partido-26694"
    },
    {
      "partido": "LaLiga SmartBank: Málaga vs FC Andorra",
      "link": "https://futbolibretv.pages.dev/#partido-26704"
    },
    {
      "partido": "LaLiga: Mallorca vs Levante",
      "link": "https://futbolibretv.pages.dev/#partido-26658"
    },
    {
      "partido": "ATP: Jannik Sinner (ITA]vs. Alexander Zverev (GER](Final]",
      "link": "https://futbolibretv.pages.dev/#partido-26715"
    },
    {
      "partido": "Eerste Divisie: Willem II vs MVV",
      "link": "https://futbolibretv.pages.dev/#partido-26713"
    },
    {
      "partido": "Eredivisie: Feyenoord vs PSV",
      "link": "https://futbolibretv.pages.dev/#partido-26701"
    },
    {
      "partido": "Premier League: Wolverhampton Wanderers vs Burnley",
      "link": "https://futbolibretv.pages.dev/#partido-26655"
    },
    {
      "partido": "Serie A: Sassuolo vs Roma",
      "link": "https://futbolibretv.pages.dev/#partido-26663"
    },
    {
      "partido": "Premier League: AFC Bournemouth vs Nottingham Forest",
      "link": "https://futbolibretv.pages.dev/#partido-26653"
    },
    {
      "partido": "Premier League: Arsenal vs Crystal Palace",
      "link": "https://futbolibretv.pages.dev/#partido-26656"
    },
    {
      "partido": "Serie A: Hellas Verona vs Cagliari",
      "link": "https://futbolibretv.pages.dev/#partido-26664"
    },
    {
      "partido": "Super Lig: Galatasaray vs Göztepe",
      "link": "https://futbolibretv.pages.dev/#partido-26708"
    },
    {
      "partido": "Premier League: Aston Villa vs Manchester City",
      "link": "https://futbolibretv.pages.dev/#partido-26654"
    },
    {
      "partido": "Ligue 1: Lille vs Metz",
      "link": "https://futbolibretv.pages.dev/#partido-26669"
    },
    {
      "partido": "Bundesliga: Bayer Leverkusen vs Freiburg",
      "link": "https://futbolibretv.pages.dev/#partido-26667"
    },
    {
      "partido": "LaLiga: Real Madrid vs Barcelona",
      "link": "https://futbolibretv.pages.dev/#partido-26659"
    },
    {
      "partido": "Primeira Liga: Famalicão vs Vitória Guimarães",
      "link": "https://futbolibretv.pages.dev/#partido-26674"
    },
    {
      "partido": "Primera División: Universidad Católica vs Universidad Chile",
      "link": "https://futbolibretv.pages.dev/#partido-26680"
    },
    {
      "partido": "Eredivisie: AZ vs Utrecht",
      "link": "https://futbolibretv.pages.dev/#partido-26702"
    },
    {
      "partido": "Liga 1: Sporting Cristal vs Los Chankas",
      "link": "https://futbolibretv.pages.dev/#partido-26649"
    },
    {
      "partido": "Ligue 1: Angers SCO vs Lorient",
      "link": "https://futbolibretv.pages.dev/#partido-26670"
    },
    {
      "partido": "Ligue 1: Rennes vs Nice",
      "link": "https://futbolibretv.pages.dev/#partido-26671"
    },
    {
      "partido": "Ligue 1: Auxerre vs Le Havre",
      "link": "https://futbolibretv.pages.dev/#partido-26672"
    },
    {
      "partido": "Premier League: Everton vs Tottenham Hotspur",
      "link": "https://futbolibretv.pages.dev/#partido-26657"
    },
    {
      "partido": "Bundesliga: Stuttgart vs Mainz 05",
      "link": "https://futbolibretv.pages.dev/#partido-26668"
    },
    {
      "partido": "Primera División: Danubio vs River Plate",
      "link": "https://futbolibretv.pages.dev/#partido-26690"
    },
    {
      "partido": "Super Lig: Kasımpaşa vs Beşiktaş",
      "link": "https://futbolibretv.pages.dev/#partido-26709"
    },
    {
      "partido": "Serie A: Fiorentina vs Bologna",
      "link": "https://futbolibretv.pages.dev/#partido-26665"
    },
    {
      "partido": "LaLiga SmartBank: Sporting Gijón vs Real Zaragoza",
      "link": "https://futbolibretv.pages.dev/#partido-26706"
    },
    {
      "partido": "LaLiga: Osasuna vs Celta de Vigo",
      "link": "https://futbolibretv.pages.dev/#partido-26660"
    },
    {
      "partido": "LaLiga SmartBank: Almería vs CD Castellon",
      "link": "https://futbolibretv.pages.dev/#partido-26705"
    },
    {
      "partido": "Serie A: Cuniburo vs Técnico Universitario",
      "link": "https://futbolibretv.pages.dev/#partido-26685"
    },
    {
      "partido": "Primeira Liga: Tondela vs Sporting CP",
      "link": "https://futbolibretv.pages.dev/#partido-26675"
    },
    {
      "partido": "Liga 1: UTC Cajamarca vs Alianza Universidad",
      "link": "https://futbolibretv.pages.dev/#partido-26650"
    },
    {
      "partido": "Eredivisie: Go Ahead Eagles vs Excelsior",
      "link": "https://futbolibretv.pages.dev/#partido-26703"
    },
    {
      "partido": "Copa de la División Profesional: Gualberto Villarroel SJ vs Oriente Petrolero",
      "link": "https://futbolibretv.pages.dev/#partido-26710"
    },
    {
      "partido": "Brasileirão: Grêmio vs Juventude",
      "link": "https://futbolibretv.pages.dev/#partido-26676"
    },
    {
      "partido": "Primera División: Cobresal vs Unión Española",
      "link": "https://futbolibretv.pages.dev/#partido-26681"
    },
    {
      "partido": "Primera División: Liverpool vs Progreso",
      "link": "https://futbolibretv.pages.dev/#partido-26691"
    },
    {
      "partido": "Brasileirão: Botafogo vs Santos",
      "link": "https://futbolibretv.pages.dev/#partido-26677"
    },
    {
      "partido": "Serie A: Lazio vs Juventus",
      "link": "https://futbolibretv.pages.dev/#partido-26666"
    },
    {
      "partido": "Ligue 1: Olympique Lyonnais vs Strasbourg",
      "link": "https://futbolibretv.pages.dev/#partido-26673"
    },
    {
      "partido": "LaLiga SmartBank: Deportivo La Coruña vs Real Valladolid",
      "link": "https://futbolibretv.pages.dev/#partido-26707"
    },
    {
      "partido": "Amistoso Internacional Femenino: EE. UU. vs Portugal",
      "link": "https://futbolibretv.pages.dev/#partido-26714"
    },
    {
      "partido": "LaLiga: Rayo Vallecano vs Deportivo Alavés",
      "link": "https://futbolibretv.pages.dev/#partido-26661"
    },
    {
      "partido": "Primera División: Olimpia vs Guaraní",
      "link": "https://futbolibretv.pages.dev/#partido-26688"
    },
    {
      "partido": "Liga 1: ADT vs Universitario",
      "link": "https://futbolibretv.pages.dev/#partido-26651"
    },
    {
      "partido": "Serie A: El Nacional vs Macará",
      "link": "https://futbolibretv.pages.dev/#partido-26686"
    },
    {
      "partido": "Primera División: O'Higgins vs Coquimbo Unido",
      "link": "https://futbolibretv.pages.dev/#partido-26683"
    },
    {
      "partido": "Copa de la División Profesional: Wilstermann vs The Strongest",
      "link": "https://futbolibretv.pages.dev/#partido-26711"
    },
    {
      "partido": "Primera División: Unión La Calera vs Ñublense",
      "link": "https://futbolibretv.pages.dev/#partido-26682"
    },
    {
      "partido": "Primera División: Wanderers vs Nacional",
      "link": "https://futbolibretv.pages.dev/#partido-26692"
    },
    {
      "partido": "Brasileirão: RB Bragantino vs Vasco da Gama",
      "link": "https://futbolibretv.pages.dev/#partido-26678"
    },
    {
      "partido": "Liga MX: Santos Laguna vs Querétaro",
      "link": "https://futbolibretv.pages.dev/#partido-26697"
    },
    {
      "partido": "Liga 1: Melgar vs Sport Huancayo",
      "link": "https://futbolibretv.pages.dev/#partido-26652"
    },
    {
      "partido": "Primera División: Deportivo Recoleta vs Libertad",
      "link": "https://futbolibretv.pages.dev/#partido-26689"
    },
    {
      "partido": "Serie A: Emelec vs Delfin",
      "link": "https://futbolibretv.pages.dev/#partido-26687"
    },
    {
      "partido": "Brasileirão: Palmeiras vs Cruzeiro",
      "link": "https://futbolibretv.pages.dev/#partido-26679"
    },
    {
      "partido": "Primera A: Atlético Nacional vs Medellín",
      "link": "https://futbolibretv.pages.dev/#partido-26684"
    },
    {
      "partido": "Copa de la División Profesional: Nacional Potosí vs Real Oruro",
      "link": "https://futbolibretv.pages.dev/#partido-26712"
    },
    {
      "partido": "Primera División: Miramar Misiones vs Boston River",
      "link": "https://futbolibretv.pages.dev/#partido-26693"
    },
    {
      "partido": "Liga MX: Toluca vs Pachuca",
      "link": "https://futbolibretv.pages.dev/#partido-26699"
    },
    {
      "partido": "Liga MX: Atlético San Luis vs Necaxa",
      "link": "https://futbolibretv.pages.dev/#partido-26698"
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
