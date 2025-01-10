from pyrogram import Client
import asyncio
import os
import re

# Configurazioni del bot, lette da variabili di ambiente
# Questi parametri sono forniti durante il deploy (ad esempio su Render)
api_id = int(os.getenv("API_ID"))  # ID API dell'app Telegram
api_hash = os.getenv("API_HASH")  # Hash API associato
session_name = os.getenv("SESSION_NAME")  # Nome della sessione (es: stringa con sessione salvata)
source_channel = int(os.getenv("SOURCE_CHANNEL"))  # ID del canale di partenza
target_channel = int(os.getenv("TARGET_CHANNEL"))  # ID del canale di destinazione
trigger_text = os.getenv("TRIGGER_TEXT")  # Testo specifico da cercare nei messaggi

# Creazione del client Pyrogram
app = Client(session_name, api_id=api_id, api_hash=api_hash)

# Funzione principale per l'elaborazione periodica dei messaggi
async def process_messages_periodically():
    """Elabora i messaggi del canale sorgente e li inoltra al canale di destinazione ogni 60 minuti e 10 secondi."""
    async with app:
        while True:  # Loop infinito per l'elaborazione periodica
            try:
                # Recupera gli ultimi 100 messaggi dal canale sorgente
                async for message in app.get_chat_history(source_channel, limit=100):
                    # Verifica se il messaggio è di testo e contiene il trigger
                    if message.text and trigger_text in message.text:
                        # Rimuove il trigger dal testo e invia al canale di destinazione
                        filtered_text = message.text.replace(trigger_text, "").strip()
                        await app.send_message(
                            chat_id=target_channel,
                            text=filtered_text,
                            entities=message.entities or []  # Mantiene formattazioni come link, grassetto, ecc.
                        )
                        print(f"Inviato messaggio di testo: {filtered_text}")
                    # Verifica se il messaggio è una foto con una didascalia contenente il trigger
                    elif message.caption and trigger_text in message.caption:
                        filtered_caption = message.caption.replace(trigger_text, "").strip()
                        if message.photo:  # Se è una foto
                            await app.send_photo(
                                chat_id=target_channel,
                                photo=message.photo.file_id,
                                caption=filtered_caption,
                                caption_entities=message.caption_entities or [],
                            )
                            print(f"Inviata foto con didascalia: {filtered_caption}")
                        elif message.animation:  # Se è un'animazione (GIF o video animato)
                            await app.send_animation(
                                chat_id=target_channel,
                                animation=message.animation.file_id,
                                caption=filtered_caption,
                                caption_entities=message.caption_entities or [],
                            )
                            print(f"Inviata animazione con didascalia: {filtered_caption}")

                # Attende 60 minuti e 10 secondi prima di ricominciare l'elaborazione
                print("Messaggi elaborati, attendo 60 minuti e 10 secondi...")
                await asyncio.sleep(3610)

            except Exception as e:
                # Gestione dell'errore specifico per la slowmode di Telegram
                match = re.search(r"\[420 SLOWMODE_WAIT_X\].*?(\d+) seconds", str(e))
                if match:
                    wait_time = int(match.group(1))  # Estrae il tempo di attesa dai dettagli dell'errore
                    print(f"Errore di slowmode, attendo {wait_time} secondi...")
                    await asyncio.sleep(wait_time)  # Attende il tempo richiesto prima di riprovare
                else:
                    print(f"Errore durante l'elaborazione: {e}")  # Log generico per altri tipi di errori

# Avvio del bot con l'elaborazione periodica
print("Bot avviato...")
app.run(process_messages_periodically())
