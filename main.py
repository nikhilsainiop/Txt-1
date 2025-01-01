import requests
import json
import subprocess
import time
import asyncio
import sys
import os
import random
import re
import tempfile
import datetime
from urllib.parse import urlparse, parse_qs
from bs4 import BeautifulSoup

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, User
from pyrogram.errors import FloodWait
from pyrogram.errors.exceptions.bad_request_400 import StickerEmojiInvalid
from pyromod import listen
from aiohttp import ClientSession

import helper
from helper import get_drm_keys
from logger import logging
from p_bar import progress_bar
from config import *

bot = Client(
    "bot",
    bot_token="7982396596:AAGZJZj1Gqc6XV46-9nXl-af1mhwAnLV6PU",
    api_id=28094744,
    api_hash="a75af4285edc7747c57bb19147ca0b9b"
)

auth_users = [5680454765]
owner_id = 5680454765

cookies_file_path = os.getenv("COOKIES_FILE_PATH", "youtube_cookies.txt")

failed_links = []
fail_cap = "**➜ This file contains failed downloads while downloading. You can retry them one more time.**"

global videocount, pdfcount

pwdl = os.environ.get("api")
processing_request = False

keyboard = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(text="👨🏻‍💻 Developer", url="https://t.me/AllCourseADMIN_BOT"),
            InlineKeyboardButton(text="❣️ BIG DEAL", url="https://t.me/+h5M1Xp0a7rM5ZDhl"),
        ],
        [InlineKeyboardButton(text="🪄 Updates Channel", url="https://t.me/+VFhUKQvM7PVlYWQ1")],
    ]
)

Busy = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(text="👨🏻‍💻 Developer", url="https://t.me/AllCourseADMIN_BOT"),
            InlineKeyboardButton(text="❣️ BIG DEAL", url="https://t.me/+h5M1Xp0a7rM5ZDhl"),
        ],
        [InlineKeyboardButton(text="Join to Check My Status", url="https://t.me/+VFhUKQvM7PVlYWQ1")],
    ]
)

@bot.on_message(filters.command(["logs"]))
async def send_logs(bot: Client, m: Message):
    try:
        with open("Assist.txt", "rb") as file:
            sent = await m.reply_text("**📤 Sending you ....**")
            await m.reply_document(document=file)
            await sent.delete()
    except Exception as e:
        await m.reply_text(f"Error sending logs: {e}")

image_urls = ["https://envs.sh/8lA.jpg"]

@bot.on_message(filters.command(["start"]))
async def start_command(bot: Client, message: Message):
    random_image_url = random.choice(image_urls)
    caption = ("**𝐇𝐞𝐥𝐥𝐨 𝐃𝐞𝐚𝐫  👋!\n\n➠ 𝐈 𝐚𝐦 𝐚 𝐓𝐞𝐱𝐭 𝐃𝐨𝐰𝐧𝐥𝐨𝐚𝐝𝐞𝐫 𝐁𝐨𝐭 𝐌𝐚𝐝𝐞 𝐖𝐢𝐭𝐡 ♥️\n"
               "➠ Can Extract Videos & Pdf Form Your Text File and Upload to Telegram\n\n"
               "➠ 𝐔𝐬𝐞 /drm 𝐂𝐨𝐦𝐦𝐚𝐧𝐝 𝐓𝐨 𝐃𝐨𝐰𝐧𝐥𝐨𝐚𝐝 𝐅𝐫𝐨𝐦 𝐓𝐗𝐓 𝐅𝐢𝐥𝐞\n\n"
               "➠𝐌𝐚𝐝𝐞 𝐁𝐲: @AllCourseADMIN_BOT **\n")
    await bot.send_photo(chat_id=message.chat.id, photo=random_image_url, caption=caption, reply_markup=keyboard)

@bot.on_message(filters.command('h2t'))
async def run_bot(bot: Client, m: Message):
    user_id = m.from_user.id
    if user_id not in auth_users:
        await m.reply_text("**HEY BUDDY THIS IS ONLY FOR MY ADMINS TO USE THIS. CONTACT MY DEV: @AllCourseADMIN_BOT**")
    else:
        editable = await m.reply_text("Send Your HTML file\n")
        input: Message = await bot.listen(editable.chat.id)
        html_file = await input.download()
        await input.delete()
        await editable.delete()
        with open(html_file, 'r') as f:
            soup = BeautifulSoup(f, 'html.parser')
            tables = soup.find_all('table')
            videos = []
            for table in tables:
                rows = table.find_all('tr')
                for row in rows:
                    cols = row.find_all('td')
                    name = cols[0].get_text().strip()
                    link = cols[1].find('a')['href']
                    videos.append(f'{name}:{link}')
        txt_file = os.path.splitext(html_file)[0] + '.txt'
        with open(txt_file, 'w') as f:
            f.write('\n'.join(videos))
        await m.reply_document(document=txt_file, caption="Here is your txt file.")
        os.remove(txt_file)

def is_subscription_expired(user_id):
    with open("Subscription_data.txt", "r") as file:
        for line in file:
            data = line.strip().split(", ")
            if int(data[0]) == user_id:
                end_date = datetime.datetime.strptime(data[2], "%d-%m-%Y")
                today = datetime.datetime.today()
                return end_date < today
    return True

@bot.on_message(filters.command("myplan"))
async def myplan_command_handler(bot, message):
    user_id = message.from_user.id
    with open("Subscription_data.txt", "r") as file:
        for line in file:
            data = line.strip().split(", ")
            if int(data[0]) == user_id:
                subscription_start = data[1]
                expiration_date = data[2]
                today = datetime.datetime.today()
                if today > datetime.datetime.strptime(expiration_date, "%d-%m-%Y"):
                    plan = "EXPIRED"
                    response_text = (f"**✨ User ID: {user_id}\n📊 PLAN STAT: {plan}\n\n"
                                     f"🔰 Activated on: {subscription_start}\n🧨 Expiration Date: {expiration_date} \n\n"
                                     f"🫰🏼 ACTIVATE YOUR PLAN AGAIN! ✨**")
                else:
                    plan = "ALIVE!"
                    response_text = (f"**✨ User ID: {user_id}\n📊 PLAN STAT: {plan}\n"
                                     f"🔰 Activated on: {subscription_start}\n🧨 Expiration Date: {expiration_date}**")
                await message.reply(response_text)
                return
    if user_id in auth_users:
        await message.reply("YOU HAVE LIFETIME ACCESS :)")
    else:
        await message.reply("No subscription data found for you.")

@bot.on_message(filters.command("stop"))
async def stop_handler(_, m):
    global processing_request
    if failed_links:
        error_file_send = await m.reply_text("**📤 Sending you Failed Downloads List Before Stopping **")
        with open("failed_downloads.txt", "w") as f:
            for link in failed_links:
                f.write(link + "\n")
        await m.reply_document(document="failed_downloads.txt", caption=fail_cap)
        await error_file_send.delete()
        os.remove('failed_downloads.txt')
        failed_links.clear()
    processing_request = False
    await m.reply_text("🚦**STOPPED**🚦", True)
    os.execl(sys.executable, sys.executable, *sys.argv)

@bot.on_message(filters.command("restart"))
async def restart_handler(_, m):
    global processing_request
    processing_request = False
    await m.reply_text("🤖**Restarting Bot **🤖", True)
    os.execl(sys.executable, sys.executable, *sys.argv)

@bot.on_message(filters.command(["drm"]))
async def account_login(bot: Client, m: Message):
    global processing_request
    if m.from_user.id not in auth_users:
        await m.reply_text("**YOU ARE NOT IN ADMIN LIST**", reply_markup=keyboard)
        return

    if processing_request:
        await m.reply_text("**🫨 I'm currently processing another request.\nPlease try again later.**", reply_markup=Busy)
        return

    editable = await m.reply_text("**➠ Send Me Your TXT File in a Proper Way\n\n➠ TXT FORMAT: LINK: URL**")
    input: Message = await bot.listen(editable.chat.id)
    editable = await editable.edit("**⚙️PROCESSING INPUT.......**")

    if input.document:
        processing_request = True
        x = await input.download()
        await input.delete()
        file_name, ext = os.path.splitext(os.path.basename(x))
        credit = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
        path = f"./downloads/{m.chat.id}"

        try:
            links = []
            videocount = 0
            pdfcount = 0
            with open(x, "r", encoding="utf-8") as f:
                for line in f:
                    link = line.strip().split("://", 1)
                    links.append(link)
                    if ".pdf" in link[1]:
                        pdfcount += 1
                    else:
                        videocount += 1
        except Exception as e:
            await m.reply_text("Error occurred while processing the file.🥲")
            os.remove(x)
            processing_request = False
            return

    else:
        content = input.text
        content = content.split("\n")
        links = []
        videocount = 0
        pdfcount = 0

        for i in content:
            link = i.split("://", 1)
            links.append(link)
            if ".pdf" in link[1]:
                pdfcount += 1
            else:
                videocount += 1

    await editable.edit(f"**Total links found are: {len(links)}\n┃\n┠ Total Video Count: {videocount}\n┠ Total Pdf Count: {pdfcount}\n┠ Send From where you want to download initially: **")
    input0: Message = await bot.listen(editable.chat.id)
    raw_text = input0.text
    await input0.delete()
    if raw_text.lower() == "stop":
        await editable.edit(f"**Task Stopped!**")
        await input0.delete()
        processing_request = False
        os.remove(x)
        return

    await editable.edit(f"**ENTER TILL WHERE YOU WANT TO DOWNLOAD\n┃\n┠ Starting Download From: `{raw_text}`\n┖ Last Index Of Links is: `{len(links)}` **")
    input9: Message = await bot.listen(editable.chat.id)
    raw_text9 = input9.text

    if int(input9.text) > len(links):
        await editable.edit(f"**PLEASE ENTER NUMBER IN RANGE OF INDEX COUNT**")
        processing_request = False
        await m.reply_text("**Exiting Task......**")
        return
    else:
        await input9.delete()

    await editable.edit("**Enter Batch Name or send 'd' for grabbing from text filename.**")
    input1: Message = await bot.listen(editable.chat.id)
    raw_text0 = input1.text
    await input1.delete()
    b_name = file_name if raw_text0 == 'd' else raw_text0

    await editable.edit("**Enter resolution\nSEND 1 for 720p\n2 for 480\n3 for 360\n4 for 240**")
    input2: Message = await bot.listen(editable.chat.id)
    raw_text2 = input2.text
    quality = input2.text
    await input2.delete()

    await editable.edit("**Enter Your Name or send 'de' for use default**")
    input3: Message = await bot.listen(editable.chat.id)
    raw_text3 = input3.text
    await input3.delete()
    CR = "@AllCourseADMIN_BOT" if raw_text3 == 'de' else raw_text3

    await editable.edit("**🖼 Thumbnail\n\n• Custom Thumbnail: Use @AllCourseADMIN_BOT and send me link\n• If you don't want Send: 'no' **")
    input6 = message = await bot.listen(editable.chat.id)
    raw_text6 = input6.text
    await input6.delete()
    thumb = input6.text
    thumb2 = input6.text

    await editable.edit("**⚡️ Thumbnail in PDF too?\n\n• If need same thumb on pdf as video send: 'yes'\nNOTE: if you have given thumb for Video then only use this\n• SEND 'no' If you don't want**")
    input7 = message = await bot.listen(editable.chat.id)
    raw_text7 = input7.text.lower()
    await input7.delete()

    if raw_text7 == "custom":
        await editable.edit("**Send URL of Pdf Thumbnail**")
        input8 = message = await bot.listen(editable.chat.id)
        raw_text8 = input8.text.lower()
        await input8.delete()
        thumb3 = input8.text
    else:
        await editable.delete()

    if thumb.startswith("http://") or thumb.startswith("https://"):
        getstatusoutput(f"wget {thumb} -O thumb1.jpg")
        thumb = "thumb1.jpg"
    else:
        thumb = "no"

    count = 1 if len(links) == 1 else int(raw_text)

    try:
        for i in range(len(links)):
            original_url = links[i][1]
            V = (
                links[i][1]
                .replace("file/d/", "uc?export=download&id=")
                .replace("www.youtube-nocookie.com/embed", "youtu.be")
                .replace("?modestbranding=1", "")
                .replace("/view?usp=sharing", "")
                .replace("mpd", "m3u8")
                .replace("youtube.com/embed/", "youtube.com/watch?v=")
            )
            url = "https://" + V

            if "acecwply" in url:
                cmd = f'yt-dlp -o "{name}.%(ext)s" -f "bestvideo[height<={raw_text2}]+bestaudio" --hls-prefer-ffmpeg --no-keep-video --remux-video mkv --no-warning "{url}"'

            if "visionias" in url:
                async with ClientSession() as session:
                    async with session.get(url, headers={'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'}) as resp:
                        text = await resp.text()
                        url = re.search(r"(https://.*?playlist.m3u8.*?)\"", text).group(1)

            elif 'videos.classplusapp' in url:
                url = requests.get(f'https://api.classplusapp.com/cams/uploader/video/jw-signed-url?url={url}', headers={'x-access-token': 'token'}).text

            if "/master.mpd" in url:
                vid_id = url.split("/")[-2]
                url = f"https://madxpw-api-e0913deb3016.herokuapp.com/{vid_id}/master.m3u8?token="

            name1 = links[i][0].replace("\t", "").replace(":", "").replace("/", "").replace("+", "").replace("#", "").replace("|", "").replace("@", "").replace("*", "").replace(".", "").replace("https", "")
            name = f'{str(count).zfill(3)}) {name1[:60]}'

            if "/master.mpd" in url and "https://sec1.pw.live/" in url:
                url = url.replace("https://sec1.pw.live/", "https://d1d34p8vz63oiq.cloudfront.net/")
                key = await helper.get_drm_keys(url)
                await m.reply_text(f"got keys from api : \n`{key}`")
                cmd = f" yt-dlp -k --allow-unplayable-formats -f bestvideo.{quality} --fixup never {url} "

            if "edge.api.brightcove.com" in url:
                bcov = 'bcov_auth=token'
                url = url.split("bcov_auth")[0] + bcov

            if "youtu" in url:
                ytf = f"b[height<={raw_text2}][ext=mp4]/bv[height<={raw_text2}][ext=mp4]+ba[ext=m4a]/b[ext=mp4]"
            else:
                ytf = f"b[height<={raw_text2}]/bv[height<={raw_text2}]+ba/b/bv+ba"

            if "jw-prod" in url:
                cmd = f'yt-dlp -o "{name}.mp4" "{url}"'

            elif "youtube.com" in url or "youtu.be" in url:
    
else:
    cmd = f'yt-dlp -f "{ytf}" "{url}" -o "{name}.mp4"'

if "m3u8" or "livestream" in url:
    cmd = f'yt-dlp -f "{ytf}" --no-keep-video --remux-video mkv "{url}" -o "romeo.mp4"'

try:
    cc = (f'**🎥 VIDEO ID: {str(count).zfill(3)}.\n\n📄 Title: {name1} {res} 🥀 NIKHIL.mkv\n\n'
          f'<pre><code>🔖 Batch Name: {b_name}</code></pre>\n\n📥 Extracted By : {CR}**')
    cc1 = (f'**📁 FILE ID: {str(count).zfill(3)}.\n\n📄 Title: {name1} SAINI.pdf \n\n'
           f'<pre><code>🔖 Batch Name: {b_name}</code></pre>\n\n📥 Extracted By : {CR}**')

    if "drive" in url:
        ka = await helper.download(url, name)
        await bot.send_document(chat_id=m.chat.id, document=ka, caption=cc1)
        count += 1
        os.remove(ka)
        time.sleep(1)

    elif ".pdf" in url:
        try:
            time.sleep(1)
            cmd = f'yt-dlp -o "{name}.pdf" "{url}"'
            download_cmd = f"{cmd} -R 25 --fragment-retries 25"
            os.system(download_cmd)
            time.sleep(1)
            start_time = time.time()
            reply = await m.reply_text(f"**⚡️ Starting Uploading ...** - `{name}`")
            time.sleep(1)
            if raw_text7 == "custom":
                subprocess.run(['wget', thumb3, '-O', 'pdfthumb.jpg'], check=True)
                thumbnail = "pdfthumb.jpg"
                copy = await bot.send_document(chat_id=m.chat.id, document=f'{name}.pdf', caption=cc1, thumb=thumbnail, progress=progress_bar, progress_args=(reply, start_time))
                os.remove(thumbnail)
            elif thumb == "no" and raw_text7 == "no":
                copy = await bot.send_document(chat_id=m.chat.id, document=f'{name}.pdf', caption=cc1, progress=progress_bar, progress_args=(reply, start_time))
            elif raw_text7 == "yes" and thumb != "no":
                subprocess.run(['wget', thumb2, '-O', 'thumb1.jpg'], check=True)
                thumbnail = "thumb1.jpg"
                copy = await bot.send_document(chat_id=m.chat.id, document=f'{name}.pdf', caption=cc1, thumb=thumbnail, progress=progress_bar, progress_args=(reply, start_time))
            else:
                subprocess.run(['wget', thumb2, '-O', 'thumb1.jpg'], check=True)
                thumbnail = "thumb1.jpg"
                copy = await bot.send_document(chat_id=m.chat.id, document=f'{name}.pdf', caption=cc1, thumb=thumbnail, progress=progress_bar, progress_args=(reply, start_time))
            await reply.delete()
            os.remove(f'{name}.pdf')
            count += 1
            time.sleep(2)
        except FloodWait as e:
            time.sleep(e.x)
            continue

    else:
        prog = await m.reply_text(f"📥 **Downloading **\n\n**➭ Count » {str(count).zfill(3)} **\n**➭ Video Name » ** `{name}`\n**➭ Quality** » `{raw_text2}`\n**➭ Video Url »*[...]")
        time.sleep(2)
        res_file = await helper.drm_download_video(url, quality, name, key)
        filename = res_file
        await prog.delete()
        time.sleep(1)
        await helper.send_vid(bot, m, cc, filename, thumb, name, thumb2)
        count += 1

except Exception as e:
    await m.reply_text(f"**This #Failed File is not Counted**\n**Name** =>> `{name1}`\n**Link** =>> `{url}`\n\n ** Fail reason »** {e}")
    failed_links.append(f"{name1} : {url}")
    count += 1
    continue

if failed_links:
    error_file_send = await m.reply_text("**📤 Sending you Failed Downloads List **")
    with open("failed_downloads.txt", "w") as f:
        for link in failed_links:
            f.write(link + "\n")
    await m.reply_document(document="failed_downloads.txt", caption=fail_cap)
    await error_file_send.delete()
    failed_links.clear()
    os.remove('failed_downloads.txt')
await m.reply_text("🔰Done🔰")
await m.reply_text("**✨Thanks for Choosing**")
processing_request = False

processing_request = False
bot.run()
