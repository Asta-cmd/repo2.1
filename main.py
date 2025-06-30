from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import os

# Ambil variabel lingkungan
API_ID_ENV = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
FORCE_SUB_CHANNEL = os.getenv("FORCE_SUB_CHANNEL")

# Validasi environment
if not API_ID_ENV:
    raise ValueError("❌ Environment variable API_ID tidak ditemukan.")
if not API_HASH:
    raise ValueError("❌ Environment variable API_HASH tidak ditemukan.")
if not BOT_TOKEN:
    raise ValueError("❌ Environment variable BOT_TOKEN tidak ditemukan.")
if not FORCE_SUB_CHANNEL:
    raise ValueError("❌ Environment variable FORCE_SUB_CHANNEL tidak ditemukan.")

API_ID = int(API_ID_ENV)

# Inisialisasi bot
bot = Client("ForceSubBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Start command
@bot.on_message(filters.private & filters.command("start"))
async def start(client, message):
    try:
        user_id = message.from_user.id
        member = await client.get_chat_member(FORCE_SUB_CHANNEL, user_id)
        if member.status not in ("member", "creator", "administrator"):
            raise Exception("User belum join")
    except:
        await message.reply(
            "🚫 Kamu harus join ke channel terlebih dahulu untuk menggunakan bot ini.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("✅ Join Channel", url=f"https://t.me/{FORCE_SUB_CHANNEL.replace('@', '')}")],
                [InlineKeyboardButton("🔄 Cek Lagi", callback_data="refresh")]
            ])
        )
        return

    await message.reply("✅ Kamu sudah bergabung. Silakan gunakan bot seperti biasa.")

# Handler tombol "Cek Lagi"
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

    await callback_query.message.edit("✅ Terima kasih sudah join. Silakan gunakan bot lagi.")

# Jalankan bot
bot.run()
