import telebot
from flask import Flask
import threading
import requests
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
import os

TOKEN = "7640481513:AAGXpRaze2oAK8XpQy6s7HphFWO-xvoKfzo"
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

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
        partidos = obtener_partidos_desde_url()
        
        if partidos:
            partidos_text = "⚽️ *PARTIDOS DE HOY* ⚽️\n\n"
            
            for i, partido in enumerate(partidos, 1):
                partidos_text += f"*{i}. {partido['liga']}*\n"
                partidos_text += f"🕐 {partido['hora']} - {partido['equipos']}\n"
                partidos_text += f"📺 {partido['canales']}\n"
                partidos_text += f"🔗 {partido['link']}\n\n"
            
            partidos_text += "_⚠️ Los links pueden requerir VPN/DNS_"
        else:
            partidos_text = "❌ *No hay partidos disponibles en este momento.*\n\nIntenta más tarde o usa /ayuda para soporte."
        
        bot.reply_to(message, partidos_text, parse_mode='Markdown')
        print("✅ /partidos enviado")
        
    except Exception as e:
        print(f"Error en /partidos: {e}")
        bot.reply_to(message, "❌ Error al cargar los partidos. Intenta más tarde.")

def obtener_partidos_desde_url():
    """Obtiene partidos desde tu URL de agenda"""
    try:
        url = "https://futbolibretv.pages.dev/agenda"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error HTTP: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error obteniendo partidos: {e}")
        return None

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

*Cambiá tus DNS para arregla pantalla negra:*

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
