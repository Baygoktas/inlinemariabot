import logging
from pyrogram import Client, emoji, filters
from pyrogram.errors.exceptions.bad_request_400 import QueryIdInvalid
from pyrogram.types import InlineQueryResultCachedDocument
from database.ia_filterdb import get_search_results
from database.temizleyici import cleanhtml
from utils import is_subscribed, get_size
from info import CACHE_TIME, AUTH_USERS, AUTH_CHANNEL, CUSTOM_FILE_CAPTION, BUTTON_COUNT

logger = logging.getLogger(__name__)
cache_time = 0 if AUTH_USERS or AUTH_CHANNEL else CACHE_TIME


@Client.on_inline_query(filters.user(AUTH_USERS) if AUTH_USERS else None)
async def answer(bot, query):
    if AUTH_CHANNEL and not await is_subscribed(bot, query):
        # await query.answer(results=[],
        #                    cache_time=0,
        #                    switch_pm_text='Tıkla buraya. Evet evet buraya.',
        #                    switch_pm_parameter="subscribe")
        return

    results = []
    if '|' in query.query:
        string, file_type = query.query.split('|', maxsplit=1)
        string = string.strip()
        file_type = file_type.strip().lower()
    else:
        string = query.query.strip()
        file_type = None

    offset = int(query.offset or 0)
    # reply_markup = get_reply_markup(query=string)
    files, next_offset, total = await get_search_results(string,
                                                  file_type=file_type,
                                                  max_results=BUTTON_COUNT,
                                                  offset=offset)

    for file in files:
        f_caption = file.caption
        if not f_caption: f_caption = str(file.file_name)
        f_caption += '' if CUSTOM_FILE_CAPTION is None else f'\n{CUSTOM_FILE_CAPTION}'

        altmetin = f'Boyut: {get_size(file.file_size)}, Tip: {file.file_type}'
        try: inlinecaption = cleanhtml(file.caption.replace('\n', ' '))
        except: inlinecaption = None
        if inlinecaption: altmetin += f'\n{inlinecaption}'

        results.append(
            InlineQueryResultCachedDocument(
                title=file.file_name,
                file_id=file.file_id,
                caption=f_caption,
                description=altmetin))

    if results:
        switch_pm_text = f"{emoji.FILE_FOLDER} {total} sonuç"
        if string:
            switch_pm_text += f": {string}"
        try:
            await query.answer(results=results,
                           is_personal = True,
                           cache_time=cache_time,
                           switch_pm_text=switch_pm_text,
                           switch_pm_parameter="start",
                           next_offset=str(next_offset))
        except QueryIdInvalid:
            pass
        except Exception as e:
            logging.exception(str(e))
            await query.answer(results=[], is_personal=True,
                           cache_time=cache_time,
                           switch_pm_text=str(e)[:63],
                           switch_pm_parameter="error")
    else:
        switch_pm_text = f'{emoji.CROSS_MARK} Bulamadım'
        if string:
            switch_pm_text += f': "{string}"'

        await query.answer(results=[],
                           is_personal = True,
                           cache_time=cache_time,
                           switch_pm_text=switch_pm_text,
                           switch_pm_parameter="okay")
