# Copyright 2021 TerminalWarlord under the terms of the MIT
# license found at https://github.com/TerminalWarlord/TikTok-Downloader-Bot/blob/master/LICENSE
# Encoding = 'utf-8'
# Fork and Deploy, do not modify this repo and claim it yours
# For collaboration mail me at dev.jaybee@gmail.com
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InlineQueryResultArticle, InputTextMessageContent
import shutil
import requests
import json
import os
import re
from bs4 import BeautifulSoup as bs
import time
from datetime import timedelta
import math
import base64
from progress_bar import progress, TimeFormatter, humanbytes
from dotenv import load_dotenv

load_dotenv()
bot_token = os.environ.get('BOTOKEN')
workers = int(os.environ.get('WORKERS'))
api = int(os.environ.get('API_KEY'))
hash = os.environ.get('API_HASH')
chnnl = os.environ.get('CHANNEL_URL')
BOT_URL = os.environ.get('BOT_URL')
app = Client("JayBee", bot_token=bot_token, api_id=api, api_hash=hash, workers=workers)



@app.on_message(filters.command('start'))
def start(client, message):
    kb = [[InlineKeyboardButton('Channel 🛡', url=chnnl),InlineKeyboardButton('Repo 🔰', url="https://github.com/TerminalWarlord/TikTok-Downloader-Bot/")]]
    reply_markup = InlineKeyboardMarkup(kb)
    app.send_message(chat_id=message.from_user.id, text=f"Hello there, I am **TikTok Downloader Bot**.\nI can download TikTok video without Watermark.\n\n"
                          "__**Developer :**__ __@JayBeeDev__\n"
                          "__**Language :**__ __Python__\n"
                          "__**Framework :**__ __🔥 Pyrogram__",
                     parse_mode='md',
                     reply_markup=reply_markup)




@app.on_message(filters.command('help'))
def help(client, message):
    kb = [[InlineKeyboardButton('Channel 🛡', url=chnnl),InlineKeyboardButton('Repo 🔰', url="https://github.com/TerminalWarlord/TikTok-Downloader-Bot/")]]
    reply_markup = InlineKeyboardMarkup(kb)
    app.send_message(chat_id=message.from_user.id, text=f"Hello there, I am **TikTok Downloader Bot**.\nI can download any TikTok video from a given link.\n\n"
                                            "__Send me a TikTok video link__",
                     parse_mode='md',
                     reply_markup=reply_markup)


@app.on_message((filters.regex("http://")|filters.regex("https://")) & (filters.regex('tiktok')|filters.regex('douyin')))
def tiktok_dl(client, message):
    a = app.send_message(chat_id=message.chat.id,
                         text='__Downloading File to the Server__',
                         parse_mode='md')
    link = "https://" + message.text.split("https://")[-1].split("http://")[-1].split(" ")[0]
    link = link.split("?")[0]
    message_bytes = link.encode('ascii')
    base64_bytes = base64.b64encode(message_bytes)
    link = base64_bytes.decode('ascii')
    link = f"https://jaybee-tiktok-dl.vercel.app/{link}"
    r = requests.get(link, timeout=300).json()[0]['mir1']
    directory = str(round(time.time()))
    filename = str(message.chat.id)+'.mp4'
    size = int(requests.head(r).headers['Content-length'])
    total_size = "{:.2f}".format(int(size) / 1048576)
    try:
        os.mkdir(directory)
    except:
        pass
    with requests.get(r, timeout=(50, 10000), stream=True) as r:
        r.raise_for_status()
        with open(f'./{directory}/{filename}', 'wb') as f:
            chunk_size = 1048576
            dl = 0
            show = 1
            for chunk in r.iter_content(chunk_size=chunk_size):
                f.write(chunk)
                dl = dl + chunk_size
                percent = round(dl * 100 / size)
                if percent > 100:
                    percent = 100
                if show == 1:
                    try:
                        a.edit(f'__**URL :**__ __{message.text}__\n'
                               f'__**Total Size :**__ __{total_size} MB__\n'
                               f'__**Downloaded :**__ __{percent}%__\n',
                               disable_web_preview=False)
                    except:
                        pass
                    if percent == 100:
                        show = 0

        a.edit(f'__Downloaded to the server!\n'
               f'Uploading to Telegram Now ⏳__')
        start = time.time()
        title = filename
        app.send_document(chat_id=message.chat.id,
                          document=f"./{directory}/{filename}",
                          caption=f"**File :** __{filename}__\n"
                          f"**Size :** __{total_size} MB__\n\n"
                          f"__Uploaded by @{BOT_URL}__",
                          file_name=f"{directory}",
                          parse_mode='md',
                          progress=progress,
                          progress_args=(a, start, title))
        a.delete()
        try:
            shutil.rmtree(directory)
        except:
            pass


app.run()
