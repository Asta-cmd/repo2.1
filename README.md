
# Telegram Bot: FSUB + Menfess

Bot Telegram berbasis Pyrogram yang mewajibkan pengguna join channel terlebih dahulu sebelum bisa mengirim menfess ke channel tujuan.

## Fitur
- ✅ Cek wajib join (force subscribe)
- ✅ Kirim pesan menfess anonim ke channel
- ✅ Berbasis polling (tidak perlu webhook)

## Cara Jalankan (Lokal / Railway)

### 1. Clone Repo
```bash
git clone https://github.com/username/fsub-menfess-bot.git
cd fsub-menfess-bot
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Buat file `.env` dengan format:
```
API_ID=24946786
API_HASH=a7bb54f7f9cb222294e85803b395c7fb
BOT_TOKEN=7979742075:AAF3yyPO0KBdLTSgjeG7LGJWQ859masX0Ek
CHANNEL_FSUB=@asupanmenfesmu2
CHANNEL_TARGET=@tarothasupan

```

### 4. Jalankan bot
```bash
python main.py
```
