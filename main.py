import os
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from collections import defaultdict
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_TARGET = os.getenv("CHANNEL_TARGET")  # contoh: @channelkamu
BOT_USERNAME = os.getenv("BOT_USERNAME")      # tanpa @
ADMIN_IDS = list(map(int, os.getenv("ADMIN_IDS", "").split(",")))
GROUP_FSUB = "@cari_teman_virtual_online"

bot = Client("menfess_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

user_limits = defaultdict(list)
lapor_aktif = set()

# ✅ Start
@bot.on_message(filters.command("start") & filters.private)
async def start(client, message):
    await message.reply(
        "👋 Kirim media dengan tag:\n"
        "#media #pap #cowok atau #media #pap #cewek\n"
        "Gunakan /lapor untuk kirim laporan.",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("✅ Join Group", url=f"https://t.me/{GROUP_FSUB.strip('@')}")],
            [InlineKeyboardButton("🔄 Cek Lagi", callback_data="checksub")]
        ])
    )

# ✅ Ping
@bot.on_message(filters.command("ping") & filters.private)
async def ping(client, message):
    await message.reply("🏓 Bot aktif!")

# ✅ Test channel
@bot.on_message(filters.command("testchannel") & filters.private)
async def test_post(client, message):
    try:
        await client.send_message(CHANNEL_TARGET, "✅ Test kirim ke channel berhasil.")
        await message.reply("✅ Bot berhasil mengirim pesan ke channel.")
    except Exception as e:
        await message.reply(f"❌ Gagal kirim ke channel:\n{e}")

# ✅ Lapor
@bot.on_message(filters.command("lapor") & filters.private)
async def start_lapor(client, message):
    lapor_aktif.add(message.from_user.id)
    await message.reply("📩 Silakan ketik laporanmu sekarang.")

@bot.on_message(filters.private & filters.text & ~filters.command(["start", "ping", "lapor", "stat", "testchannel"]))
async def proses_laporan(client, message):
    uid = message.from_user.id
    if uid in lapor_aktif:
        for admin in ADMIN_IDS:
            try:
                await client.send_message(admin, f"🚨 Laporan dari user `{uid}`:\n\n{message.text}")
            except:
                pass
        await message.reply("✅ Laporan kamu telah dikirim ke admin.")
        lapor_aktif.remove(uid)

# ✅ Statistik
@bot.on_message(filters.command("stat") & filters.private)
async def stat(client, message):
    uid = message.from_user.id
    if uid not in ADMIN_IDS:
        return
    now = datetime.now().date()
    lines = []
    for user_id, timestamps in user_limits.items():
        today = len([t for t in timestamps if t.date() == now])
        lines.append(f"👤 {user_id}: {today} media")
    await message.reply("\n".join(lines) if lines else "Belum ada pengirim hari ini.")

# ✅ Callback Cek FSub
@bot.on_callback_query(filters.regex("checksub"))
async def check_fsub(client, cb):
    uid = cb.from_user.id
    try:
        member = await client.get_chat_member(GROUP_FSUB, uid)
        if member.status in ("member", "administrator", "creator"):
            await cb.message.edit("✅ Terima kasih sudah join.")
        else:
            raise Exception()
    except:
        await cb.answer("❌ Kamu belum join!", show_alert=True)

# ✅ Handle media
@bot.on_message(filters.private & filters.media)
async def handle_media(client, message):
    uid = message.from_user.id
    tags = message.caption.lower() if message.caption else ""
    if not all(x in tags for x in ["#media", "#pap"]) or not any(x in tags for x in ["#cowok", "#cewek"]):
        await message.reply("⚠️ Gunakan tag: #media #pap #cowok atau #media #pap #cewek")
        return

    # FSub check (kecuali admin)
    if uid not in ADMIN_IDS:
        try:
            member = await client.get_chat_member(GROUP_FSUB, uid)
            if member.status not in ("member", "administrator", "creator"):
                raise Exception()
        except:
            await message.reply(
                "🚫 Kamu harus join grup dulu.",
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton("✅ Join", url=f"https://t.me/{GROUP_FSUB.strip('@')}"),
                    InlineKeyboardButton("🔄 Cek Ulang", callback_data="checksub")
                ]])
            )
            return

    # Limit harian (non-admin)
    now = datetime.now()
    if uid not in ADMIN_IDS:
        today = [t for t in user_limits[uid] if t.date() == now.date()]
        if len(today) >= 5:
            await message.reply("❌ Kamu sudah mencapai batas 5 media hari ini.")
            return
        user_limits[uid].append(now)

    # Copy ke bot sendiri dan buat link
    copied = await message.copy(BOT_USERNAME)
    link = f"https://t.me/{BOT_USERNAME}?start=media_{copied.id}"

    # Kirim ke channel target
    await client.send_message(
        CHANNEL_TARGET,
        f"📥 Kiriman anonim:\n🔗 {link}"
    )

    await message.reply("✅ Media kamu disimpan dan link dikirim ke channel.")

# ✅ Run bot
bot.run()
                
