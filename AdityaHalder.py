import aiohttp, aiofiles, asyncio, base64, logging
import os, platform, random, re, socket
import sys, time, textwrap

from os import getenv
from io import BytesIO
from time import strftime
from functools import partial
from dotenv import load_dotenv
from datetime import datetime
from typing import Union, List, Pattern
from logging.handlers import RotatingFileHandler


from git import Repo
from git.exc import GitCommandError, InvalidGitRepositoryError
from motor.motor_asyncio import AsyncIOMotorClient as _mongo_async_

from pyrogram import Client, filters as pyrofl
from pytgcalls import PyTgCalls, filters as pytgfl


from pyrogram import idle, __version__ as pyro_version
from pytgcalls.__version__ import __version__ as pytgcalls_version

from ntgcalls import TelegramServerError
from pyrogram.enums import ChatMemberStatus, ChatType
from pyrogram.errors import (
    ChatAdminRequired,
    FloodWait,
    InviteRequestSent,
    UserAlreadyParticipant,
    UserNotParticipant,
)
from pytgcalls.exceptions import NoActiveGroupCall
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pytgcalls.types import ChatUpdate, Update, GroupCallConfig
from pytgcalls.types import Call, MediaStream, AudioQuality, VideoQuality

from PIL import Image, ImageDraw, ImageEnhance
from PIL import ImageFilter, ImageFont, ImageOps
from youtubesearchpython.__future__ import VideosSearch


loop = asyncio.get_event_loop()


# versions dictionary
__version__ = {
    "AP": "1.0.0 Mini",
    "Python": platform.python_version(),
    "Pyrogram": pyro_version,
    "PyTgCalls": pytgcalls_version,
}


# store all logs
logging.basicConfig(
    format="[%(name)s]:: %(message)s",
    level=logging.INFO,
    datefmt="%H:%M:%S",
    handlers=[
        RotatingFileHandler("logs.txt", maxBytes=(1024 * 1024 * 5), backupCount=10),
        logging.StreamHandler(),
    ],
)

logging.getLogger("apscheduler").setLevel(logging.ERROR)
logging.getLogger("asyncio").setLevel(logging.ERROR)
logging.getLogger("httpx").setLevel(logging.ERROR)
logging.getLogger("pyrogram").setLevel(logging.ERROR)
logging.getLogger("pytgcalls").setLevel(logging.ERROR)

LOGGER = logging.getLogger("SYSTEM")


# config variables
if os.path.exists("Config.env"):
    load_dotenv("Config.env")

API_ID = int(getenv("API_ID", 0))
API_HASH = getenv("API_HASH", None)
BOT_TOKEN = getenv("BOT_TOKEN", None)
STRING_SESSION = getenv("STRING_SESSION", None)
MONGO_DB_URL = getenv("MONGO_DB_URL", None)
OWNER_ID = int(getenv("OWNER_ID", 0))
LOG_GROUP_ID = int(getenv("LOG_GROUP_ID", 0))
START_IMAGE_URL = getenv("START_IMAGE_URL", None)


# Memory Database

ACTIVE_AUDIO_CHATS = []
ACTIVE_VIDEO_CHATS = []
ACTIVE_MEDIA_CHATS = []

QUEUE = {}


# Command & Callback Handlers


def cdx(commands: Union[str, List[str]]):
    return pyrofl.command(commands, ["/", "!", "."])


def cdz(commands: Union[str, List[str]]):
    return pyrofl.command(commands, ["", "/", "!", "."])


def rgx(pattern: Union[str, Pattern]):
    return pyrofl.regex(pattern)


bot_owner_only = pyrofl.user(OWNER_ID)


# all clients

app = Client(
    name="App",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=str(STRING_SESSION),
)

bot = Client(
    name="Bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
)

call = PyTgCalls(app)
call_config = GroupCallConfig(auto_start=False)

mongo_async_cli = _mongo_async_(MONGO_DB_URL)
mongodb = mongo_async_cli.adityaxdb

# store start time
__start_time__ = time.time()


# start and run


async def main():
    LOGGER.info("🐬 Updating Directories ...")
    if "cache" not in os.listdir():
        os.mkdir("cache")
    if "cookies.txt" not in os.listdir():
        LOGGER.info("⚠️ 'cookies.txt' - Not Found❗")
        sys.exit()
    if "downloads" not in os.listdir():
        os.mkdir("downloads")
    for file in os.listdir():
        if file.endswith(".session"):
            os.remove(file)
    for file in os.listdir():
        if file.endswith(".session-journal"):
            os.remove(file)
    LOGGER.info("✅ All Directories Updated.")
    await asyncio.sleep(1)
    LOGGER.info("🌐 Checking Required Variables ...")
    if API_ID == 0:
        LOGGER.info("❌ 'API_ID' - Not Found ‼️")
        sys.exit()
    if not API_HASH:
        LOGGER.info("❌ 'API_HASH' - Not Found ‼️")
        sys.exit()
    if not BOT_TOKEN:
        LOGGER.info("❌ 'BOT_TOKEN' - Not Found ‼️")
        sys.exit()
    if not STRING_SESSION:
        LOGGER.info("❌ 'STRING_SESSION' - Not Found ‼️")
        sys.exit()

    if not MONGO_DB_URL:
        LOGGER.info("'MONGO_DB_URL' - Not Found !!")
        sys.exit()
    try:
        await mongo_async_cli.admin.command('ping')
    except Exception:
        LOGGER.info("❌ 'MONGO_DB_URL' - Not Valid !!")
        sys.exit()
    LOGGER.info("✅ Required Variables Are Collected.")
    await asyncio.sleep(1)
    LOGGER.info("🌀 Starting All Clients ...")
    try:
        await bot.start()
    except Exception as e:
        LOGGER.info(f"🚫 Bot Error: {e}")
        sys.exit()
    if LOG_GROUP_ID != 0:
        try:
            await bot.send_message(LOG_GROUP_ID, "**🤖 Bot Started.**")
        except Exception:
            pass
    LOGGER.info("✅ Bot Started.")
    try:
        await app.start()
    except Exception as e:
        LOGGER.info(f"🚫 Assistant Error: {e}")
        sys.exit()
    try:
        await app.join_chat("MEETUP_ZONE")
        await app.join_chat("ABOUT_ARTHIK")
    except Exception:
        pass
    if LOG_GROUP_ID != 0:
        try:
            await app.send_message(LOG_GROUP_ID, "**🦋 Assistant Started.**")
        except Exception:
            pass
    LOGGER.info("✅ Assistant Started.")
    try:
        await call.start()
    except Exception as e:
        LOGGER.info(f"🚫 PyTgCalls Error: {e}")
        sys.exit()
    LOGGER.info("✅ PyTgCalls Started.")
    await asyncio.sleep(1)
    LOGGER.info("✅ Sucessfully Hosted Your Bot !!")
    LOGGER.info("✅ Now Do Visit: @ABOUT_ARTHIK !!")
    await idle()









# Some Required Functions ...!!


def _netcat(host, port, content):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    s.sendall(content.encode())
    s.shutdown(socket.SHUT_WR)
    while True:
        data = s.recv(4096).decode("utf-8").strip("\n\x00")
        if not data:
            break
        return data
    s.close()


async def paste_queue(content):
    loop = asyncio.get_running_loop()
    link = await loop.run_in_executor(None, partial(_netcat, "ezup.dev", 9999, content))
    return link



def get_readable_time(seconds: int) -> str:
    count = 0
    ping_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]
    while count < 4:
        count += 1
        if count < 3:
            remainder, result = divmod(seconds, 60)
        else:
            remainder, result = divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)
    for i in range(len(time_list)):
        time_list[i] = str(time_list[i]) + time_suffix_list[i]
    if len(time_list) == 4:
        ping_time += time_list.pop() + ", "
    time_list.reverse()
    ping_time += ":".join(time_list)
    return ping_time





# Mongo Database Functions

chatsdb = mongodb.chatsdb
usersdb = mongodb.usersdb




# Served Chats

async def is_served_chat(chat_id: int) -> bool:
    chat = await chatsdb.find_one({"chat_id": chat_id})
    if not chat:
        return False
    return True


async def get_served_chats() -> list:
    chats_list = []
    async for chat in chatsdb.find({"chat_id": {"$lt": 0}}):
        chats_list.append(chat)
    return chats_list


async def add_served_chat(chat_id: int):
    is_served = await is_served_chat(chat_id)
    if is_served:
        return
    return await chatsdb.insert_one({"chat_id": chat_id})



# Served Users

async def is_served_user(user_id: int) -> bool:
    user = await usersdb.find_one({"user_id": user_id})
    if not user:
        return False
    return True


async def get_served_users() -> list:
    users_list = []
    async for user in usersdb.find({"user_id": {"$gt": 0}}):
        users_list.append(user)
    return users_list


async def add_served_user(user_id: int):
    is_served = await is_served_user(user_id)
    if is_served:
        return
    return await usersdb.insert_one({"user_id": user_id})













# Callback & Message Queries


@bot.on_message(cdx(["start", "help"]) & pyrofl.private)
async def start_message_private(client, message):
    user_id = message.from_user.id
    mention = message.from_user.mention
    await add_served_user(user_id)
    if len(message.text.split()) > 1:
        name = message.text.split(None, 1)[1]
        if name[0:5] == "verify":
            pass
            
    else:
        caption = f"""**➻ Hello, {mention}

🥀 I am An ≽ Advanced ≽ High Quality
Bot, I Can Stream 🌿 Audio & Video In
Your ♚ Channel And Group.

🐬 Must Click ❥ Open Command List
Button ⋟ To Get More Info's 🦋 About
My All Commands.

💐 Feel Free ≽ To Use Me › And Share
With Your ☛ Other Friends.**"""
        buttons = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="🥀 Add Me In Your Chat ✨",
                        url=f"https://t.me/{bot.me.username}?startgroup=true",
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="🌺 Open Command List 🌷",
                        callback_data="open_command_list",
                    )
                ],
            ]
        )
        if START_IMAGE_URL:
            try:
                return await message.reply_photo(
                    photo=START_IMAGE_URL, caption=caption, reply_markup=buttons
                )
            except Exception as e:
                LOGGER.info(f"🚫 Start Image Error: {e}")
                try:
                    return await message.reply_text(text=caption, reply_markup=buttons)
                except Exception as e:
                    LOGGER.info(f"🚫 Start Error: {e}")
                    return
        else:
            try:
                return await message.reply_text(text=caption, reply_markup=buttons)
            except Exception as e:
                LOGGER.info(f"🚫 Start Error: {e}")
                return




@bot.on_callback_query(rgx("open_command_list"))
async def open_command_list_alert(client, query):
    caption = """**🥀 All Members Can Use:**
/play - Stream Only Audio On VC.
/vplay - Stream Audio With Video.

**👾 Only For Chat Admins:**
/pause - Pause Running Stream.
/resume - Resume Paused Stream.
/skip - Skip Current Stream To Next.
/end - Stop Current Running Stream.

**Note:** All Commands Will Work
Only in Channels/Groups."""
    buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="🔙 Back",
                    callback_data="back_to_home",
                )
            ],
        ]
    )
    try:
        return await query.edit_message_text(text=caption, reply_markup=buttons)
    except Exception as e:
        LOGGER.info(f"🚫 Cmd Menu Error: {e}")
        return


@bot.on_callback_query(rgx("back_to_home"))
async def back_to_home_menu(client, query):
    mention = query.from_user.mention
    caption = f"""**➻ Hello, {mention}

🥀 I am An ≽ Advanced ≽ High Quality
Bot, I Can Stream 🌿 Audio & Video In
Your ♚ Channel And Group.

🐬 Must Click ❥ Open Command List
Button ⋟ To Get More Info's 🦋 About
My All Commands.

💐 Feel Free ≽ To Use Me › And Share
With Your ☛ Other Friends.**"""
    buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="🥀 Add Me In Your Chat ✨",
                    url=f"https://t.me/{bot.me.username}?startgroup=true",
                )
            ],
            [
                InlineKeyboardButton(
                    text="🌺 Open Command List 🌷",
                    callback_data="open_command_list",
                )
            ],
        ]
    )
    try:
        return await query.edit_message_text(text=caption, reply_markup=buttons)
    except Exception as e:
        LOGGER.info(f"🚫 Back Menu Error: {e}")
        return


@bot.on_callback_query(rgx("force_close"))
async def delete_cb_query(client, query):
    try:
        return await query.message.delete()
    except Exception:
        return


# Thumbnail Generator Area


async def download_thumbnail(vidid: str):
    async with aiohttp.ClientSession() as session:
        links = [
            f"https://i.ytimg.com/vi/{vidid}/maxresdefault.jpg",
            f"https://i.ytimg.com/vi/{vidid}/sddefault.jpg",
            f"https://i.ytimg.com/vi/{vidid}/hqdefault.jpg",
            START_IMAGE_URL,
        ]
        thumbnail = f"cache/temp_{vidid}.png"
        for url in links:
            async with session.get(url) as resp:
                if resp.status != 200:
                    continue
                else:
                    f = await aiofiles.open(thumbnail, mode="wb")
                    await f.write(await resp.read())
                    await f.close()
                    return thumbnail


async def get_user_logo(user_id):
    try:
        user_chat = await bot.get_chat(user_id)
        userimage = user_chat.photo.big_file_id
        user_logo = await bot.download_media(userimage, f"cache/{user_id}.png")
    except:
        user_chat = await bot.get_me()
        userimage = user_chat.photo.big_file_id
        user_logo = await bot.download_media(userimage, f"cache/{bot.id}.png")
    return user_logo


def changeImageSize(maxWidth, maxHeight, image):
    widthRatio = maxWidth / image.size[0]
    heightRatio = maxHeight / image.size[1]
    newWidth = int(widthRatio * image.size[0])
    newHeight = int(heightRatio * image.size[1])
    newImage = image.resize((newWidth, newHeight))
    return newImage


def circle_image(image, size):
    size = (size, size)
    mask = Image.new("L", size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + size, fill=255)
    output = ImageOps.fit(image, mask.size, centering=(0.5, 0.5))
    output.putalpha(mask)
    return output


def random_color_generator():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    return (r, g, b)


async def create_thumbnail(results, user_id):
    if not results:
        return START_IMAGE_URL
    title = results.get("title")
    title = re.sub("\W+", " ", title)
    title = title.title()
    vidid = results.get("id")
    duration = results.get("duration")
    views = results.get("views")
    channel = results.get("channel")
    image = await download_thumbnail(vidid)
    logo = await get_user_logo(user_id)
    image_string = "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
