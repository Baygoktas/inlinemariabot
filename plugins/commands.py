import os
import logging
import random
import asyncio
from pyrogram.types.messages_and_media.message import Message
from Script import script
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from database.ia_filterdb import Media, get_file_details, unpack_new_file_id
from database.users_chats_db import db
from info import CHANNELS, ADMINS, AUTH_CHANNEL, CUSTOM_FILE_CAPTION, LOG_CHANNEL
from utils import get_size, is_subscribed, temp
import re
logger = logging.getLogger(__name__)

@Client.on_message(filters.command(["start", "help", "h", "y", "yardım", "yardim"]))
#@Client.on_message(filters.command(["start", "help", "h", "y", "yardım", "yardim", f"start@{temp.U_NAME}", f"help@{temp.U_NAME}", f"h@{temp.U_NAME}", f"y@{temp.U_NAME}", f"yardım@{temp.U_NAME}", f"yardim@{temp.U_NAME}"]))
async def start(client:Client, message: Message):
    if AUTH_CHANNEL and not await is_subscribed(client, message):
        return await message.reply_text("Lütfen oku: https://telegra.ph/KitapAraBot-04-16", disable_web_page_preview=True)
    buttons = [
        [
            InlineKeyboardButton('➕ Gruba ekle', url=f'http://t.me/{temp.U_NAME}?startgroup=true'),
            InlineKeyboardButton('🔍 Ara', switch_inline_query_current_chat='')
        ],
        [
            InlineKeyboardButton('🔮 İstatistikler', callback_data='stats'),
            InlineKeyboardButton('😊 Hakkında', callback_data='about')
        ]
        ]
    if message.chat.type in ['group', 'supergroup']:
        reply_markup = InlineKeyboardMarkup(buttons)
        await message.reply(script.START_TXT.format(
            message.from_user.mention if message.from_user else message.chat.title, temp.U_NAME, temp.B_NAME),
            reply_markup=reply_markup, disable_web_page_preview=True)
        await asyncio.sleep(2)
        if not await db.get_chat(message.chat.id):
            total=await client.get_chat_members_count(message.chat.id)
            await client.send_message(LOG_CHANNEL, f"#{temp.U_NAME}\n" +  script.LOG_TEXT_G.format(message.chat.title, message.chat.id, total, "Unknown"))       
            await db.add_chat(message.chat.id, message.chat.title)
        return 
    if not await db.is_user_exist(message.from_user.id):
        await db.add_user(message.from_user.id, message.from_user.first_name)
        await client.send_message(LOG_CHANNEL, f"#{temp.U_NAME}\n" +  script.LOG_TEXT_P.format(message.from_user.id, message.from_user.mention))
    if len(message.command) != 2:
        reply_markup = InlineKeyboardMarkup(buttons)
        return await message.reply_text(text=script.START_TXT.format(message.from_user.mention, temp.U_NAME, temp.B_NAME),
            reply_markup=reply_markup, parse_mode='html', disable_web_page_preview=True)
    
    if len(message.command) == 2 and message.command[1] in ["subscribe", "error", "okay", "help"]:
        reply_markup = InlineKeyboardMarkup(buttons)
        return await message.reply_text(text=script.START_TXT.format(message.from_user.mention, temp.U_NAME, temp.B_NAME),
            reply_markup=reply_markup, parse_mode='html', disable_web_page_preview=True)
    file_id = message.command[1]
    files_ = await get_file_details(file_id)
    if not files_:
        delo = await message.reply("Bulamadım bir şey.\nArama ipuçları için tıkla ve oku: /yardim")
        await asyncio.sleep(10)
        return await delo.delete()
    files = files_[0]
    f_caption=files.caption
    try:
        f_caption = files.caption
        if not f_caption: f_caption = str(files.file_name)
        f_caption += '' if CUSTOM_FILE_CAPTION is None else f'\n{CUSTOM_FILE_CAPTION}'
    except Exception as e:
        logger.exception(e)
        f_caption=f_caption
    await client.send_cached_media(
        chat_id=message.from_user.id,
        file_id=file_id,
        caption=f_caption,
        )
    if not files.file_name: return
    # + 001 gibi arşivse tuto gönder
    if files.file_name and files.file_name.endswith(tuple(["00","01","02","03","04","05"])):
        await message.reply_text("Bölümlü arşiv tespit ettim (sanırım)\naçmak için şuna ihtiyacın olacak: https://telegra.ph/0-a%C3%A7mak-ve-olu%C5%9Fturmak-04-05\nrica ederim.", disable_web_page_preview=True)
    # - 001 gibi arşivse tuto gönder
    # + 001 gibi arşivse tuto gönder
    elif files.file_name and files.file_name.endswith(tuple(["rar","zip","7z","tar","gz"])):
        await message.reply_text("Arşiv tespit ettim (sanırım)\narşivleri telegram içinden çıkartmak için bazı botlar: @unziprobot @UnzipinBot @UnArchiveBot @ExtractProBot @ExtractorRobot", disable_web_page_preview=True)
    # - 001 gibi arşivse tuto gönder
    # + 001 gibi arşivse tuto gönder
    elif files.file_name and files.file_name.endswith(tuple(["exe","msi","jar"])):
        await message.reply_text("Program tespit ettim (sanırım)\nözellikle bu dosya türünde dikkatli olmalısın. şunu tamamen oku: https://telegra.ph/KitapAraBot-04-16\nvirüs tarama botları: @VirusTotalAV_bot @VirusTotal_AVBot", disable_web_page_preview=True)
    # - 001 gibi arşivse tuto gönder


@Client.on_message(filters.command('channel') & filters.user(ADMINS))
async def channel_info(bot, message):
           
    """Send basic information of channel"""
    if isinstance(CHANNELS, (int, str)):
        channels = [CHANNELS]
    elif isinstance(CHANNELS, list):
        channels = CHANNELS
    else:
        raise ValueError("Unexpected type of CHANNELS")

    text = '📑 **Indexed channels/groups**\n'
    for channel in channels:
        chat = await bot.get_chat(channel)
        if chat.username:
            text += '\n@' + chat.username
        else:
            text += '\n' + chat.title or chat.first_name

    text += f'\n\n**Total:** {len(CHANNELS)}'

    if len(text) < 4096:
        await message.reply(text)
    else:
        file = 'Indexed channels.txt'
        with open(file, 'w') as f:
            f.write(text)
        await message.reply_document(file)
        os.remove(file)


@Client.on_message(filters.command('logs') & filters.user(ADMINS))
async def log_file(bot, message):
    """Send log file"""
    try:
        await message.reply_document('log.txt')
    except Exception as e:
        await message.reply(str(e))

@Client.on_message(filters.command('delete') & filters.user(ADMINS))
async def delete(bot, message):
    """Delete file from database"""
    reply = message.reply_to_message
    if reply and reply.media:
        msg = await message.reply("Processing...⏳", quote=True)
    else:
        await message.reply('Reply to file with /delete which you want to delete', quote=True)
        return

    for file_type in ("document", "video", "audio"):
        media = getattr(reply, file_type, None)
        if media is not None:
            break
    else:
        await msg.edit('This is not supported file format')
        return
    
    file_id, file_ref = unpack_new_file_id(media.file_id)

    result = await Media.collection.delete_one({
        '_id': file_id,
    })
    if result.deleted_count:
        await msg.edit('File is successfully deleted from database')
    else:
        file_name = re.sub(r"(_|\-|\.|\+)", " ", str(media.file_name))
        result = await Media.collection.delete_many({
            'file_name': file_name,
            'file_size': media.file_size,
            'mime_type': media.mime_type
            })
        if result.deleted_count:
            await msg.edit('File is successfully deleted from database')
        else:
            # files indexed before https://github.com/EvamariaTG/EvaMaria/commit/f3d2a1bcb155faf44178e5d7a685a1b533e714bf#diff-86b613edf1748372103e94cacff3b578b36b698ef9c16817bb98fe9ef22fb669R39 
            # have original file name.
            result = await Media.collection.delete_many({
                'file_name': media.file_name,
                'file_size': media.file_size,
                'mime_type': media.mime_type
            })
            if result.deleted_count:
                await msg.edit('File is successfully deleted from database')
            else:
                await msg.edit('File not found in database')

# admin paneli
@Client.on_message(filters.command('admin') & filters.user(ADMINS))
async def adminpaneli(bot, message):
    await message.reply_text(
        'admin paneli',
        reply_markup=InlineKeyboardMarkup(
            [[
                InlineKeyboardButton(text="admin", callback_data="help")
            ]]),
        quote=True)

@Client.on_message(filters.command('deleteall') & filters.user(ADMINS))
async def delete_all_index(bot, message):
    await message.reply_text(
        'This will delete all indexed files.\nDo you want to continue?',
        reply_markup=InlineKeyboardMarkup(
            [   [ InlineKeyboardButton(text="YES", callback_data="autofilter_delete") ],
                [ InlineKeyboardButton(text="CANCEL", callback_data="close_data") ],
            ]
        ),
        quote=True,
    )


@Client.on_callback_query(filters.regex(r'^autofilter_delete'))
async def delete_all_index_confirm(bot, message):
    await Media.collection.drop()
    await message.answer('korsan suçtur :D')
    await message.message.edit('Succesfully Deleted All The Indexed Files.')

