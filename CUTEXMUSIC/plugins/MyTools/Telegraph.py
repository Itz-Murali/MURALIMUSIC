from telegraph import upload_file
from pyrogram import filters
from CUTEXMUSIC import app
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio
from pyrogram.types import InputMediaPhoto

BUTTON = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(text="ADD ME", url="https://t.me/pokemin"),
        InlineKeyboardButton(text="✗ ᴄʟᴏsᴇ ✗", callback_data="close"),
    ],
    ]
)

@app.on_message(filters.command(["tgm", "tl", "telegraph"]))
async def ul(_, message):
    reply = message.reply_to_message
    cutex = message.from_user.mention
    try:
        if reply.media:
            up = await message.reply_sticker("CAACAgUAAx0CbEz78AABAQrnZfLFaeYoGtYnnpz9tjMoS7kguGMAAvsAA2ZVWFYsY40Xw0VjvB4E")
            await asyncio.sleep(0.3)
            await up.delete()
            i = await message.reply_text("Just a second...")
            path = await reply.download()
            fk = upload_file(path)
            for x in fk:
                url = "https://telegra.ph" + x
            await i.edit_text(f"Hey {cutex}\n\nHere is your link:\n`{url}`\nclick to copy 👆", reply_markup=BUTTON)
        if not reply:
            await message.reply("Please reply with a media under 5 MB.")
    except Exception as e:
        await message.reply("Please reply with a media under 5 MB.")
        
###Hello


@app.on_message(filters.command(["graph" , "grf"]))
def ul(_, message):
    reply = message.reply_to_message
    if reply.media:
        i = message.reply("ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ...")
        path = reply.download()
        fk = upload_file(path)
        for x in fk:
            url = "https://graph.org" + x

        i.edit(f'ʜᴇʀᴇ ɪs ʏᴏᴜʀ ʟɪɴᴋ 🔗 {url}')
            
