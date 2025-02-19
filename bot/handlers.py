import os
import re
import yt_dlp
import asyncio
from pyrogram import filters
from pyrogram.errors import FloodWait

# 🔹 सिर्फ .m3u8 वीडियो लिंक निकालने का फ़ंक्शन
def extract_m3u8_urls(text):
    url_pattern = re.compile(r'https?://\S+\.m3u8')  # सिर्फ .m3u8 URLs खोजो
    return url_pattern.findall(text)

def register_handlers(app):
    @app.on_message(filters.command("start"))
    def start(client, message):
        message.reply_text("Send me a .txt file containing M3U8 video links, and I'll download them one by one!")

    @app.on_message(filters.document & filters.private)
    def download_m3u8_from_txt(client, message):
        if not message.document.file_name.endswith(".txt"):
            return message.reply_text("Please send a .txt file containing M3U8 video links!")

        msg = message.reply_text("Processing file...")

        # 🔹 TXT फ़ाइल को मेमोरी में डाउनलोड करें
        file_bytes = client.download_media(message.document, in_memory=True)

        try:
            # 🔹 TXT फ़ाइल से टेक्स्ट पढ़ो और सिर्फ .m3u8 लिंक निकालो
            text_content = file_bytes.getvalue().decode("utf-8").strip()
            m3u8_urls = extract_m3u8_urls(text_content)

            if not m3u8_urls:
                return message.reply_text("The file doesn't contain valid M3U8 video links!")

            # 🔹 M3U8 VIDEO DOWNLOAD & UPLOAD
            msg.edit_text(f"Found {len(m3u8_urls)} M3U8 videos. Downloading one by one...")
            for index, m3u8_url in enumerate(m3u8_urls, start=1):
                msg.edit_text(f"Downloading M3U8 video {index}/{len(m3u8_urls)}...")

                video_path = f"video_{index}.mp4"
                ydl_opts = {
                    "format": "best",
                    "outtmpl": video_path
                }

                try:
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        ydl.download([m3u8_url])

                    msg.edit_text(f"Uploading M3U8 video {index}/{len(m3u8_urls)}...")

                    # 🔹 FLOOD WAIT ERROR HANDLE
                    try:
                        message.reply_video(video_path)
                    except FloodWait as e:
                        wait_time = e.value
                        msg.edit_text(f"FloodWait detected! Waiting for {wait_time} seconds...")
                        asyncio.sleep(wait_time)
                        message.reply_video(video_path)

                    os.remove(video_path)

                except Exception as e:
                    message.reply_text(f"Error downloading M3U8 video {index}: {str(e)}")

            msg.edit_text("All M3U8 videos processed!")

        except Exception as e:
            message.reply_text(f"Error: {str(e)}")