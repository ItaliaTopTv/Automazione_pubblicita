from pyrogram import Client, filters
from pyrogram.types import Message

# Configurazioni
api_id = 23599261
api_hash = "521a804ba551dd302d15ad01f799429c"
session_name = "iptvitalia_pubblicita"
source_channel = -1002349094009  # ID del canale di partenza
target_channel = -1001430436385  # ID del canale di destinazione

# Avvio del client Pyrogram
app = Client(session_name, api_id=api_id, api_hash=api_hash)

@app.on_message(filters.chat(source_channel))
async def forward_message(client: Client, message: Message):
    try:
        if message.text:
            await client.send_message(
                chat_id=target_channel,
                text=message.text,
                entities=message.entities  # Mantiene la formattazione
            )
        elif message.photo:
            await client.send_photo(
                chat_id=target_channel,
                photo=message.photo.file_id,
                caption=message.caption,
                caption_entities=message.caption_entities,
            )
        elif message.animation:
            await client.send_animation(
                chat_id=target_channel,
                animation=message.animation.file_id,
                caption=message.caption,
                caption_entities=message.caption_entities,
            )
        # Puoi aggiungere qui altre gestioni per media (video, documenti, audio, ecc.)
    except Exception as e:
        print(f"Errore durante l'invio del messaggio: {e}")

print("Bot avviato...")
app.run()