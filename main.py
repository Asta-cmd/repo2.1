from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import os

API_ID_ENV = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
FORCE_SUB_CHANNEL = os.getenv("FORCE_SUB_CHANNEL")
CHANNEL_TARGET = os.getenv("CHANNEL_TARGET")

if not all([API_ID_ENV, API_HASH, BOT_TOKEN, FORCE_SUB_CHANNEL, CHANNEL_TARGET]):
    raise ValueError("❌ Salah satu variabel lingkungan belum diset.")

API_ID = int(API_ID_ENV)

bot = Client("ForceSubBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

def is_valid_tag(text):
    if not text:
        return False
    tags = ["#media", "#pap"]
    gender = ["#cowok", "#cewek"]
    return any(tag in text.lower() for tag in tags) and any(g in text.lower() for g in gender)

@bot.on_message(filters.private & filters.command("start"))
async def start(client, message):
    try:
        user_id = message.from_user.id
        member = await client.get_chat_member(FORCE_SUB_CHANNEL, user_id)
        if member.status not in ("member", "creator", "administrator"):
            raise Exception("Belum join")
    except:
        await message.reply(
            "Maaf,kamu harus join ke grup/channel dibawah ini untuk mengirim media.
            jika kamu telah join,pencet restart.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Join Channel", url=f"https://t.me/{FORCE_SUB_CHANNEL.replace('@', '')}")],
                [InlineKeyboardButton("Restart", callback_data="refresh")]
            ])
        )
        return
    await message.reply("Kamu sudah bergabung. penting di ingat bahwa Admin 100% menjaga privasi pengirim.
    agar media dapat terkirim, kirim media dengan tag seperti: `#media #pap #cowok` atau `#media #pap #cewek`")

@bot.on_message(filters.private & filters.command("ping"))
async def ping(client, message):
    await message.reply("apakah kita saling kenal?!")

@bot.on_callback_query(filters.regex("refresh"))
async def refresh(client, callback_query):
    try:
        user = callback_query.from_user.id
        member = await client.get_chat_member(FORCE_SUB_CHANNEL, user)
        if member.status not in ("member", "creator", "administrator"):
            raise Exception("Belum join")
    except:
        await callback_query.answer("❌ Kamu belum join!", show_alert=True)
        return
    await callback_query.message.edit("✅ Terima kasih sudah join. Kirim media sekarang.")

@bot.on_message(filters.private & filters.media)
async def handle_media(client, message):
    try:
        user_id = message.from_user.id
        member = await client.get_chat_member(FORCE_SUB_CHANNEL, user_id)
        if member.status not in ("member", "creator", "administrator"):
            raise Exception("Belum join")
    except:
        await message.reply("🚫 Kamu belum join channel. Silakan join dulu.")
        return

    if not is_valid_tag(message.caption):
        await message.reply("⚠️ Media harus dikirim dengan tag seperti: `#media #pap #cowok` atau `#media #pap #cewek`")
        return

    try:
        await client.copy_message(CHANNEL_TARGET, from_chat_id=message.chat.id, message_id=message.id)
        await message.reply("✅ Media berhasil dikirim ke channel.")
    except Exception as e:
        await message.reply(f"❌ Gagal kirim ke channel: {str(e)}")

bot.run()
    
