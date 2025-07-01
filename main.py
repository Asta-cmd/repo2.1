from datetime import datetime, timedelta
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import os
from collections import defaultdict

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
FORCE_SUB_GROUP = "@cari_teman_virtual_online"
CHANNEL_TARGET = os.getenv("CHANNEL_TARGET")  # contoh: @pap_cewek_cowok
BOT_USERNAME = os.getenv("BOT_USERNAME")      # tanpa @
ADMIN_IDS = os.getenv("ADMIN_IDS", "")

admin_ids = [int(x) for x in ADMIN_IDS.split(",") if x.strip().isdigit()]
user_daily_limit = defaultdict(list)
user_stats = defaultdict(int)
media_storage = {}
lapor_aktif = set()

bot = Client("AnonMediaBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

def is_valid_tag(text):
    if not text:
        return False
    return all(tag in text.lower() for tag in ["#media", "#pap"]) and (
        "#cowok" in text.lower() or "#cewek" in text.lower()
    )

def is_today(dt):
    return dt.date() == datetime.now().date()

@bot.on_message(filters.private & filters.command("start"))
async def start(client, message):
    args = message.text.split(" ", 1)
    if len(args) == 2 and args[1].startswith("media_"):
        media_id = int(args[1].replace("media_", ""))
        if media_id in media_storage:
            data = media_storage[media_id]
            if datetime.now() - data["time"] > timedelta(days=10):
                await message.reply("⏳ Media sudah kedaluwarsa dan telah dihapus otomatis.")
            else:
                try:
                    await message.reply_cached_media(data["msg_id"])
                except:
                    await message.reply("❌ Gagal memuat media.")
        else:
            await message.reply("❌ Media tidak ditemukan.")
    else:
        await message.reply("👋 Kirim media dengan tag:\n`#media #pap #cowok` atau `#media #pap #cewek`\nGunakan /lapor untuk menghubungi admin.")

@bot.on_message(filters.private & filters.command("ping"))
async def ping(client, message):
    await message.reply("🏓 Bot aktif!")

@bot.on_message(filters.private & filters.command("stats"))
async def stats(client, message):
    uid = message.from_user.id
    if uid not in admin_ids:
        await message.reply("❌ Perintah ini hanya untuk admin.")
        return
    lines = ["📊 Statistik Pengiriman:"]
    for user, total in user_stats.items():
        lines.append(f"👤 User `{user}`: {total} media")
    await message.reply("\n".join(lines))

@bot.on_message(filters.private & filters.command("lapor"))
async def start_lapor(client, message):
    uid = message.from_user.id
    lapor_aktif.add(uid)
    await message.reply("📩 Silakan ketik laporanmu sekarang. Bot akan meneruskan ke admin.")

@bot.on_message(filters.private & filters.text & ~filters.command(["start", "ping", "stats"]))
async def proses_laporan(client, message):
    uid = message.from_user.id
    if uid in lapor_aktif:
        for admin in admin_ids:
            try:
                await client.send_message(admin, f"🚨 Laporan dari user `{uid}`:\n\n{message.text}")
            except:
                pass
        await message.reply("✅ Laporan kamu telah dikirim ke admin.")
        lapor_aktif.remove(uid)

@bot.on_message(filters.private & filters.media)
async def handle_media(client, message):
    uid = message.from_user.id

    if uid not in admin_ids:
        try:
            member = await client.get_chat_member(FORCE_SUB_GROUP, uid)
            if member.status not in ("member", "administrator", "creator"):
                raise Exception("Belum join")
        except:
            await message.reply(
                "🚫 Kamu harus join grup terlebih dahulu.",
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton("✅ Join Grup", url=f"https://t.me/{FORCE_SUB_GROUP.replace('@', '')}"),
                    InlineKeyboardButton("🔄 Cek Lagi", callback_data="refresh")
                ]])
            )
            return

    if not is_valid_tag(message.caption):
        await message.reply("⚠️ Gunakan tag: `#media #pap #cowok` atau `#media #pap #cewek`")
        return

    recent = [t for t in user_daily_limit[uid] if is_today(t)]
    if uid not in admin_ids and len(recent) >= 5:
        await message.reply("❌ Kamu sudah mencapai batas 5 media hari ini.")
        return

    copied = await message.copy(BOT_USERNAME)
    media_id = copied.id
    media_storage[media_id] = {
        "uid": uid,
        "msg_id": copied.id,
        "time": datetime.now(),
        "deleted": False
    }

    link = f"https://t.me/{BOT_USERNAME}?start=media_{media_id}"
    note = f"\n\n👁️ ID: `{uid}`" if uid in admin_ids else ""

    await client.send_message(
        CHANNEL_TARGET,
        f"📥 Media baru diterima!\n🔗 Klik untuk lihat: {link}{note}",
        disable_web_page_preview=True
    )

    user_daily_limit[uid].append(datetime.now())
    user_stats[uid] += 1
    await message.reply("✅ Media kamu disimpan dan link dikirim ke channel.")

@bot.on_callback_query(filters.regex("refresh"))
async def refresh(client, cb):
    uid = cb.from_user.id
    if uid in admin_ids:
        await cb.message.edit("✅ Kamu admin. Lanjut.")
        return
    try:
        member = await client.get_chat_member(FORCE_SUB_GROUP, uid)
        if member.status in ("member", "administrator", "creator"):
            await cb.message.edit("✅ Terima kasih sudah join!")
        else:
            raise Exception()
    except:
        await cb.answer("❌ Kamu belum join!", show_alert=True)

# Fungsi penghapusan otomatis (panggil manual/scheduler)
async def auto_delete_old_media():
    now = datetime.now()
    for mid, data in list(media_storage.items()):
        if not data["deleted"] and now - data["time"] > timedelta(days=10):
            try:
                await bot.delete_messages(BOT_USERNAME, data["msg_id"])
                media_storage[mid]["deleted"] = True
            except:
                pass
@bot.on_message(filters.private & filters.command("testchannel"))
async def test_post(client, message):
    try:
        await client.send_message(CHANNEL_TARGET, "✅ Test kirim ke channel berhasil.")
        await message.reply("✅ Bot berhasil mengirim pesan ke channel.")
    except Exception as e:
        await message.reply(f"❌ Gagal kirim ke channel:\n{e}")
        
bot.run()
