# Made with python3
# (C) @FayasNoushad
# Copyright permission under MIT License
# All rights reserved by FayasNoushad
# License -> https://github.com/FayasNoushad/Attach-Bot/blob/main/LICENSE

import os
import pyrogram
from pyrogram import Client, filters 
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton 
from telegraph import upload_file

FayasNoushad = Client(
    "Telegram Attach Bot",
    bot_token = os.environ["BOT_TOKEN"],
    api_id = int(os.environ["API_ID"]),
    api_hash = os.environ["API_HASH"],
)

START_TEXT = """
Hello {}, I' am small media or file in a message attach bot.

- Just give me a media under 5MB
- Reply a message to the media

Made by @FayasNoushad
"""

@FayasNoushad.on_message(filters.private & filters.command(["start"]))
async def start(bot, update):
    await bot.send_message(
        chat_id=update.chat.id,
        text=START_TEXT.format(update.from_user.mention),
        parse_mode="html",
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('⚙ Channel ⚙', url='https://telegram.me/FayasNoushad'), InlineKeyboardButton('⚙ Group ⚙', url='https://telegram.me/FayasChat')]]),
        reply_to_message_id=update.message_id
    )

@FayasNoushad.on_message(filters.media & filters.private)
async def attach(bot, update):
    media = "./DOWNLOADS/" + "FayasNoushad/FnAttachBot"
    if update.reply_to_message is None:
        await update.reply_text(text="Reply to a media to get an attached Media")
    else:
        text = await bot.send_message(
            chat_id=update.chat.id,
            text="<code>Downloading to My Server ...</code>",
            parse_mode="html",
            disable_web_page_preview=True,
            reply_to_message_id=update.message_id
        )
        await bot.download_media(message=update.reply_to_message, file_name=media)
        await text.edit_text(text="<code>Downloading Completed. Now I am Uploading...</code>")
        try:
            response = upload_file(media)
        except Exception as error:
            print(error)
            await text.edit_text(text=f"Error :- {error}", disable_web_page_preview=True)
        await text.edit_text(text=f"{update.text} [{\u2063}](https://telegra.ph{response[0]})")
        try:
            os.remove(media)
        except:
            pass 

FayasNoushad.run()
