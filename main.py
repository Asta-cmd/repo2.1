from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import os

API_ID_ENV = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
FORCE_SUB_CHANNEL = os.getenv("FORCE_SUB_CHANNEL")

print("🔧 Loading environment variables...")

if not API_ID_ENV:
    raise ValueError("❌ Environment variable API_ID tidak ditemukan.")
if not API_HASH:
    raise ValueError("❌ Environment variable API_HASH tidak ditemukan.")
if not BOT_TOKEN:
    raise ValueError("❌ Environment variable BOT_TOKEN tidak ditemukan.")
if not FORCE_SUB_CHANNEL:
    raise ValueError("❌ Environment variable FORCE_SUB_CHANNEL tidak ditemukan.")

API_ID = int(API_ID_ENV)

print("✅ ENV loaded. Starting bot...")
print(f"📡 FORCE_SUB_CHANNEL set to: {FORCE_SUB_CHANNEL}")

bot = Client("ForceSubBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@bot.on_message(filters.private & filters.command("start"))
async def start(client, message):
    user_id = message.from_user.id
    print(f"📥 Received /start from user ID: {user_id}")
    try:
        member = await client.get_chat_member(FORCE_SUB_CHANNEL, user_id)
        print(f"👤 Member status: {member.status}")
        if member.status not in ("member", "creator", "administrator"):
            raise Exception("User belum join channel.")
    except Exception as e:
        print(f"❌ Exception during membership check: {e}")
        await message.reply(
            "🚫 Kamu harus join ke channel terlebih dahulu untuk menggunakan bot ini.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("✅ Join Channel", url=f"https://t.me/{FORCE_SUB_CHANNEL.replace('@', '')}")],
                [InlineKeyboardButton("🔄 Cek Lagi", callback_data="refresh")]
            ])
        )
        return

    await message.reply("✅ Kamu sudah bergabung. Silakan gunakan bot seperti biasa.")

@bot.on_callback_query(filters.regex("refresh"))
async def refresh(client, callback_query):
    user_id = callback_query.from_user.id
    print(f"🔄 Refresh clicked by user ID: {user_id}")
    try:
        member = await client.get_chat_member(FORCE_SUB_CHANNEL, user_id)
        print(f"🔁 Member status on refresh: {member.status}")
        if member.status not in ("member", "creator", "administrator"):
            raise Exception("User belum join channel.")
    except Exception as e:
        print(f"❌ Exception during refresh check: {e}")
        await callback_query.answer("❌ Kamu belum join!", show_alert=True)
        return

    await callback_query.message.edit("✅ Terima kasih sudah join. Silakan gunakan bot lagi.")

@bot.on_message(filters.private & filters.command("ping"))
async def ping(client, message):
    await message.reply("🏓 Bot aktif!")

print("🚀 Bot is running...")
bot.run()
