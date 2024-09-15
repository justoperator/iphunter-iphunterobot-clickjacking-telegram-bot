import sqlite3

conn = sqlite3.connect('databases/database.db')
c = conn.cursor()

# Users table
c.execute('''
    CREATE TABLE IF NOT EXISTS users(
        id TEXT PRIMARY KEY,
        username TEXT,
        messages TEXT,
        links_count TEXT,
        language TEXT
    )
''')

# Premium users table
c.execute('''
    CREATE TABLE IF NOT EXISTS premium_us(
        user TEXT PRIMARY KEY,
        buy_id TEXT,
        byrefferals TEXT,
        expiry_date TEXT
    )
''')

# Refferals table
c.execute('''
    CREATE TABLE IF NOT EXISTS refferals_us(
        user TEXT PRIMARY KEY,
        refferals TEXT
    )
''')

# Messages count table
c.execute('''
    CREATE TABLE IF NOT EXISTS messages_us(
        user TEXT PRIMARY KEY,
        messages_count INTEGER
    )
''')

# Another refferals table
c.execute('''
    CREATE TABLE IF NOT EXISTS referrals(
        user_id TEXT,
        referrer_id TEXT,
        PRIMARY KEY (user_id, referrer_id)
    )
''')

# Promocodes table
c.execute('''
    CREATE TABLE IF NOT EXISTS promo_codes(
        code TEXT PRIMARY KEY,
        reward_type TEXT,
        reward_value INTEGER,
        expiry_date TEXT
        usage_limit INTEGER DEFAULT -1
    )
''')

# Used promocodes table
c.execute('''
    CREATE TABLE IF NOT EXISTS used_promos(
        user_id INTEGER,
        promo_code TEXT,
        PRIMARY KEY (user_id, promo_code)
    )
    ''')

# Subscribers table
c.execute('''
    CREATE TABLE IF NOT EXISTS subscriptions(
        user TEXT PRIMARY KEY,
        subscribed INTEGER DEFAULT 0
    )
''')


conn.commit()
conn.close()
