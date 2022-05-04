import logging
import asyncio
from pyrogram import Client, filters
from pyrogram.errors.exceptions.bad_request_400 import ChannelInvalid, ChatAdminRequired, UsernameInvalid, UsernameNotModified
from info import ADMINS
from info import INDEX_REQ_CHANNEL as LOG_CHANNEL
from info import botStartTime
from database.ia_filterdb import save_file
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from utils import temp
import re, time
from plugins.pm_filter import ReadableTime
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
lock = asyncio.Lock()
from pyrogram.types import Message
from pyrogram import client

@Client.on_callback_query(filters.regex(r'^index'))
async def index_files(bot, query):
    if query.data.startswith('index_cancel'):
        temp.CANCEL = True
        return await query.answer("Cancelling Indexing")
    _, raju, chat, lst_msg_id, from_user, fastordb = query.data.split("#")
    if raju == 'reject':
        await query.message.delete()
        await bot.send_message(int(from_user),
                               f'Your Submission for indexing {chat} has been decliened by our moderators.',
                               reply_to_message_id=int(lst_msg_id))
        return

    if lock.locked():
        return await query.answer('Wait until previous process complete.', show_alert=True)
    msg = query.message

    await query.answer('Processing...', show_alert=True)
    if int(from_user) not in ADMINS:
        await bot.send_message(int(from_user),
                               f'Your Submission for indexing {chat} has been accepted by our moderators and will be added soon.',
                               reply_to_message_id=int(lst_msg_id))
    await msg.edit(
        "Starting Indexing",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton('Cancel', callback_data='index_cancel')]]
        )
    )
    try: chat = int(chat)
    except: chat = chat
    await index_files_to_db(int(lst_msg_id), chat, msg, bot, fastordb=="dbindex")


@Client.on_message((filters.forwarded | (filters.regex("(https://)?(t\.me/|telegram\.me/|telegram\.dog/)(c/)?(\d+|[a-zA-Z_0-9]+)/(\d+)$")) & filters.text ) & filters.private & filters.incoming)
async def send_for_index(bot, message):
    if message.text:
        regex = re.compile("(https://)?(t\.me/|telegram\.me/|telegram\.dog/)(c/)?(\d+|[a-zA-Z_0-9]+)/(\d+)$")
        match = regex.match(message.text)
        if not match:
            return await message.reply('Invalid link')
        chat_id = match.group(4)
        last_msg_id = int(match.group(5))
        if chat_id.isnumeric():
            chat_id  = int(("-100" + chat_id))
    elif message.forward_from_chat.type == 'channel':
        last_msg_id = message.forward_from_message_id
        chat_id = message.forward_from_chat.username or message.forward_from_chat.id
    else:
        return
    try:
        await bot.get_chat(chat_id)
    except ChannelInvalid:
        return await message.reply('This may be a private channel / group. Make me an admin over there to index the files.')
    except (UsernameInvalid, UsernameNotModified):
        return await message.reply('Invalid Link specified.')
    except Exception as e:
        logger.exception(e)
        return await message.reply(f'Errors - {e}')
    try:
        k = await bot.get_messages(chat_id, last_msg_id)
    except:
        return await message.reply('Make Sure That Iam An Admin In The Channel, if channel is private')
    if k.empty:
        return await message.reply('This may be group and iam not a admin of the group.')

    if message.from_user.id in ADMINS:
        buttons = [
            [
                InlineKeyboardButton('Yes (DB)',
                                     callback_data=f'index#accept#{chat_id}#{last_msg_id}#{message.from_user.id}#dbindex')
            ],
            [
                InlineKeyboardButton('Yes (Fast)',
                                     callback_data=f'index#accept#{chat_id}#{last_msg_id}#{message.from_user.id}#fastindex')
            ],
            [
                InlineKeyboardButton('Cancel', callback_data='close_data'),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(buttons)
        return await message.reply(
            f'Do you Want To Index This Channel/ Group ?\n\nChat ID/ Username: `{chat_id}`\nLast Message ID: `{last_msg_id}`\nStarting ID: {str(temp.CURRENT)}\nExample: index from 23140. message: `/setskip 23140`',
            reply_markup=reply_markup)

    if type(chat_id) is int:
        try:
            link = (await bot.create_chat_invite_link(chat_id)).invite_link
        except ChatAdminRequired:
            return await message.reply('Make sure iam an admin in the chat and have permission to invite users.')
    else:
        link = f"@{message.forward_from_chat.username}"
    buttons = [
        [
            InlineKeyboardButton('Accept (DB)',
                                 callback_data=f'index#accept#{chat_id}#{last_msg_id}#{message.from_user.id}#dbindex')
        ],
        [
            InlineKeyboardButton('Accept (Fast)',
                                 callback_data=f'index#accept#{chat_id}#{last_msg_id}#{message.from_user.id}#fastindex')
        ],
        [
            InlineKeyboardButton('Reject Index',
                                 callback_data=f'index#reject#{chat_id}#{message.message_id}#{message.from_user.id}#silme'),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(buttons)
    await bot.send_message(LOG_CHANNEL,
                           f'#IndexRequest\n\nBy : {message.from_user.mention} (`{message.from_user.id}`)\nChat ID/ Username - ` {chat_id}`\nLast Message ID - `{last_msg_id}`\nInviteLink - {link}',
                           reply_markup=reply_markup)
    await message.reply('ThankYou For the Contribution, Wait For My Moderators to verify the files.')


@Client.on_message(filters.command('setskip') & filters.user(ADMINS))
async def set_skip_number(bot, message):
    if ' ' in message.text:
        _, skip = message.text.split(" ")
        try:
            skip = int(skip)
        except:
            return await message.reply("Skip number should be an integer.")
        await message.reply(f"Successfully set SKIP number as {skip}")
        temp.CURRENT = int(skip)
    else:
        await message.reply("Give me a skip number")


async def index_files_to_db(lst_msg_id, chat, msg, bot, dbindex):
    total_files = 0
    duplicate = 0
    errors = 0
    deleted = 0
    no_media = 0
    unsupported = 0
    kayitdisi = 0
    baslangic = time.time()
    hiz = 0
    async with lock:
        try:
            current = temp.CURRENT
            temp.CANCEL = False
            async for message in bot.iter_messages(chat, lst_msg_id, temp.CURRENT):
                try: hiz = (current / ((time.time() - baslangic).__round__())).__round__()
                except: hiz = 0
                if temp.CANCEL:
                    await msg.edit(f"Successfully Cancelled\n\nSaved `{total_files}` files to dataBase!\nDuplicate Files Skipped: `{duplicate}`\nDeleted Messages Skipped: `{deleted}`\nNon-Media messages skipped: `{no_media + unsupported}`(Unsupported Media - `{unsupported}` )\nEs geçilenler: `{kayitdisi}`\nErrors Occurred: `{errors}`\nSüre: `{ReadableTime(time.time() - baslangic)}`\nHız: `{hiz} öge/saniye`\nBot Ömrü: `{ReadableTime(time.time() - botStartTime)}`")
                    break
                current += 1
                # kaçta bir güncellesin
                kactabir = 20 if dbindex else 200
                if current % kactabir == 0:
                    reply = InlineKeyboardMarkup([[InlineKeyboardButton('Cancel', callback_data='index_cancel')]])
                    try: await msg.edit_text(text=f"Starting ID: {str(temp.CURRENT)}\nTotal messages fetched: `{current}`\nTotal messages saved: `{total_files}`\nDuplicate Files Skipped: `{duplicate}`\nDeleted Messages Skipped: `{deleted}`\nNon-Media skipeed: `{no_media}`\nUnsupported Media skipped: `{unsupported}`\nErrors Occurred: `{errors}`\nEs geçilenler: `{kayitdisi}`\nIndex from: `/setskip {current}`\nSüre: `{ReadableTime(time.time() - baslangic)}`\nHız: `{hiz} öge/saniye`\nBot Ömrü: `{ReadableTime(time.time() - botStartTime)}`", reply_markup=reply)
                    except: pass
                if message.empty:
                    deleted += 1
                    continue
                elif not message.media:
                    no_media += 1
                    continue
                elif message.media not in ['audio', 'video', 'document']:
                    unsupported += 1
                    continue
                media = getattr(message, message.media, None)
                if not media:
                    unsupported += 1
                    continue
                if dbindex:
                    media.file_type = message.media
                    media.caption = message.caption
                    res = await save_file(media)
                    if res == 1:
                        total_files += 1
                    elif res == 2:
                        duplicate += 1
                    elif res == 3:
                        errors += 1
                    elif res == 4:
                        kayitdisi += 1
        except Exception as e:
            logger.exception(e)
            await msg.edit(f'Error: {e}')
        else:
            await msg.edit(f'Succesfully saved `{total_files}` to database!\nDuplicate Files Skipped: `{duplicate}`\nDeleted Messages Skipped: `{deleted}`\nNon-Media skipeed: `{no_media}`\nUnsupported Media skipped: `{unsupported}` )\nEs geçilenler: `{kayitdisi}`\nErrors Occurred: `{errors}`\nSüre: `{ReadableTime(time.time() - baslangic)}`\nHız: `{hiz} öge/saniye`\nBot Ömrü: `{ReadableTime(time.time() - botStartTime)}`')
