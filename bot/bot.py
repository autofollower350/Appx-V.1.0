import asyncio
from pyrogram import Client, idle
from config import API_ID, API_HASH, BOT_TOKEN
import handlers  # ✅ हैंडलर इम्पोर्ट करें

# ✅ Pyrogram Bot Mode सेट करें
app = Client("m3u8_video_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# ✅ सभी हैंडलर्स को लोड करें
handlers.register_handlers(app)

# ✅ Google Colab में बॉट को सही तरीके से स्टार्ट करें
async def start_bot():
    await app.start()
    print("✅ Bot is running...")
    await idle()  # ✅ बॉट को बैकग्राउंड में चलाने के लिए `idle()` का इस्तेमाल

loop = asyncio.get_event_loop()
loop.run_until_complete(start_bot())  # ✅ asyncio टास्क को सही तरीके से रन करें