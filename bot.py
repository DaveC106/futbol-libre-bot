import telebot
from flask import Flask
import threading
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
import os

TOKEN = "7640481513:AAGXpRaze2oAK8XpQy6s7HphFWO-xvoKfzo"
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# ========================
# PARTIDOS DIRECTAMENTE EN EL CÓDIGO
# ========================
PARTIDOS_JSON = {
  "partidos": [
    {
      "partido": "Internacional Palmira vs Real Santander",
      "link": "https://futbolibretv.pages.dev/#partido-26383"
    },
    {
      "partido": "Boca Juniors de Cali vs Barranquilla",
      "link": "https://futbolibretv.pages.dev/#partido-26382"
    },
    {
      "partido": "Tigre vs Barracas Central",
      "link": "https://futbolibretv.pages.dev/#partido-26365"
    },
    {
      "partido": "Plaza Colonia vs Liverpool",
      "link": "https://futbolibretv.pages.dev/#partido-26375"
    },
    {
      "partido": "Deportivo Riestra vs Instituto",
      "link": "https://futbolibretv.pages.dev/#partido-26366"
    },
    {
      "partido": "Tristán Suárez vs Estudiantes Caseros",
      "link": "https://futbolibretv.pages.dev/#partido-26379"
    },
    {
      "partido": "Juventude vs RB Bragantino",
      "link": "https://futbolibretv.pages.dev/#partido-26368"
    },
    {
      "partido": "Vasco da Gama vs Fluminense",
      "link": "https://futbolibretv.pages.dev/#partido-26369"
    },
    {
      "partido": "Ferroviária vs Paysandu",
      "link": "https://futbolibretv.pages.dev/#partido-26380"
    },
    {
      "partido": "Sport Boys vs Melgar",
      "link": "https://futbolibretv.pages.dev/#partido-26360"
    },
    {
      "partido": "La Equidad vs Deportes Tolima",
      "link": "https://futbolibretv.pages.dev/#partido-26371"
    },
    {
      "partido": "El Nacional vs Deportivo Cuenca",
      "link": "https://futbolibretv.pages.dev/#partido-26373"
    },
    {
      "partido": "Atlético Tucumán vs San Lorenzo",
      "link": "https://futbolibretv.pages.dev/#partido-26367"
    },
    {
      "partido": "Santos vs Vitória",
      "link": "https://futbolibretv.pages.dev/#partido-26370"
    },
    {
      "partido": "Medellín vs Santa Fe",
      "link": "https://futbolibretv.pages.dev/#partido-26372"
    },
    {
      "partido": "Universitario vs Ayacucho",
      "link": "https://futbolibretv.pages.dev/#partido-26361"
    },
    {
      "partido": "Guadalupe vs Sporting San José",
      "link": "https://futbolibretv.pages.dev/#partido-26384"
    }
  ]
}

# ========================
# FOOTER PARA TODOS LOS MENSAJES
# ========================
def add_footer():
    return "\n\n🤔 *¿Quieres hacer algo más?*\nVolver al menú principal /menu"
    
def add_search_footer():
    return "\n\n🤔 *¿Quieres hacer algo más?*\nBuscar otro partido o /menu"

# ========================
# COMANDO /start Y /menu
# ========================
@bot.message_handler(commands=['start', 'menu'])
def send_welcome(message):
    user_name = message.from_user.first_name
    welcome_text = f"""¡Hola {user_name}! 👋

Soy el Bot de *Fútbol Libre*, tu asistente para ver partidos gratis.

✅ *Comandos disponibles:*
/partidos - Ver los partidos de hoy
/ayuda - Guía completa y soluciones

*¿Buscas un partido específico?* 🔍
¡Solo escribe el nombre del equipo o una palabra clave! ⚡

¡Elige un comando y disfruta del fútbol! 🎉"""
    
    full_message = welcome_text + add_footer()
    bot.reply_to(message, full_message, parse_mode='Markdown')
    print(f"✅ /{message.text[1:]} enviado a {user_name}")

# ========================
# COMANDO /partidos 
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
# COMANDO /ayuda CON TECLADO
# ========================
@bot.message_handler(commands=['ayuda'])
def send_help(message):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton("📱 Solución Celular (VPN)"))
    keyboard.add(KeyboardButton("💻 Solución PC/TV (DNS)"))
    keyboard.add(KeyboardButton("🌐 Modo Incógnito"))
    keyboard.add(KeyboardButton("❌ Cerrar"))
    
    help_text = """📖 *AYUDA RÁPIDA* 📖

❌ *¿No puedes ver el partido?*
👉 Prueba primero estas soluciones:

📱 *En celular* → usar VPN (desbloquea los links)
💻 *En PC/TV* → cambiar DNS (arregla pantalla negra)

⚽️ *También puedes:* ver cómo pedir partidos o usar modo incógnito

👇 *Elige una opción del menú:*"""
    
    full_message = help_text + add_footer()
    bot.send_message(message.chat.id, full_message, 
                    parse_mode='Markdown', reply_markup=keyboard)
    print("✅ /ayuda enviado")

# ========================
# SISTEMA DE BÚSQUEDA INTELIGENTE
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
            result_result += "• Revisa la ortografía\n"
            result_text += "• Usa términos más generales (ej: 'boca', 'madrid')\n"
            result_text += "• Ver todos los partidos con /partidos"
        
        full_message = result_text + add_search_footer()
        bot.reply_to(message, full_message, parse_mode='Markdown')
        print(f"🔍 Búsqueda: '{search_term}' → {len(matches)} resultados")
        
    except Exception as e:
        print(f"Error en búsqueda: {e}")
        error_message = "❌ Error en la búsqueda. Intenta más tarde." + add_footer()
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
    
    # Si es un botón del teclado, manejarlo
    button_texts = ["📱 solución celular (vpn)", "💻 solución pc/tv (dns)", "🌐 modo incógnito", "❌ cerrar"]
    if text in button_texts:
        handle_buttons(message)
        return
    
    # Si no es comando ni botón, es una búsqueda
    search_matches(message, text)

# ========================
# MANEJAR BOTONES DEL TECLADO
# ========================
def handle_buttons(message):
    text = message.text
    
    if text == "📱 Solución Celular (VPN)":
        response = """📱 *SOLUCIÓN CELULAR - VPN*

1. *Descarga una app VPN gratis:*
   - Turbo VPN (recomendado)
   - Windscribe
   - Hotspot Shield

2. *Conéctate a cualquier servidor*

3. *Vuelve a intentar el link*

¡Así se desbloquean todos los links! ✅"""
        
    elif text == "💻 Solución PC/TV (DNS)":
        response = """💻 *SOLUCIÓN PC/TV - DNS*

*Cambia tus DNS para arreglar pantalla negra:*

1. *DNS Públicos:*
   - Google: 8.8.8.8 y 8.8.4.4
   - Cloudflare: 1.1.1.1 y 1.0.0.1

2. *En Windows:* Red → Propiedades → IPv4
3. *En Android:* WiFi → DNS privado
4. *En Smart TV:* Configuración de red

¡Listo, pantalla negra solucionada! ✅"""
        
    elif text == "🌐 Modo Incógnito":
        response = """🌐 *MODO INCÓGNITO*

*Si tienes problemas, prueba en modo incógnito:*

1. *Chrome/Edge:* Ctrl+Shift+N
2. *Firefox:* Ctrl+Shift+P  
3. *Safari:* Cmd+Shift+N

*O también:*
- Limpiar caché del navegador
- Usar otro navegador
- Reiniciar el router

¡Suele solucionar muchos problemas! ✅"""
        
    elif text == "❌ Cerrar":
        close_message = "✅ Menú cerrado." + add_footer()
        bot.send_message(message.chat.id, close_message, 
                        reply_markup=telebot.types.ReplyKeyboardRemove())
        return
    
    full_response = response + add_footer()
    bot.send_message(message.chat.id, full_response, parse_mode='Markdown')

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
