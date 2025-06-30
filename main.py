from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import os

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
FORCE_SUB_CHANNEL = os.getenv("FORCE_SUB_CHANNEL")

bot = Client("ForceSubBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@bot.on_message(filters.private & filters.command("start"))
async def start(client, message):
    try:
        user = message.from_user.id
        member = await client.get_chat_member(FORCE_SUB_CHANNEL, user)
        if member.status not in ("member", "creator", "administrator"):
            raise Exception("Not a member")
    except:
        await message.reply(
            f"🚫 Kamu harus join ke channel terlebih dahulu untuk menggunakan bot ini.",
            reply_markup=InlineKeyboardMarkup(
                [[
                    InlineKeyboardButton("✅ Join Channel", url=f"https://t.me/{FORCE_SUB_CHANNEL.replace('@', '')}"),
                    InlineKeyboardButton("🔄 Cek Lagi", callback_data="refresh")
                ]]
            )
        )
        return
    await message.reply("✅ Kamu sudah bergabung. Silakan gunakan bot seperti biasa.")

@bot.on_callback_query(filters.regex("refresh"))
async def refresh(client, callback_query):
    try:
        user = callback_query.from_user.id
        member = await client.get_chat_member(FORCE_SUB_CHANNEL, user)
        if member.status not in ("member", "creator", "administrator"):
            raise Exception("Not a member")
    except:
        await callback_query.answer("🚫 Kamu belum join!", show_alert=True)
        return
    await callback_query.message.edit("✅ Terima kasih sudah bergabung. Silakan gunakan bot lagi.")

bot.run()
