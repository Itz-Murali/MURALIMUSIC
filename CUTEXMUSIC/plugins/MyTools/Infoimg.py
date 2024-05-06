import os
from PIL import Image, ImageDraw, ImageFont
from pyrogram import Client, filters, enums
from pyrogram.types import Message
from typing import Union, Optional
from CUTEXMUSIC import app
from unidecode import unidecode

# Function to download user's profile picture
async def cute_download_pic(user_id):
    user = await app.get_users(user_id)
    if user.photo:
        file_path = await app.download_media(user.photo.big_file_id)
        return file_path
    else:
        return "assets/NODP.PNG"

# Function to generate user info image
async def get_userinfo_img(user_id, first_name, username):
    bg = Image.open("assets/INFOO.PNG")
    photo_path = await cute_download_pic(user_id)
    img = Image.open(photo_path)
    mask = Image.new("L", img.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.pieslice([(0, 0), img.size], 0, 360, fill=255)

    circular_img = Image.new("RGBA", img.size, (0, 0, 0, 0))
    circular_img.paste(img, (0, 0), mask)
    resized = circular_img.resize((1300, 1300))
    bg.paste(resized, (199, 600), resized)
    
    first_name = unidecode(first_name) if first_name else "None"
    username = unidecode(username) if username else "None"

    draw = ImageDraw.Draw(bg)
    font = ImageFont.truetype('assets/font.ttf', size=160)  
    draw.text((1800, 1680), f"Name : {first_name}", font=font, fill=(255, 255, 255))
    draw.text((1800, 1950), f"ID : {user_id}", font=font, fill=(255, 255, 255))
    draw.text((1800, 2200), f"Username : {username}", font=font, fill=(255, 255, 255))

    path = f"./userinfo_img_{user_id}.png"
    bg.save(path)
    return path

# Function to get user's status
async def userstatus(user_id):
    try:
        user = await app.get_users(user_id)
        x = user.status
        if x == enums.UserStatus.RECENTLY:
            return "User was seen recently."
        elif x == enums.UserStatus.LAST_WEEK:
            return "User was seen last week."
        elif x == enums.UserStatus.LONG_AGO:
            return "User was seen long ago."
        elif x == enums.UserStatus.OFFLINE:
            return "User is offline."
        elif x == enums.UserStatus.ONLINE:
            return "User is online."
    except:
        return "**Something went wrong!**"


INFO_TEXT = """
<u>**ᴜsᴇʀ ɪɴғᴏʀᴍᴀᴛɪᴏɴ**</u>

**Usᴇʀ ɪᴅ** ☞ `{}`
**ɴᴀᴍᴇ** ☞ {}
**ᴜsᴇʀɴᴀᴍᴇ **☞ {}
**ᴍᴇɴᴛɪᴏɴ **☞ {}
**ᴜsᴇʀ sᴛᴀᴛᴜs** ☞ `{}`
**ʙɪᴏ** ☞ {}
"""

# Command to get user information
@app.on_message(filters.command(["info", "information", "userinfo"], prefixes=["/", "!", "%", ",", "", ".", "@", "#"]))
async def userinfo(_, message: Message):
    chat_id = message.chat.id

    # If command is called with user ID
    if not message.reply_to_message and len(message.command) == 2:
        try:
            user_id = message.text.split(None, 1)[1]
            user_info = await app.get_chat(user_id)
            user = await app.get_users(user_id)
            status = await userstatus(user.id)
            id = user_info.id
            dc_id = user.dc_id
            name = user_info.first_name
            username = user_info.username
            mention = user.mention
            bio = user_info.bio or ""
            photo = await app.download_media(user.photo.big_file_id) if user.photo else None
            welcome_photo = await get_userinfo_img(
                user_id=user_id,
                first_name=name,
                username=username
            )
            await app.send_photo(chat_id, photo=welcome_photo, caption=INFO_TEXT.format(
                id, name, username, mention, status, bio), reply_to_message_id=message.id)
            if photo:
                os.remove(photo)
        except Exception as e:
            await message.reply_text(str(e))

    # If command is called without user ID
    elif not message.reply_to_message:
        try:
            user_id = message.from_user.id
            user_info = await app.get_chat(user_id)
            user = await app.get_users(user_id)
            status = await userstatus(user.id)
            id = user_info.id
            dc_id = user.dc_id
            name = user_info.first_name
            username = user_info.username
            mention = user.mention
            bio = user_info.bio or ""
            photo = await cute_download_pic(user_id)
            welcome_photo = await get_userinfo_img(
                user_id=user_id,
                first_name=name,
                username=username
            )
            await app.send_photo(chat_id, photo=welcome_photo, caption=INFO_TEXT.format(
                id, name, username, mention, status, dc_id, bio), reply_to_message_id=message.id)
            if photo:
                os.remove(photo)
        except Exception as e:
            await message.reply_text(str(e))

    # If command is a reply to a message
    elif message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        try:
            user_info = await app.get_chat(user_id)
            user = await app.get_users(user_id)
            status = await userstatus(user.id)
            id = user_info.id
            dc_id = user.dc_id
            name = user_info.first_name
            username = user_info.username
            mention = user.mention
            bio = user_info.bio or ""
            photo = await app.download_media(message.reply_to_message.from_user.photo.big_file_id) if message.reply_to_message.from_user.photo else None
            welcome_photo = await get_userinfo_img(
                user_id=user_id,
                first_name=name,
                username=username
            )
            await app.send_photo(chat_id, photo=welcome_photo, caption=INFO_TEXT.format(
                id, name, username, mention, status, dc_id, bio), reply_to_message_id=message.id)
            if photo:
                os.remove(photo)
        except Exception as e:
            await message.reply_text(str(e))
