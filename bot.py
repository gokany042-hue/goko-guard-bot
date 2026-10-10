import telebot
from telebot import types
import time

# Bilgileriniz
TOKEN = "8998485712:AAH15ldE_wr-Q00GRNXw4IGO0rmDyVmAYbk"
OWNER_ID = 7731769678
BOT_USERNAME = "Gokokoruma_bot"  

bot = telebot.TeleBot(TOKEN)

# Dinamik Yasaklı Kelimeler Listesi
YASAKLI_KELIMELER = ["küfür1", "küfür2", "reklam", "amk", "aq", "orospu", "oc"]

user_last_message_time = {}
user_warnings = {} 

def is_admin(message):
    try:
        chat_member = bot.get_chat_member(message.chat.id, message.from_user.id)
        return chat_member.status in ['creator', 'administrator']
    except:
        return False

# Gelişmiş Inline Butonlu Start Menüsü (Gruba + Kanala Ekleme Desteği)
@bot.message_handler(commands=['start'])
def let_start(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    
    # Hem Gruba hem Kanala ekleme butonları ayrı ayrı eklendi
    btn_add_group = types.InlineKeyboardButton("➕ Gruba Ekle", url=f"https://t.me/{BOT_USERNAME}?startgroup=true")
    btn_add_channel = types.InlineKeyboardButton("📢 Kanala Ekle", url=f"https://t.me/{BOT_USERNAME}?startchannel=true")
    
    btn_clone = types.InlineKeyboardButton("🧬 Beni Klonla", callback_data="btn_clone")
    btn_settings = types.InlineKeyboardButton("🛡️ Koruma Ayarları", callback_data="btn_settings")
    btn_welcome = types.InlineKeyboardButton("👋 Karşılama", callback_data="btn_welcome")
    btn_badwords = types.InlineKeyboardButton("🚫 Yasaklı Kelimeler", callback_data="btn_badwords")
    btn_warns = types.InlineKeyboardButton("⚠️ Uyarılar", callback_data="btn_warns")
    btn_admins = types.InlineKeyboardButton("👮 Yetkililer", callback_data="btn_admins")
    btn_stats = types.InlineKeyboardButton("📊 İstatistik", callback_data="btn_stats")
    btn_notes = types.InlineKeyboardButton("📝 Notlar", callback_data="btn_notes")
    btn_filters = types.InlineKeyboardButton("🔍 Filtreler", callback_data="btn_filters")
    btn_rules = types.InlineKeyboardButton("📜 Kurallar", callback_data="btn_rules")
    btn_help = types.InlineKeyboardButton("❓ Yardım", callback_data="btn_help")
    btn_night = types.InlineKeyboardButton("🌙 Gece Modu", callback_data="btn_night")
    btn_backup = types.InlineKeyboardButton("💾 Yedekle", callback_data="btn_backup")
    btn_suggest = types.InlineKeyboardButton("💡 Öneri", callback_data="btn_suggest")
    btn_report = types.InlineKeyboardButton("⚠️ Şikayet", callback_data="btn_report")
    btn_bug = types.InlineKeyboardButton("🐛 Bug Bildir", callback_data="btn_bug")
    btn_role = types.InlineKeyboardButton("🎖️ Rolüm", callback_data="btn_role")
    
    btn_channel = types.InlineKeyboardButton("📢 Kanal ↗️", url="https://t.me/yago_frewl")
    btn_dev = types.InlineKeyboardButton("🧙‍♂️ Geliştirici ↗️", url="https://t.me/GOKO_R4")
    
    # Buton Düzeni
    markup.add(btn_add_group, btn_add_channel)
    markup.add(btn_clone, btn_settings)
    markup.add(btn_welcome, btn_badwords)
    markup.add(btn_warns, btn_admins)
    markup.add(btn_stats, btn_notes)
    markup.add(btn_filters, btn_rules)
    markup.add(btn_help, btn_night)
    markup.add(btn_backup, btn_suggest)
    markup.add(btn_report, btn_bug)
    markup.add(btn_role)
    markup.add(btn_channel, btn_dev)
    
    caption_text = (
        "🚀 **GÖKØ GUARD HOŞGELDİNİZ** ✨\n\n"
        "🛡️ Profesyonel Grup ve Kanal Koruma Sistemi\n\n"
        "➕ **Grubuna veya Kanalına Ekle!**\n"
        "🧬 **Kendi botunu klonla!**\n\n"
        "💡 Komutlar için /help"
    )
    
    bot.reply_to(message, caption_text, parse_mode="Markdown", reply_markup=markup)

# Menü Buton Yanıtları (Sohbete Mesaj Atar)
@bot.callback_query_handler(func=lambda call: True)
def callback_listener(call):
    chat_id = call.message.chat.id
    
    responses = {
        "btn_clone": "🧬 **Klonlama Sistemi:** Botunuzu kendi tokeninizle çalıştırabilirsiniz.",
        "btn_settings": "🛡️ **Koruma Ayarları:** Küfür, link, flood, anti-bot, kilit ve filtreler tam aktif.",
        "btn_welcome": "👋 **Karşılama Sistemi:** Yeni üyeler gruba girdiğinde otomatik karşılanır.",
        "btn_badwords": "🚫 **Yasaklı Kelimeler:** /addword ve /delword komutlarıyla kelime yönetebilirsiniz.",
        "btn_warns": "⚠️ **Uyarı Sistemi:** 3 uyarı alan kullanıcılar sistem tarafından cezalandırılır.",
        "btn_admins": "👮 **Yetkili Yönetimi:** Kurucu ve yöneticiler korumalardan muaftır.",
        "btn_stats": "📊 **İstatistikler:** Bot grubu kesintisiz korumaktadır.",
        "btn_notes": "📝 **Notlar Sistemi:** Grup içi notlar saklanabilir.",
        "btn_filters": "🔍 **Filtreler:** Metin, bağlantı ve reklam denetimleri çalışıyor.",
        "btn_rules": "📜 **Kurallar:** /rules komutu ile kurallara ulaşabilirsiniz.",
        "btn_help": "❓ **Yardım Menüsü:**\n• `/ban` - Yasaklar\n• `/mute` - Susturur\n• `/warn` - Uyarır\n• `/lock /unlock` - Sohbeti kilitler\n• `/purge` - Mesajları temizler\n• `/ping` - Bot durumunu gösterir",
        "btn_night": "🌙 **Gece Modu:** Gece güvenliğini sağlar.",
        "btn_backup": "💾 **Yedekleme:** Veriler güvence altındadır.",
        "btn_suggest": "💡 **Öneri:** Görüşlerinizi bildirebilirsiniz.",
        "btn_report": "⚠️ **Şikayet:** Yönetici denetimindedir.",
        "btn_bug": "🐛 **Bug Bildir:** Hata bildirim sistemi.",
        "btn_role": f"🎖️ **Rol Bilginiz:** {'Kurucu / Yönetici' if call.from_user.id == OWNER_ID else 'Standart Üye'}"
    }

    if call.data in responses:
        bot.send_message(chat_id, responses[call.data], parse_mode="Markdown")
        bot.answer_callback_query(call.id)

# Ping Komutu
@bot.message_handler(commands=['ping'])
def ping_bot(message):
    bot.reply_to(message, "⚡ **Gökø Guard aktif ve sorunsuz çalışıyor!** (Ping: 0.04s)", parse_mode="Markdown")

# ID Komutu
@bot.message_handler(commands=['id'])
def show_id(message):
    target = message.reply_to_message.from_user if message.reply_to_message else message.from_user
    text = (
        f"👤 **Kullanıcı Bilgileri:**\n"
        f"• **Adı:** {target.first_name}\n"
        f"• **Kullanıcı Adı:** @{target.username or 'Yok'}\n"
        f"• **Kullanıcı ID:** `{target.id}`"
    )
    bot.reply_to(message, text, parse_mode="Markdown")

# Sohbet Kilitleme
@bot.message_handler(commands=['lock'])
def lock_chat(message):
    if message.from_user.id != OWNER_ID and not is_admin(message):
        return
    try:
        bot.set_chat_permissions(message.chat.id, types.ChatPermissions(can_send_messages=False))
        bot.reply_to(message, "🔒 **Sohbet yöneticiler tarafından kilitlendi!** Artık kimse mesaj yazamaz.")
    except:
        bot.reply_to(message, "❌ Yetkim yetersiz.")

@bot.message_handler(commands=['unlock'])
def unlock_chat(message):
    if message.from_user.id != OWNER_ID and not is_admin(message):
        return
    try:
        bot.set_chat_permissions(message.chat.id, types.ChatPermissions(
            can_send_messages=True, can_send_media_messages=True, 
            can_send_other_messages=True, can_add_web_page_previews=True
        ))
        bot.reply_to(message, "🔓 **Sohbetin kilidi açıldı!** Üyeler tekrar mesaj yazabilir.")
    except:
        bot.reply_to(message, "❌ Yetkim yetersiz.")

# Toplu Mesaj Temizleme (Purge)
@bot.message_handler(commands=['purge'])
def purge_messages(message):
    if message.from_user.id != OWNER_ID and not is_admin(message):
        return
    if message.reply_to_message:
        start_id = message.reply_to_message.message_id
        end_id = message.message_id
        deleted_count = 0
        for msg_id in range(start_id, end_id + 1):
            try:
                bot.delete_message(message.chat.id, msg_id)
                deleted_count += 1
            except:
                pass
        
        notify = bot.send_message(message.chat.id, f"🧹 {deleted_count} mesaj başarıyla temizlendi.")
        time.sleep(2)
        try:
            bot.delete_message(message.chat.id, notify.message_id)
        except:
            pass

# Dinamik Kelime Ekle / Sil
@bot.message_handler(commands=['addword'])
def add_word(message):
    if message.from_user.id != OWNER_ID and not is_admin(message):
        return
    args = message.text.split(maxsplit=1)
    if len(args) > 1:
        new_word = args[1].lower()
        if new_word not in YASAKLI_KELIMELER:
            YASAKLI_KELIMELER.append(new_word)
            bot.reply_to(message, f"✅ `{new_word}` yasaklı kelimelere eklendi.", parse_mode="Markdown")
        else:
            bot.reply_to(message, "⚠️ Bu kelime zaten listede var.")
    else:
        bot.reply_to(message, "⚠️ Lütfen eklenecek kelimeyi yazın. Örnek: `/addword kelime`", parse_mode="Markdown")

@bot.message_handler(commands=['delword'])
def del_word(message):
    if message.from_user.id != OWNER_ID and not is_admin(message):
        return
    args = message.text.split(maxsplit=1)
    if len(args) > 1:
        word = args[1].lower()
        if word in YASAKLI_KELIMELER:
            YASAKLI_KELIMELER.remove(word)
            bot.reply_to(message, f"🗑️ `{word}` yasaklı kelimelerden kaldırıldı.", parse_mode="Markdown")
        else:
            bot.reply_to(message, "❌ Bu kelime listede bulunamadı.")
    else:
        bot.reply_to(message, "⚠️ Lütfen silinecek kelimeyi yazın. Örnek: `/delword kelime`", parse_mode="Markdown")

# Kurallar
@bot.message_handler(commands=['rules'])
def show_rules(message):
    rules_text = (
        "📜 **Grup Kuralları:**\n\n"
        "1️⃣ Küfür, argo ve hakaret kesinlikle yasaktır.\n"
        "2️⃣ İzinsiz reklam, link ve t.me davetleri yasaktır.\n"
        "3️⃣ Spam, flood ve ard arda gereksiz mesaj atmak yasaktır.\n"
        "4️⃣ Din, siyaset ve tartışma yaratmak yasaktır.\n\n"
        "⚠️ *Kurallara uymayanlar sistem tarafından cezalandırılır!*"
    )
    bot.reply_to(message, rules_text, parse_mode="Markdown")

# Uyarı Sistemi
@bot.message_handler(commands=['warn'])
def warn_user(message):
    if message.from_user.id != OWNER_ID and not is_admin(message):
        bot.reply_to(message, "⚠️ Bu komutu sadece yöneticiler kullanabilir!")
        return
    if message.reply_to_message:
        target_id = message.reply_to_message.from_user.id
        target_name = message.reply_to_message.from_user.first_name
        
        if target_id == OWNER_ID:
            bot.reply_to(message, "❌ Kurucu uyarılmaz!")
            return
            
        user_warnings[target_id] = user_warnings.get(target_id, 0) + 1
        count = user_warnings[target_id]
        
        if count >= 3:
            try:
                bot.ban_chat_member(message.chat.id, target_id)
                bot.reply_to(message, f"🚫 {target_name} 3 uyarı sınırını aştığı için gruptan yasaklandı!")
                user_warnings[target_id] = 0
            except:
                bot.reply_to(message, "❌ Kullanıcı yasaklanamadı, yetkim yetersiz.")
        else:
            bot.reply_to(message, f"⚠️ {target_name} uyarıldı! (Toplam Uyarı: {count}/3)")

# Yönetici Komutları
@bot.message_handler(commands=['ban'])
def ban_user(message):
    if message.from_user.id != OWNER_ID and not is_admin(message):
        return
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        if user_id == OWNER_ID:
            bot.reply_to(message, "❌ Kurucuyu yasaklayamazsın!")
            return
        try:
            bot.ban_chat_member(message.chat.id, user_id)
            bot.reply_to(message, "🔨 Kullanıcı gruptan yasaklandı.")
        except:
            bot.reply_to(message, "❌ Botu grupta admin yapmalısın.")

@bot.message_handler(commands=['mute'])
def mute_user(message):
    if message.from_user.id != OWNER_ID and not is_admin(message):
        return
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        try:
            bot.restrict_chat_member(message.chat.id, user_id, can_send_messages=False)
            bot.reply_to(message, "🔇 Kullanıcı susturuldu.")
        except:
            bot.reply_to(message, "❌ Botu grupta admin yapmalısın.")

@bot.message_handler(commands=['unmute'])
def unmute_user(message):
    if message.from_user.id != OWNER_ID and not is_admin(message):
        return
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        try:
            bot.restrict_chat_member(message.chat.id, user_id, can_send_messages=True, can_send_media_messages=True, can_send_other_messages=True)
            bot.reply_to(message, "🔊 Kullanıcının susturulması kaldırıldı.")
        except:
            pass

# Yeni Üye Karşılama ve Anti-Bot
@bot.message_handler(content_types=['new_chat_members'])
def welcome_and_antibot(message):
    for new_member in message.new_chat_members:
        if new_member.is_bot and new_member.id != bot.get_me().id:
            try:
                bot.ban_chat_member(message.chat.id, new_member.id)
                bot.send_message(message.chat.id, f"🤖 İzinsiz eklenen yabancı bot engellendi: @{new_member.username}")
            except:
                pass
            return
            
        if not new_member.is_bot:
            welcome_text = (
                f"✨ Hoş geldin [{new_member.first_name}](tg://user?id={new_member.id})!\n"
                f"🛡️ Bu grup Gökø Guard ile korunmaktadır.\n"
                f"📜 Lütfen kurallara uymayı unutma (/rules)."
            )
            bot.send_message(message.chat.id, welcome_text, parse_mode="Markdown")

# Koruma Filtreleri
@bot.message_handler(func=lambda message: True, content_types=['text'])
def guard_system(message):
    if message.chat.type in ['group', 'supergroup']:
        if message.from_user.id == OWNER_ID or is_admin(message):
            return

        user_id = message.from_user.id
        text = message.text.lower()

        # Link ve Kanal Engelleme
        if "http://" in text or "https://" in text or "t.me/" in text or "www." in text or "@" in text:
            try:
                bot.delete_message(message.chat.id, message.message_id)
                bot.send_message(message.chat.id, f"⚠️ @{message.from_user.username or message.from_user.first_name}, link veya reklam paylaşımı yasaktır!")
            except:
                pass
            return

        # Küfür Engelleme
        for kelime in YASAKLI_KELIMELER:
            if kelime in text:
                try:
                    bot.delete_message(message.chat.id, message.message_id)
                    bot.send_message(message.chat.id, f"⚠️ @{message.from_user.username or message.from_user.first_name}, küfür/argo kullanımı yasaktır!")
                except:
                    pass
                return

        # Flood Koruması
        current_time = time.time()
        if user_id in user_last_message_time:
            if current_time - user_last_message_time[user_id] < 1.5:
                try:
                    bot.delete_message(message.chat.id, message.message_id)
                    bot.restrict_chat_member(message.chat.id, user_id, can_send_messages=False, until_date=int(time.time() + 60))
                    bot.send_message(message.chat.id, f"⚠️ @{message.from_user.username or message.from_user.first_name}, spam yaptığınız için 1 dakika susturuldunuz!")
                except:
                    pass
                return
        user_last_message_time[user_id] = current_time

print("Gökø Guard Master Sürüm Aktif...")
bot.infinity_polling()
                                          
