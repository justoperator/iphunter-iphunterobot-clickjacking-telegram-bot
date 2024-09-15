import sqlite3

# Создаем соединение с базой данных
conn = sqlite3.connect('databases/database.db')
c = conn.cursor()

# Таблица пользователей
c.execute('''
    CREATE TABLE IF NOT EXISTS users(
        id TEXT PRIMARY KEY,
        username TEXT,
        messages TEXT,
        links_count TEXT,
        language TEXT
    )
''')

# Таблица премиум-пользователей
c.execute('''
    CREATE TABLE IF NOT EXISTS premium_us(
        user TEXT PRIMARY KEY,
        buy_id TEXT,
        byrefferals TEXT,
        expiry_date TEXT
    )
''')

# Таблица рефералов
c.execute('''
    CREATE TABLE IF NOT EXISTS refferals_us(
        user TEXT PRIMARY KEY,
        refferals TEXT
    )
''')

# Таблица сообщений пользователей
c.execute('''
    CREATE TABLE IF NOT EXISTS messages_us(
        user TEXT PRIMARY KEY,
        messages_count INTEGER
    )
''')

# Таблица для хранения информации о реферальных связях
c.execute('''
    CREATE TABLE IF NOT EXISTS referrals(
        user_id TEXT,
        referrer_id TEXT,
        PRIMARY KEY (user_id, referrer_id)
    )
''')

# Таблица для промокодов
c.execute('''
    CREATE TABLE IF NOT EXISTS promo_codes(
        code TEXT PRIMARY KEY,
        reward_type TEXT,
        reward_value INTEGER,
        expiry_date TEXT
        usage_limit INTEGER DEFAULT -1
    )
''')

c.execute('''
    CREATE TABLE IF NOT EXISTS used_promos(
        user_id INTEGER,
        promo_code TEXT,
        PRIMARY KEY (user_id, promo_code)
    )
    ''')

# Таблица для подписок
c.execute('''
    CREATE TABLE IF NOT EXISTS subscriptions(
        user TEXT PRIMARY KEY,
        subscribed INTEGER DEFAULT 0
    )
''')


conn.commit()
conn.close()
