from pyrogram import filters, enums
from pyrogram.errors.exceptions.bad_request_400 import (
    ChatAdminRequired,
    UserAdminInvalid,
    BadRequest
)
import requests
from CUTEXMUSIC import app
import datetime
import random 
from pyrogram.errors import UserNotParticipant
from config import LOG_GROUP_ID, OWNER_ID
from pyrogram.types import *



BANIMG = [
    "https://telegra.ph/file/3c6582c8dfd23c2f2b1f8.jpg",
    "https://telegra.ph/file/abe5304508cdb952cb546.jpg",
    "https://telegra.ph/file/e1de039e0130450a238a6.jpg",
]

def mention(user, name, mention=True):
    if mention:
        link = f"[{name}](tg://openmessage?user_id={user})"
    else:
        link = f"[{name}](https://t.me/{user})"
    return link

async def get_userid_from_username(username):
    try:
        user = await app.get_users(username)
    except:
        return None

    user_obj = [user.id, user.first_name]
    return user_obj

async def ban_user(user_id, first_name, admin_id, admin_name, chat_id, reason, message, time=None):
    if user_id == 6844821478:
        msg_text = "sᴏʀʀʏ I Cᴀɴ'ᴛ ʙᴀɴ Mʏ Cᴜᴛᴇsᴛ Oᴡɴᴇʀ... 😒"
        return msg_text, False
    try:
        # Check if the user is currently a member of the group
        member = await app.get_chat_member(chat_id, user_id)
        # Check if the user is already banned in the group
        if member.status == enums.ChatMemberStatus.BANNED:
            return "ɪ ᴛʜɪɴᴋ ᴛʜɪs ᴜsᴇʀ ɪs ᴀʟʀᴇᴀᴅʏ ʙᴀɴɴᴇᴅ ʜᴇʀᴇ 👀.", False

        await app.ban_chat_member(chat_id, user_id)
        
        # Insert banned user into the database
        
        url = "https://api.waifu.pics/sfw/kick"
        user_mention = mention(user_id, first_name)
        admin_mention = mention(admin_id, admin_name)
        button = [
            [
                InlineKeyboardButton(
                    text="• ᴜɴʙᴀɴ •",    
                    callback_data=f"unban_={user_id}",
                ),
                InlineKeyboardButton(
                    text="• ᴅᴇʟᴇᴛᴇ •",
                    callback_data=f"close",
                ),
            ]
        ]
        response = requests.get(url).json()
        pimg = response['url']
        await app.send_message(LOG_GROUP_ID, f"{user_mention} Bᴀɴɴᴇᴅ Bʏ {admin_mention} in {message.chat.title}")
        YEAHHHH = await message.reply_video(
            pimg,
            caption=f"<u>{message.chat.title} Bᴀɴ Eᴠᴇɴᴛ🚫 </u> \n\n ɴᴀᴍᴇ - {user_mention}\n Bᴀɴɴᴇᴅ Bʏ - {admin_mention}\n",
            reply_markup=InlineKeyboardMarkup(button)
        )

        if reason:
            YEAHHHH += f"Reason: `{reason}`\n"
        if time:
            YEAHHHH += f"Time: `{time}`\n"

        return YEAHHHH, True
    except ChatAdminRequired:
        msg_text = "Gɪᴠᴇ Mᴇ Bᴀɴ Rɪɢʜᴛs Fɪʀsᴛ Tʜᴇɴ Usᴇ Iᴛ 😑 "
        return msg_text, False
    except UserAdminInvalid:
        msg_text = "I ᴄᴀɴᴛ ʙᴀɴ ᴍʏ ʙᴇsᴛɪᴇs "
        return msg_text, False
    except UserNotParticipant:
        msg = "ᴛʜɪs ᴜsᴇʀ ɪs ɴᴏᴛ ᴀ ᴘᴀʀᴛɪᴄɪᴘᴀɴᴛ ʜᴇʀᴇ "
        return msg, False
    except Exception as e:
        msg_text = f"ᴀɴ ᴇʀʀᴏʀ ᴏᴄᴄᴜʀʀᴇᴅ\n{e}"
        await app.send_message(LOG_GROUP_ID, f"An error Occurred in Ban - {e}")
        return msg_text, False

@app.on_message(filters.command(["unban"]))
async def unban_command_handler(client, message):
    chat = message.chat
    chat_id = chat.id
    admin_id = message.from_user.id
    admin_name = message.from_user.first_name
    member = await chat.get_member(admin_id)
    if member.status not in [enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER]:
        msg_text = "ᴍʏ ᴍᴀsᴛᴇʀ ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴘᴇʀᴍɪssɪᴏɴ ᴛᴏ Uɴʙᴀɴ Sᴏᴍᴇᴏɴᴇ ✨"
        return await message.reply_text(msg_text)

    if len(message.command) > 1:
        try:
            user_id = int(message.command[1])
            first_name = "User"
        except ValueError:
            user_obj = await get_userid_from_username(message.command[1])
            if user_obj is None:
                return await message.reply_text("ɪ ᴅɪᴅɴ'ᴛ ғɪɴᴅ ᴛʜᴀᴛ ᴜsᴇʀ 👀")
            user_id, first_name = user_obj
    elif message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        first_name = message.reply_to_message.from_user.first_name
    else:
        await message.reply_text("ᴍʏ ᴄᴜᴛᴇ ᴍᴀsᴛᴇʀ sᴘᴇᴄɪғʏ ᴀ ᴠᴀʟɪᴅ ᴜsᴇʀ ᴏʀ ʀᴇᴘʟʏ ᴡɪᴛʜ ᴛʜᴀᴛ ᴜsᴇʀs ᴍᴇssᴀɢᴇ")
        return

    

    msg_text, result = await unban_user(user_id, first_name, admin_id, admin_name, chat_id, message)
    if result:
        await message.reply_text(msg_text)
    else:
        await message.reply_text("Failed to unban the user.")

@app.on_message(filters.command(["ban"]))
async def ban_command_handler(client, message):
    chat = message.chat
    chat_id = chat.id
    admin_id = message.from_user.id
    admin_name = message.from_user.first_name
    member = await chat.get_member(admin_id)
    if member.status == enums.ChatMemberStatus.ADMINISTRATOR or member.status == enums.ChatMemberStatus.OWNER:
        if member.privileges.can_restrict_members:
            pass
        else:
            msg_text = "ᴍʏ ᴄᴜᴛᴇ ᴍᴀꜱᴛᴇʀ ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴘᴇʀᴍɪꜱꜱɪᴏɴ ᴛᴏ ʙᴀɴ ꜱᴏᴍᴇᴏɴᴇ 🪔"
            return await message.reply_text(msg_text)
    else:
        msg_text = "ᴍʏ ᴄᴜᴛᴇ ᴍᴀꜱᴛᴇʀ ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴘᴇʀᴍɪꜱꜱɪᴏɴ ᴛᴏ ʙᴀɴ ꜱᴏᴍᴇᴏɴᴇ 💓"
        return await message.reply_text(msg_text)

    # user id lelo reply se 
    if len(message.command) > 1:
        if message.reply_to_message:
            user_id = message.reply_to_message.from_user.id
            first_name = message.reply_to_message.from_user.first_name
            reason = message.text.split(None, 1)[1]
        else:
            try:
                user_id = int(message.command[1])
                first_name = "User"
            except:
                user_obj = await get_userid_from_username(message.command[1])
                if user_obj == None:
                    return await message.reply_text("ɪ ᴅɪᴅɴ'ᴛ ꜰɪɴᴅ ᴛʜᴀᴛ ᴜꜱᴇʀ 🤨")
                user_id = user_obj[0]
                first_name = user_obj[1]

            try:
                reason = message.text.partition(message.command[1])[2]
            except:
                reason = None

    elif message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        first_name = message.reply_to_message.from_user.first_name
        reason = None
    else:
        await message.reply_text("ᴍʏ ᴄᴜᴛᴇ ᴍᴀsᴛᴇʀ sᴘᴇᴄɪғʏ ᴀ ᴠᴀʟɪᴅ ᴜsᴇʀ ᴏʀ ʀᴇᴘʟʏ ᴡɪᴛʜ ᴛʜᴀᴛ ᴜsᴇʀs ᴍᴇssᴀɢᴇ ❄️")
        return

    
    msg_text, result = await ban_user(user_id, first_name, admin_id, admin_name, chat_id, reason, message)
    if result == False:
        await message.reply_text(msg_text)

# unban callback function he bro
@app.on_callback_query(filters.regex("^unban_"))
async def unbanbutton(c: app, q: CallbackQuery):
    splitter = (str(q.data).replace("unban_", "")).split("=")
    user_id = int(splitter[1])
    user = await q.message.chat.get_member(q.from_user.id)

    if not user:
        await q.answer(
            "ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴇɴᴏᴜɢʜ ʀɪɢʜᴛꜱ ᴛᴏ ᴅᴏ ᴛʜɪꜱ ꜱᴛᴀʏ ɪɴ ʏᴏᴜʀ ʟɪᴍɪᴛꜱ 🤨",
            show_alert=True,
        )
        return

    if not user.privileges.can_restrict_members and q.from_user.id != OWNER_ID:
        await q.answer(
            "ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴇɴᴏᴜɢʜ ʀɪɢʜᴛꜱ ᴛᴏ ᴅᴏ ᴛʜɪꜱ ꜱᴛᴀʏ ɪɴ ʏᴏᴜʀ ʟɪᴍɪᴛꜱ ✨",
            show_alert=True,
        )
        return
    
    whoo = await c.get_chat(user_id)
    doneto = whoo.first_name if whoo.first_name else whoo.title
    
    try:
        await q.message.chat.unban_member(user_id)
    except RPCError as e:
        await q.message.edit_text(f"Error: {e}")
        return
    
    button = [
        [
            InlineKeyboardButton(
                text="Sᴜᴍᴍᴏɴ ᴍᴇ ",     
                url=f"https://t.me/CuteXMusicBot?startgroup=true",
            ),
            InlineKeyboardButton(
                text=" ᴅᴇʟᴇᴛᴇ ",
                callback_data=f"close",
            ),
        ]
    ]
    
    await q.message.edit_text(
        f"Uɴʙᴀɴ Eᴠᴇɴᴛ \n\n ɴᴀᴍᴇ - {doneto} \n Uɴʙᴀɴ Bʏ {q.from_user.mention}",
        reply_markup=InlineKeyboardMarkup(button)
    )
    return

