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
      "partido": "2. Bundesliga: Holstein Kiel vs Bochum",
      "link": "https://futbolibretv.pages.dev/#partido-26611"
    },
    {
      "partido": "2. Bundesliga: Arminia Bielefeld vs Elversberg",
      "link": "https://futbolibretv.pages.dev/#partido-26609"
    },
    {
      "partido": "2. Bundesliga: Dynamo Dresden vs Paderborn",
      "link": "https://futbolibretv.pages.dev/#partido-26610"
    },
    {
      "partido": "LaLiga SmartBank: Cultural Leonesa vs Ceuta",
      "link": "https://futbolibretv.pages.dev/#partido-26616"
    },
    {
      "partido": "LaLiga: Girona vs Real Oviedo",
      "link": "https://futbolibretv.pages.dev/#partido-26567"
    },
    {
      "partido": "Serie A: Parma vs Como",
      "link": "https://futbolibretv.pages.dev/#partido-26571"
    },
    {
      "partido": "Serie A: Udinese vs Lecce",
      "link": "https://futbolibretv.pages.dev/#partido-26572"
    },
    {
      "partido": "Copa Mundial Femenina Sub-17 de la FIFA: Colombia vs Corea del Sur",
      "link": "https://futbolibretv.pages.dev/#partido-26613"
    },
    {
      "partido": "Bundesliga: Hoffenheim vs Heidenheim",
      "link": "https://futbolibretv.pages.dev/#partido-26576"
    },
    {
      "partido": "Bundesliga: Eintracht Frankfurt vs St. Pauli",
      "link": "https://futbolibretv.pages.dev/#partido-26579"
    },
    {
      "partido": "Bundesliga: Borussia M'gladbach vs Bayern München",
      "link": "https://futbolibretv.pages.dev/#partido-26577"
    },
    {
      "partido": "Bundesliga: Hamburger SV vs Wolfsburg",
      "link": "https://futbolibretv.pages.dev/#partido-26575"
    },
    {
      "partido": "Bundesliga: Augsburg vs RB Leipzig",
      "link": "https://futbolibretv.pages.dev/#partido-26578"
    },
    {
      "partido": "Championship: Blackburn Rovers vs Southampton",
      "link": "https://futbolibretv.pages.dev/#partido-26608"
    },
    {
      "partido": "Premier League: Newcastle United vs Fulham",
      "link": "https://futbolibretv.pages.dev/#partido-26563"
    },
    {
      "partido": "Premier League: Chelsea vs Sunderland",
      "link": "https://futbolibretv.pages.dev/#partido-26564"
    },
    {
      "partido": "LaLiga SmartBank: Eibar vs Leganés",
      "link": "https://futbolibretv.pages.dev/#partido-26617"
    },
    {
      "partido": "LaLiga SmartBank: Albacete vs Córdoba",
      "link": "https://futbolibretv.pages.dev/#partido-26618"
    },
    {
      "partido": "LaLiga: Espanyol vs Elche",
      "link": "https://futbolibretv.pages.dev/#partido-26568"
    },
    {
      "partido": "Eredivisie: Fortuna Sittard vs Groningen",
      "link": "https://futbolibretv.pages.dev/#partido-26639"
    },
    {
      "partido": "Eerste Divisie: ADO Den Haag vs Den Bosch",
      "link": "https://futbolibretv.pages.dev/#partido-26643"
    },
    {
      "partido": "Pro League: Al Quadisiya vs Al Akhdoud",
      "link": "https://futbolibretv.pages.dev/#partido-26646"
    },
    {
      "partido": "Pro League: Al Shabab vs Damac",
      "link": "https://futbolibretv.pages.dev/#partido-26644"
    },
    {
      "partido": "Ligue 1: Brest vs PSG",
      "link": "https://futbolibretv.pages.dev/#partido-26581"
    },
    {
      "partido": "Serie A: Napoli vs Internazionale",
      "link": "https://futbolibretv.pages.dev/#partido-26573"
    },
    {
      "partido": "Bundesliga: Borussia Dortmund vs Köln",
      "link": "https://futbolibretv.pages.dev/#partido-26580"
    },
    {
      "partido": "Amistoso Internacional Femenino: Inglaterra vs Brasil",
      "link": "https://futbolibretv.pages.dev/#partido-26614"
    },
    {
      "partido": "LaLiga SmartBank: Burgos vs Real Sociedad II",
      "link": "https://futbolibretv.pages.dev/#partido-26619"
    },
    {
      "partido": "Premier League: Manchester United vs Brighton & Hove Albion",
      "link": "https://futbolibretv.pages.dev/#partido-26565"
    },
    {
      "partido": "LaLiga: Athletic Club vs Getafe",
      "link": "https://futbolibretv.pages.dev/#partido-26569"
    },
    {
      "partido": "Primera División: Juventud vs Plaza Colonia",
      "link": "https://futbolibretv.pages.dev/#partido-26605"
    },
    {
      "partido": "LaLiga SmartBank: Granada vs Cádiz",
      "link": "https://futbolibretv.pages.dev/#partido-26620"
    },
    {
      "partido": "Eredivisie: Sparta Rotterdam vs Telstar",
      "link": "https://futbolibretv.pages.dev/#partido-26640"
    },
    {
      "partido": "Super Lig: Trabzonspor vs Eyüpspor",
      "link": "https://futbolibretv.pages.dev/#partido-26622"
    },
    {
      "partido": "Primeira Liga: Santa Clara vs AVS",
      "link": "https://futbolibretv.pages.dev/#partido-26584"
    },
    {
      "partido": "Ligue 1: Monaco vs Toulouse",
      "link": "https://futbolibretv.pages.dev/#partido-26582"
    },
    {
      "partido": "Eredivisie: Volendam vs Heracles",
      "link": "https://futbolibretv.pages.dev/#partido-26641"
    },
    {
      "partido": "Pro League: Al Hazm vs Al Nassr",
      "link": "https://futbolibretv.pages.dev/#partido-26645"
    },
    {
      "partido": "Primera División: La Serena vs Audax Italiano",
      "link": "https://futbolibretv.pages.dev/#partido-26593"
    },
    {
      "partido": "Liga 1: Ayacucho vs Deportivo Garcilaso",
      "link": "https://futbolibretv.pages.dev/#partido-26560"
    },
    {
      "partido": "2. Bundesliga: Hertha BSC vs Fortuna Düsseldorf",
      "link": "https://futbolibretv.pages.dev/#partido-26612"
    },
    {
      "partido": "Serie A: Cremonese vs Atalanta",
      "link": "https://futbolibretv.pages.dev/#partido-26574"
    },
    {
      "partido": "LaLiga: Valencia vs Villarreal",
      "link": "https://futbolibretv.pages.dev/#partido-26570"
    },
    {
      "partido": "Primera A: Envigado vs Boyacá Chicó",
      "link": "https://futbolibretv.pages.dev/#partido-26595"
    },
    {
      "partido": "Premier League: Brentford vs Liverpool",
      "link": "https://futbolibretv.pages.dev/#partido-26566"
    },
    {
      "partido": "Serie B: Volta Redonda vs Coritiba",
      "link": "https://futbolibretv.pages.dev/#partido-26626"
    },
    {
      "partido": "Brasileirão: Atlético Mineiro vs Ceará",
      "link": "https://futbolibretv.pages.dev/#partido-26587"
    },
    {
      "partido": "Copa de la División Profesional: ABB vs Universitario de Vinto",
      "link": "https://futbolibretv.pages.dev/#partido-26623"
    },
    {
      "partido": "Serie B: Athletic Club vs América Mineiro",
      "link": "https://futbolibretv.pages.dev/#partido-26627"
    },
    {
      "partido": "Eredivisie: PEC Zwolle vs NEC",
      "link": "https://futbolibretv.pages.dev/#partido-26642"
    },
    {
      "partido": "Brasileirão: Vitória vs Corinthians",
      "link": "https://futbolibretv.pages.dev/#partido-26588"
    },
    {
      "partido": "Serie A: Mushuc Runa vs Manta",
      "link": "https://futbolibretv.pages.dev/#partido-26600"
    },
    {
      "partido": "Primera División: Cerro vs Peñarol",
      "link": "https://futbolibretv.pages.dev/#partido-26606"
    },
    {
      "partido": "LaLiga SmartBank: Mirandés vs Racing Santander",
      "link": "https://futbolibretv.pages.dev/#partido-26621"
    },
    {
      "partido": "Ligue 1: Lens vs Olympique Marseille",
      "link": "https://futbolibretv.pages.dev/#partido-26583"
    },
    {
      "partido": "Primeira Liga: Benfica vs Arouca",
      "link": "https://futbolibretv.pages.dev/#partido-26586"
    },
    {
      "partido": "Primeira Liga: Estrela vs Rio Ave",
      "link": "https://futbolibretv.pages.dev/#partido-26585"
    },
    {
      "partido": "Primera B: Bogotá vs Leones",
      "link": "https://futbolibretv.pages.dev/#partido-26630"
    },
    {
      "partido": "Primera A: Deportes Tolima vs Deportivo Cali",
      "link": "https://futbolibretv.pages.dev/#partido-26596"
    },
    {
      "partido": "Liga 1: Alianza Atlético vs Cienciano",
      "link": "https://futbolibretv.pages.dev/#partido-26561"
    },
    {
      "partido": "Brasileirão: Fluminense vs Internacional",
      "link": "https://futbolibretv.pages.dev/#partido-26589"
    },
    {
      "partido": "Primera División: Huachipato vs Deportes Iquique",
      "link": "https://futbolibretv.pages.dev/#partido-26594"
    },
    {
      "partido": "Primera División: Atlético Tembetary vs Sportivo Luqueño",
      "link": "https://futbolibretv.pages.dev/#partido-26603"
    },
    {
      "partido": "Primera B: Barranquilla vs Tigres",
      "link": "https://futbolibretv.pages.dev/#partido-26631"
    },
    {
      "partido": "Primera B: Cúcuta Deportivo vs Orsomarso",
      "link": "https://futbolibretv.pages.dev/#partido-26632"
    },
    {
      "partido": "Primera A: Atlético Bucaramanga vs Llaneros",
      "link": "https://futbolibretv.pages.dev/#partido-26597"
    },
    {
      "partido": "Serie A: Barcelona vs Libertad",
      "link": "https://futbolibretv.pages.dev/#partido-26601"
    },
    {
      "partido": "Serie B: Paysandu vs Avaí",
      "link": "https://futbolibretv.pages.dev/#partido-26628"
    },
    {
      "partido": "Brasileirão: Sport Recife vs Mirassol",
      "link": "https://futbolibretv.pages.dev/#partido-26590"
    },
    {
      "partido": "Primera División: Cerro Largo vs Racing",
      "link": "https://futbolibretv.pages.dev/#partido-26607"
    },
    {
      "partido": "Copa de la División Profesional: Guabirá vs Blooming",
      "link": "https://futbolibretv.pages.dev/#partido-26624"
    },
    {
      "partido": "Brasileirão: Fortaleza vs Flamengo",
      "link": "https://futbolibretv.pages.dev/#partido-26591"
    },
    {
      "partido": "Primera División: Sportivo Trinidense vs 2 de Mayo",
      "link": "https://futbolibretv.pages.dev/#partido-26604"
    },
    {
      "partido": "Liga MX: Tigres UANL vs Tijuana",
      "link": "https://futbolibretv.pages.dev/#partido-26635"
    },
    {
      "partido": "Liga 1: Cusco vs Atlético Grau",
      "link": "https://futbolibretv.pages.dev/#partido-26562"
    },
    {
      "partido": "Primera A: Santa Fe vs Millonarios",
      "link": "https://futbolibretv.pages.dev/#partido-26598"
    },
    {
      "partido": "Serie B: Criciúma vs Goiás",
      "link": "https://futbolibretv.pages.dev/#partido-26629"
    },
    {
      "partido": "Serie A: Deportivo Cuenca vs Aucas",
      "link": "https://futbolibretv.pages.dev/#partido-26602"
    },
    {
      "partido": "Copa de la División Profesional: Aurora vs Always Ready",
      "link": "https://futbolibretv.pages.dev/#partido-26625"
    },
    {
      "partido": "Primera División: Sporting San José vs Municipal Liberia",
      "link": "https://futbolibretv.pages.dev/#partido-26633"
    },
    {
      "partido": "Liga MX: León vs Pumas UNAM",
      "link": "https://futbolibretv.pages.dev/#partido-26636"
    },
    {
      "partido": "Liga MX: Guadalajara vs Atlas",
      "link": "https://futbolibretv.pages.dev/#partido-26637"
    },
    {
      "partido": "Brasileirão: São Paulo vs Bahia",
      "link": "https://futbolibretv.pages.dev/#partido-26592"
    },
    {
      "partido": "Primera División: Herediano vs Cartaginés",
      "link": "https://futbolibretv.pages.dev/#partido-26634"
    },
    {
      "partido": "Primera A: Once Caldas vs Unión Magdalena",
      "link": "https://futbolibretv.pages.dev/#partido-26599"
    },
    {
      "partido": "Liga de Expansión MX: Dorados vs Tlaxcala",
      "link": "https://futbolibretv.pages.dev/#partido-26615"
    },
    {
      "partido": "Liga MX: Cruz Azul vs Monterrey",
      "link": "https://futbolibretv.pages.dev/#partido-26638"
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
