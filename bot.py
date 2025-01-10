from pyrogram import Client, filters
from pyrogram.types import Message
import asyncio

# Configurazioni
api_id = 23599261
api_hash = "521a804ba551dd302d15ad01f799429c"
session_name = "iptvitalia_pubblicita"
source_channel = -1002349094009  # ID del canale di partenza
target_channel = -1001430436385  # Nuovo ID del canale di destinazione
trigger_text = "-pubblicita_completa"  # Testo per identificare i messaggi

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
                            entities=message.entities  # Mantiene la formattazione
                        )
                    elif message.caption and trigger_text in message.caption:
                        filtered_caption = message.caption.replace(trigger_text, "").strip()
                        if message.photo:
                            await app.send_photo(
                                chat_id=target_channel,
                                photo=message.photo.file_id,
                                caption=filtered_caption,
                                caption_entities=message.caption_entities,
                            )
                        elif message.animation:
                            await app.send_animation(
                                chat_id=target_channel,
                                animation=message.animation.file_id,
                                caption=filtered_caption,
                                caption_entities=message.caption_entities,
                            )
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
                entities=message.entities
            )
        elif message.caption and trigger_text in message.caption:
            filtered_caption = message.caption.replace(trigger_text, "").strip()
            if message.photo:
                await client.send_photo(
                    chat_id=target_channel,
                    photo=message.photo.file_id,
                    caption=filtered_caption,
                    caption_entities=message.caption_entities,
                )
            elif message.animation:
                await client.send_animation(
                    chat_id=target_channel,
                    animation=message.animation.file_id,
                    caption=filtered_caption,
                    caption_entities=message.caption_entities,
                )
            # Puoi aggiungere qui altre gestioni per media (video, documenti, audio, ecc.)
    except Exception as e:
        print(f"Errore durante l'invio del messaggio: {e}")

print("Bot avviato...")
app.run(process_messages_on_startup())
