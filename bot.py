from pyrogram import Client, filters
from pyrogram.types import Message
import asyncio
import os

# Configurazioni
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
session_name = os.getenv("SESSION_NAME")
source_channel = int(os.getenv("SOURCE_CHANNEL"))  # ID del canale di partenza
target_channel = int(os.getenv("TARGET_CHANNEL"))  # Nuovo ID del canale di destinazione
trigger_text = os.getenv("TRIGGER_TEXT")  # Testo per identificare i messaggi

# Avvio del client Pyrogram
app = Client(session_name, api_id=api_id, api_hash=api_hash)

# Funzione per inviare messaggi filtrati all'avvio
async def process_messages_on_startup():
    async with app:
        while True:
            try:
                # Recupera gli ultimi messaggi del canale di partenza
                async for message in app.get_chat_history(source_channel, limit=100):
                    if message.text and trigger_text in message.text:
                        filtered_text = message.text.replace(trigger_text, "").strip()
                        await app.send_message(
                            chat_id=target_channel,
                            text=filtered_text,
                            entities=message.entities or []  # Evita errori se None
                        )
                        print(f"Inviato messaggio di testo: {filtered_text}")
                    elif message.caption and trigger_text in message.caption:
                        filtered_caption = message.caption.replace(trigger_text, "").strip()
                        if message.photo:
                            await app.send_photo(
                                chat_id=target_channel,
                                photo=message.photo.file_id,
                                caption=filtered_caption,
                                caption_entities=message.caption_entities or [],
                            )
                            print(f"Inviata foto con didascalia: {filtered_caption}")
                        elif message.animation:
                            await app.send_animation(
                                chat_id=target_channel,
                                animation=message.animation.file_id,
                                caption=filtered_caption,
                                caption_entities=message.caption_entities or [],
                            )
                            print(f"Inviata animazione con didascalia: {filtered_caption}")
                        # Puoi aggiungere qui altre gestioni per media (video, documenti, audio, ecc.)

                print("Messaggi elaborati, attendo 60 minuti e 10 secondi...")
                await asyncio.sleep(3610)  # Attendi 60 minuti e 10 secondi prima di rieseguire

            except Exception as e:
                print(f"Errore durante l'elaborazione: {e}")

# Callback per inviare messaggi in tempo reale
@app.on_message(filters.chat(source_channel))
async def forward_message(client: Client, message: Message):
    try:
        if message.text and trigger_text in message.text:
            filtered_text = message.text.replace(trigger_text, "").strip()
            await client.send_message(
                chat_id=target_channel,
                text=filtered_text,
                entities=message.entities or []
            )
            print(f"Inviato messaggio di testo in tempo reale: {filtered_text}")
        elif message.caption and trigger_text in message.caption:
            filtered_caption = message.caption.replace(trigger_text, "").strip()
            if message.photo:
                await client.send_photo(
                    chat_id=target_channel,
                    photo=message.photo.file_id,
                    caption=filtered_caption,
                    caption_entities=message.caption_entities or [],
                )
                print(f"Inviata foto con didascalia in tempo reale: {filtered_caption}")
            elif message.animation:
                await client.send_animation(
                    chat_id=target_channel,
                    animation=message.animation.file_id,
                    caption=filtered_caption,
                    caption_entities=message.caption_entities or [],
                )
                print(f"Inviata animazione con didascalia in tempo reale: {filtered_caption}")
            # Puoi aggiungere qui altre gestioni per media (video, documenti, audio, ecc.)
    except Exception as e:
        print(f"Errore durante l'invio del messaggio: {e}")

print("Bot avviato...")
app.run(process_messages_on_startup())
