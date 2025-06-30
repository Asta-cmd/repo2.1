
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
API_ID=123456
API_HASH=your_api_hash
BOT_TOKEN=your_bot_token
CHANNEL_FSUB=@channel_wajib_join
CHANNEL_TARGET=@channel_menfess_tujuan
```

### 4. Jalankan bot
```bash
python main.py
```
