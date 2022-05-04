class script(object):
    START_TXT = """Esenlikler {}, ben <a href=https://t.me/{}>{}</a>.
Aşağıdaki butondan kanala katıl.
Bana özelden yaz. /start yazsan yeterli.
Ya bana bir kitap adı gönder,
Ya da ara butonuna tıklayınca kitap adını yazmaya başla.
Yapamadın mı? Diğelerine bakarak kopya çek.

🔥 Boşluklarla aratsan daha iyi olur:
Örnek: "nihalatsız ruh-adam.pdf" gibi yazma.
Şöyle yaz: "nihal atsız ruh adam"
Şöyle yaz: "ruh adam pdf"
Nokta tire gibi şeyler kullanmıyoruz.
Onun yerine boşluk koyuyoruz.

🔥 Ne kadar az şey yazarsan o kadar çok sonuç çıkar:
Örnek: "celal şengör dahi diktatör" gibi yazma.
Şöyle yaz: "dahi diktatör"
Şöyle yaz: "dahi diktatör epub"

🔥 Eğer Türkçe terimler çalışmazsa Türkçe karakterleri çıkar:
Örnek: "celal şengör dahi diktatör" gibi yazma.
Şöyle yaz: "celal sengor dahi diktator"

🔥 Oku: https://telegra.ph/KitapAraBot-04-16
"""
    HELP_TXT = "Esenlikler {} aşağıdaki butonlar sana yardımcı olur."
    ABOUT_TXT = "[🔥](https://telegra.ph/file/375b69b135524990cb7ca.jpg) {}, Sürüm: v2.0.4 Beta\nAnonim kişiler tarafından geliştirildi.\nTakıl işte üzümü ye bağını sorma.\nTelegramı indexleyen bir bot."
    SOURCE_TXT = "Takıl işte üzümü ye bağını sorma.\nTelegramı indexleyen bir bot."
    MANUELFILTER_TXT = SOURCE_TXT
    BUTTON_TXT = SOURCE_TXT
    AUTOFILTER_TXT = SOURCE_TXT
    CONNECTION_TXT = SOURCE_TXT
    EXTRAMOD_TXT = SOURCE_TXT
    ADMIN_TXT = SOURCE_TXT
    STATUS_TXT = """Dosya: <code>{}</code>
Kullanıcı: <code>{}</code>
Sohbet: <code>{}</code>
Dolu: <code>{}</code>
Boş: <code>{}</code>"""
    LOG_TEXT_G = """#NewGroup
Group = {}(<code>{}</code>)
Total Members = <code>{}</code>
Added By - {}
"""
    LOG_TEXT_P = """#NewUser
ID - <code>{}</code>
Name - {}
"""


    MANUELFILTER_TXT = """Help: <b>Filters</b>
- Filter is the feature were users can set automated replies for a particular keyword and EvaMaria will respond whenever a keyword is found the message
<b>NOTE:</b>
1. eva maria should have admin privillage.
2. only admins can add filters in a chat.
3. alert buttons have a limit of 64 characters.
<b>Commands and Usage:</b>
• /filter - <code>add a filter in chat</code>
• /filters - <code>list all the filters of a chat</code>
• /del - <code>delete a specific filter in chat</code>
• /delall - <code>delete the whole filters in a chat (chat owner only)</code>"""
    BUTTON_TXT = """Help: <b>Buttons</b>
- Eva Maria Supports both url and alert inline buttons.
<b>NOTE:</b>
1. Telegram will not allows you to send buttons without any content, so content is mandatory.
2. Eva Maria supports buttons with any telegram media type.
3. Buttons should be properly parsed as markdown format
<b>URL buttons:</b>
<code>[Button Text](buttonurl:https://t.me/EvaMariaBot)</code>
<b>Alert buttons:</b>
<code>[Button Text](buttonalert:This is an alert message)</code>"""
    AUTOFILTER_TXT = """Help: <b>Auto Filter</b>
<b>NOTE:</b>
1. Make me the admin of your channel if it's private.
2. make sure that your channel does not contains camrips, porn and fake files.
3. Forward the last message to me with quotes.
 I'll add all the files in that channel to my db."""
    CONNECTION_TXT = """Help: <b>Connections</b>
- Used to connect bot to PM for managing filters 
- it helps to avoid spamming in groups.
<b>NOTE:</b>
1. Only admins can add a connection.
2. Send <code>/connect</code> for connecting me to ur PM
<b>Commands and Usage:</b>
• /connect  - <code>connect a particular chat to your PM</code>
• /disconnect  - <code>disconnect from a chat</code>
• /connections - <code>list all your connections</code>"""
    EXTRAMOD_TXT = """Help: <b>Extra Modules</b>
<b>NOTE:</b>
these are the extra features of Eva Maria"""
    ADMIN_TXT = """Help: <b>Admin mods</b>
<b>NOTE:</b>
This module only works for my admins
<b>Commands and Usage:</b>
• /logs - <code>to get the rescent errors</code>
• /stats - <code>to get status of files in db.</code>
• /delete - <code>to delete a specific file from db.</code>
• /users - <code>to get list of my users and ids.</code>
• /setskip - <code>set index from id.</code>
• /chats - <code>to get list of the my chats and ids </code>
• /leave  - <code>to leave from a chat.</code>
• /disable  -  <code>do disable a chat.</code>
• /ban  - <code>to ban a user.</code>
• /unban  - <code>to unban a user.</code>
• /channel - <code>to get list of total connected channels</code>
• /broadcast - <code>to broadcast a message to all users</code>
• /deleteall - <code>delete all saved files from database</code>"""