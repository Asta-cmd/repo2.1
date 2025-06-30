
import os
from pyrogram import Client, filters

API_ID = os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_FSUB = os.getenv("CHANNEL_FSUB")

app = Client("bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.private & filters.command("start"))
async def start(client, message):
    user = message.from_user.id
    try:
        member = await client.get_chat_member(CHANNEL_FSUB, user)
        if member.status in ("member", "administrator", "creator"):
            await message.reply("Selamat datang! Silakan kirim menfess kamu:")
        else:
            raise Exception("Not a member")
    except:
        await message.reply(f"🚫 Kamu harus join dulu ke {CHANNEL_FSUB} untuk menggunakan bot ini.")

@app.on_message(filters.private & ~filters.command("start"))
async def handle_menfess(client, message):
    user = message.from_user.id
    try:
        member = await client.get_chat_member(CHANNEL_FSUB, user)
        if member.status in ("member", "administrator", "creator"):
            await client.send_message(CHANNEL_TARGET, f"#Menfess"

"{message.text}")
            await message.reply("✅ Menfess kamu berhasil dikirim!")
        else:
            raise Exception("Not a member")
    except:
        await message.reply(f"🚫 Kamu belum join {CHANNEL_FSUB}. Silakan join dulu.")

app.run()
