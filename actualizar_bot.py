import re

# Leer el archivo actualizado
with open("partidos_actualizados.py", "r", encoding="utf-8") as f:
    partidos_actualizados = f.read()

# Leer el bot.py actual
with open("bot.py", "r", encoding="utf-8") as f:
    bot_content = f.read()

# Reemplazar la variable PARTIDOS_JSON
pattern = r'PARTIDOS_JSON = \{.*?\}'
updated_bot_content = re.sub(pattern, partidos_actualizados, bot_content, flags=re.DOTALL)

# Guardar el bot.py actualizado
with open("bot.py", "w", encoding="utf-8") as f:
    f.write(updated_bot_content)

print("✅ bot.py actualizado con los nuevos partidos")
