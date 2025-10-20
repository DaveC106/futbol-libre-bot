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
      "partido": "Al Shorta vs Al Ittihad",
      "link": "https://futbolibretv.pages.dev/#partido-26376"
    },
    {
      "partido": "Dordrecht vs RKC Waalwijk",
      "link": "https://futbolibretv.pages.dev/#partido-26385"
    },
    {
      "partido": "PSV II vs ADO Den Haag",
      "link": "https://futbolibretv.pages.dev/#partido-26386"
    },
    {
      "partido": "Roda JC vs Almere City",
      "link": "https://futbolibretv.pages.dev/#partido-26387"
    },
    {
      "partido": "Sport Huancayo vs Alianza Lima",
      "link": "https://futbolibretv.pages.dev/#partido-26359"
    },
    {
      "partido": "Al-Ahli vs Al Gharafa",
      "link": "https://futbolibretv.pages.dev/#partido-26377"
    },
    {
      "partido": "Cádiz vs Burgos",
      "link": "https://futbolibretv.pages.dev/#partido-26378"
    },
    {
      "partido": "Cremonese vs Udinese",
      "link": "https://futbolibretv.pages.dev/#partido-26364"
    },
    {
      "partido": "West Ham United vs Brentford",
      "link": "https://futbolibretv.pages.dev/#partido-26362"
    },
    {
      "partido": "Tigres vs Bogotá",
      "link": "https://futbolibretv.pages.dev/#partido-26381"
    },
    {
      "partido": "Deportivo Alavés vs Valencia",
      "link": "https://futbolibretv.pages.dev/#partido-26363"
    },
    {
      "partido": "Racing vs Juventud",
      "link": "https://futbolibretv.pages.dev/#partido-26374"
    },
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
# COMANDO /start
# ========================
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_name = message.from_user.first_name
    welcome_text = f"""¡Hola {user_name}! ⚽️

Soy *Fútbol Libre Bot*, tu asistente para ver partidos gratis.

📋 *Comandos disponibles:*
/partidos - Ver partidos de hoy
/ayuda - Guía completa y soluciones

¡Elige un comando y disfruta del fútbol! 🎉"""
    
    bot.reply_to(message, welcome_text, parse_mode='Markdown')
    print(f"✅ /start enviado a {user_name}")

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
        
        bot.reply_to(message, partidos_text, parse_mode='Markdown')
        print("✅ /partidos enviado")
        
    except Exception as e:
        print(f"Error en /partidos: {e}")
        bot.reply_to(message, "❌ Error al cargar los partidos. Intenta más tarde.")

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

❌ *¿No te anda el partido?*
👉 Probá primero estas soluciones:

📱 *En celular* → usar VPN (desbloquea los links)
💻 *En PC/TV* → cambiar DNS (arregla pantalla negra)

⚽️ *También podés:* ver cómo pedir partidos o usar modo incógnito

👇 *Elegí una opción del menú:*"""
    
    bot.send_message(message.chat.id, help_text, 
                    parse_mode='Markdown', reply_markup=keyboard)
    print("✅ /ayuda enviado")

# ========================
# MANEJAR BOTONES DEL TECLADO
# ========================
@bot.message_handler(func=lambda message: True)
def handle_buttons(message):
    text = message.text
    
    if text == "📱 Solución Celular (VPN)":
        response = """📱 *SOLUCIÓN CELULAR - VPN*

1. *Descargá una app VPN gratis:*
   - Turbo VPN (recomendado)
   - Windscribe
   - Hotspot Shield

2. *Conectate a cualquier servidor*

3. *Volvé a intentar el link*

¡Así se desbloquean todos los links! ✅"""
        
    elif text == "💻 Solución PC/TV (DNS)":
        response = """💻 *SOLUCIÓN PC/TV - DNS*

*Cambiá tus DNS para arreglar pantalla negra:*

1. *DNS Públicos:*
   - Google: 8.8.8.8 y 8.8.4.4
   - Cloudflare: 1.1.1.1 y 1.0.0.1

2. *En Windows:* Red → Propiedades → IPv4
3. *En Android:* WiFi → DNS privado
4. *En Smart TV:* Configuración de red

¡Listo, pantalla negra solucionada! ✅"""
        
    elif text == "🌐 Modo Incógnito":
        response = """🌐 *MODO INCÓGNITO*

*Si tenés problemas, probá en modo incógnito:*

1. *Chrome/Edge:* Ctrl+Shift+N
2. *Firefox:* Ctrl+Shift+P  
3. *Safari:* Cmd+Shift+N

*O también:*
- Limpiar caché del navegador
- Usar otro navegador
- Reiniciar el router

¡Suele solucionar muchos problemas! ✅"""
        
    elif text == "❌ Cerrar":
        bot.send_message(message.chat.id, "✅ Menú cerrado. Usa /ayuda para volver a abrir.", 
                        reply_markup=telebot.types.ReplyKeyboardRemove())
        return
        
    else:
        response = "🤔 No entendí tu mensaje. Usa /start para ver los comandos disponibles."
    
    bot.send_message(message.chat.id, response, parse_mode='Markdown')

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
