import telebot
from flask import Flask
import threading
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import os
import re
import time
import unicodedata   # <-- agregado

TOKEN = os.environ.get('BOT_TOKEN')
if not TOKEN:
    raise ValueError("❌ BOT_TOKEN no encontrado en variables de entorno")

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# ========================
# FUNCION QUITAR TILDES
# ========================
def quitar_tildes(texto):
    return ''.join(
        c for c in unicodedata.normalize('NFD', texto)
        if unicodedata.category(c) != 'Mn'
    )

# ========================
# PARTIDOS DIRECTAMENTE EN EL CÓDIGO.
# ========================
PARTIDOS_JSON = {
  "partidos": [
    {
      "partido": "2. Bundesliga: Nürnberg vs Eintracht Braunschweig",
      "link": "https://futbolibretv.pages.dev/#partido-26993"
    },
    {
      "partido": "FA Cup: Chelmsford City vs Braintree Town",
      "link": "https://futbolibretv.pages.dev/#partido-26989"
    },
    {
      "partido": "2. Bundesliga: Hertha BSC vs Dynamo Dresden",
      "link": "https://futbolibretv.pages.dev/#partido-26994"
    },
    {
      "partido": "Women's Super League: Manchester City vs West Ham United",
      "link": "https://futbolibretv.pages.dev/#partido-26991"
    },
    {
      "partido": "Women's Super League: Chelsea FC vs London City Lionesses",
      "link": "https://futbolibretv.pages.dev/#partido-26992"
    },
    {
      "partido": "2. Bundesliga: Karlsruher SC vs Schalke 04",
      "link": "https://futbolibretv.pages.dev/#partido-26995"
    },
    {
      "partido": "Championship: Leicester City vs Blackburn Rovers",
      "link": "https://futbolibretv.pages.dev/#partido-26987"
    },
    {
      "partido": "Primera División: Progreso vs Torque",
      "link": "https://futbolibretv.pages.dev/#partido-26984"
    },
    {
      "partido": "LaLiga: Villarreal vs Rayo Vallecano",
      "link": "https://futbolibretv.pages.dev/#partido-26949"
    },
    {
      "partido": "Serie A: Udinese vs Atalanta",
      "link": "https://futbolibretv.pages.dev/#partido-26953"
    },
    {
      "partido": "Bundesliga: RB Leipzig vs Stuttgart",
      "link": "https://futbolibretv.pages.dev/#partido-26958"
    },
    {
      "partido": "Bundesliga: Mainz 05 vs Werder Bremen",
      "link": "https://futbolibretv.pages.dev/#partido-26956"
    },
    {
      "partido": "Bundesliga: Heidenheim vs Eintracht Frankfurt",
      "link": "https://futbolibretv.pages.dev/#partido-26959"
    },
    {
      "partido": "Bundesliga: Union Berlin vs Freiburg",
      "link": "https://futbolibretv.pages.dev/#partido-26957"
    },
    {
      "partido": "Bundesliga: St. Pauli vs Borussia M'gladbach",
      "link": "https://futbolibretv.pages.dev/#partido-26960"
    },
    {
      "partido": "Premier League: Fulham vs Wolverhampton Wanderers",
      "link": "https://futbolibretv.pages.dev/#partido-26942"
    },
    {
      "partido": "Premier League: Brighton & Hove Albion vs Leeds United",
      "link": "https://futbolibretv.pages.dev/#partido-26944"
    },
    {
      "partido": "Premier League: Burnley vs Arsenal",
      "link": "https://futbolibretv.pages.dev/#partido-26946"
    },
    {
      "partido": "Championship: Queens Park Rangers vs Ipswich Town",
      "link": "https://futbolibretv.pages.dev/#partido-26988"
    },
    {
      "partido": "Premier League: Crystal Palace vs Brentford",
      "link": "https://futbolibretv.pages.dev/#partido-26943"
    },
    {
      "partido": "Premier League: Nottingham Forest vs Manchester United",
      "link": "https://futbolibretv.pages.dev/#partido-26945"
    },
    {
      "partido": "LaLiga SmartBank: Cultural Leonesa vs Mirandés",
      "link": "https://futbolibretv.pages.dev/#partido-27006"
    },
    {
      "partido": "LaLiga: Atlético Madrid vs Sevilla",
      "link": "https://futbolibretv.pages.dev/#partido-26950"
    },
    {
      "partido": "Primeira Liga: Nacional vs Famalicão",
      "link": "https://futbolibretv.pages.dev/#partido-26965"
    },
    {
      "partido": "Eredivisie: Ajax vs Heerenveen",
      "link": "https://futbolibretv.pages.dev/#partido-27002"
    },
    {
      "partido": "Ligue 1: PSG vs Nice",
      "link": "https://futbolibretv.pages.dev/#partido-26962"
    },
    {
      "partido": "Primera Nacional: Atlanta vs Deportivo Morón",
      "link": "https://futbolibretv.pages.dev/#partido-27013"
    },
    {
      "partido": "Super Lig: Galatasaray vs Trabzonspor",
      "link": "https://futbolibretv.pages.dev/#partido-27010"
    },
    {
      "partido": "Serie A: Napoli vs Como",
      "link": "https://futbolibretv.pages.dev/#partido-26954"
    },
    {
      "partido": "LaLiga: Real Sociedad vs Athletic Club",
      "link": "https://futbolibretv.pages.dev/#partido-26951"
    },
    {
      "partido": "Bundesliga: Bayern München vs Bayer Leverkusen",
      "link": "https://futbolibretv.pages.dev/#partido-26961"
    },
    {
      "partido": "LaLiga SmartBank: Albacete vs Huesca",
      "link": "https://futbolibretv.pages.dev/#partido-27007"
    },
    {
      "partido": "LaLiga SmartBank: Leganés vs Burgos",
      "link": "https://futbolibretv.pages.dev/#partido-27008"
    },
    {
      "partido": "Premier League: Tottenham Hotspur vs Chelsea",
      "link": "https://futbolibretv.pages.dev/#partido-26947"
    },
    {
      "partido": "FA Cup: Brackley Town vs Notts County",
      "link": "https://futbolibretv.pages.dev/#partido-26990"
    },
    {
      "partido": "Eredivisie: NAC Breda vs Go Ahead Eagles",
      "link": "https://futbolibretv.pages.dev/#partido-27003"
    },
    {
      "partido": "Liga Profesional: Aldosivi vs Independiente Rivadavia",
      "link": "https://futbolibretv.pages.dev/#partido-26967"
    },
    {
      "partido": "Liga 1: Los Chankas vs Ayacucho",
      "link": "https://futbolibretv.pages.dev/#partido-26939"
    },
    {
      "partido": "Ligue 1: Monaco vs Paris",
      "link": "https://futbolibretv.pages.dev/#partido-26963"
    },
    {
      "partido": "Primera División: Real Oruro vs Gualberto Villarroel SJ",
      "link": "https://futbolibretv.pages.dev/#partido-26971"
    },
    {
      "partido": "Brasileirão: Cruzeiro vs Vitória",
      "link": "https://futbolibretv.pages.dev/#partido-26972"
    },
    {
      "partido": "Eredivisie: Feyenoord vs Volendam",
      "link": "https://futbolibretv.pages.dev/#partido-27004"
    },
    {
      "partido": "Liga Profesional: Barracas Central vs Argentinos Juniors",
      "link": "https://futbolibretv.pages.dev/#partido-26968"
    },
    {
      "partido": "Brasileirão: Santos vs Fortaleza",
      "link": "https://futbolibretv.pages.dev/#partido-26973"
    },
    {
      "partido": "Serie A: Técnico Universitario vs Mushuc Runa",
      "link": "https://futbolibretv.pages.dev/#partido-26980"
    },
    {
      "partido": "2. Bundesliga: Darmstadt 98 vs Arminia Bielefeld",
      "link": "https://futbolibretv.pages.dev/#partido-26996"
    },
    {
      "partido": "Primera División: Liverpool vs Juventud",
      "link": "https://futbolibretv.pages.dev/#partido-26985"
    },
    {
      "partido": "Serie A: Cremonese vs Juventus",
      "link": "https://futbolibretv.pages.dev/#partido-26955"
    },
    {
      "partido": "Eredivisie: Telstar vs Excelsior",
      "link": "https://futbolibretv.pages.dev/#partido-27005"
    },
    {
      "partido": "Liga Profesional: Vélez Sarsfield vs Talleres Córdoba",
      "link": "https://futbolibretv.pages.dev/#partido-26969"
    },
    {
      "partido": "Premier League: Liverpool vs Aston Villa",
      "link": "https://futbolibretv.pages.dev/#partido-26948"
    },
    {
      "partido": "LaLiga: Real Madrid vs Valencia",
      "link": "https://futbolibretv.pages.dev/#partido-26952"
    },
    {
      "partido": "LaLiga SmartBank: Almería vs Eibar",
      "link": "https://futbolibretv.pages.dev/#partido-27009"
    },
    {
      "partido": "Ligue 1: Auxerre vs Olympique Marseille",
      "link": "https://futbolibretv.pages.dev/#partido-26964"
    },
    {
      "partido": "Liga 1: Comerciantes Unidos vs Sporting Cristal",
      "link": "https://futbolibretv.pages.dev/#partido-26940"
    },
    {
      "partido": "Primeira Liga: Vitória Guimarães vs Benfica",
      "link": "https://futbolibretv.pages.dev/#partido-26966"
    },
    {
      "partido": "Primera División: Nacional Asunción vs Sportivo Trinidense",
      "link": "https://futbolibretv.pages.dev/#partido-26982"
    },
    {
      "partido": "Primera División: Ñublense vs Colo-Colo",
      "link": "https://futbolibretv.pages.dev/#partido-26976"
    },
    {
      "partido": "Brasileirão: Mirassol vs Botafogo",
      "link": "https://futbolibretv.pages.dev/#partido-26974"
    },
    {
      "partido": "Primera A: Alianza vs Boyacá Chicó",
      "link": "https://futbolibretv.pages.dev/#partido-26977"
    },
    {
      "partido": "Serie A: Aucas vs El Nacional",
      "link": "https://futbolibretv.pages.dev/#partido-26981"
    },
    {
      "partido": "Liga MX Femenil: Cruz Azul vs Tigres UANL",
      "link": "https://futbolibretv.pages.dev/#partido-26998"
    },
    {
      "partido": "Primera División: Cerro vs Nacional",
      "link": "https://futbolibretv.pages.dev/#partido-26986"
    },
    {
      "partido": "Liga MX Femenil: León vs Pumas UNAM",
      "link": "https://futbolibretv.pages.dev/#partido-26999"
    },
    {
      "partido": "Liga MX Femenil: Atlético San Luis vs Santos Laguna",
      "link": "https://futbolibretv.pages.dev/#partido-27000"
    },
    {
      "partido": "Liga 1: Deportivo Garcilaso vs ADT",
      "link": "https://futbolibretv.pages.dev/#partido-26941"
    },
    {
      "partido": "Liga Profesional: Independiente vs Atlético Tucumán",
      "link": "https://futbolibretv.pages.dev/#partido-26970"
    },
    {
      "partido": "Primera División: Libertad vs Olimpia",
      "link": "https://futbolibretv.pages.dev/#partido-26983"
    },
    {
      "partido": "Primera A: Deportivo Pereira vs Medellín",
      "link": "https://futbolibretv.pages.dev/#partido-26978"
    },
    {
      "partido": "Major League Soccer: Nashville SC vs Inter Miami",
      "link": "https://futbolibretv.pages.dev/#partido-27011"
    },
    {
      "partido": "USL Super League: Fort Lauderdale United vs Brooklyn",
      "link": "https://futbolibretv.pages.dev/#partido-27012"
    },
    {
      "partido": "Brasileirão: Flamengo vs Sport Recife",
      "link": "https://futbolibretv.pages.dev/#partido-26975"
    },
    {
      "partido": "Liga MX Femenil: Mazatlán vs América",
      "link": "https://futbolibretv.pages.dev/#partido-27001"
    },
    {
      "partido": "Liga de Expansión MX: Tlaxcala vs Atlético Morelia",
      "link": "https://futbolibretv.pages.dev/#partido-26997"
    },
    {
      "partido": "Primera A: Once Caldas vs Deportivo Pasto",
      "link": "https://futbolibretv.pages.dev/#partido-26979"
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
            max_chars = 3500
            for partido in partidos:
                partido_limpio = formato_limpio(partido['partido'])
                texto = f"*{contador}. {partido_limpio}*\n🔗 {partido['link']}\n\n"
                if len(bloque) + len(texto) > max_chars:
                    bot.reply_to(message, bloque, parse_mode='Markdown')
                    bloque = ""
                bloque += texto
                contador += 1

            if bloque:
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
# BUSCADOR SUPER SIMPLE IGNORA TILDES
# ========================
def search_matches(message, search_term):
    try:
        partidos = PARTIDOS_JSON["partidos"]
        matches = []

        search_clean = quitar_tildes(search_term.strip().lower())
        print(f"🔍 Búsqueda simple: '{search_term}'")

        for partido in partidos:
            partido_text = quitar_tildes(partido['partido'].lower())
            
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
    print("🤖 Bot iniciado en Render 24/7 activo")
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
    return "✅ Bot activo en Render 24/7"

if __name__ == "__main__":
    bot_thread = threading.Thread(target=run_bot)
    bot_thread.daemon = True
    bot_thread.start()
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
