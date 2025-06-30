
import os
from pyrogram import Client, filters

API_ID = int(os.getenv("24946786"))
API_HASH = os.getenv("a7bb54f7f9cb222294e85803b395c7fb")
BOT_TOKEN = os.getenv("7979742075:AF3yyPO0KBdLTSgjeG7LGJWQ859masX0Ek")
CHANNEL_FSUB = os.getenv("@asupanmenfesmu2")
CHANNEL_TARGET = os.getenv("@tarothasupan")

app = Client("bot", api_id=24946786, api_hash=a7bb54f7f9cb222294e85803b395c7fb, bot_token=AF3yyPO0KBdLTSgjeG7LGJWQ859masX0Ek)

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
