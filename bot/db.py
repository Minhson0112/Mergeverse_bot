import mysql.connector
from .config import DB_CONFIG

def get_connection():
    return mysql.connector.connect(**DB_CONFIG)

def get_allowed_channels():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT channel_id FROM guild_settings")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return set(int(row[0]) for row in rows)

def save_guild_channel(guild_id, channel_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO guild_settings (guild_id, channel_id)
        VALUES (%s, %s)
        ON DUPLICATE KEY UPDATE channel_id = VALUES(channel_id)
    """, (guild_id, channel_id))
    conn.commit()
    cursor.close()
    conn.close()

def get_allowed_channel(guild_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT channel_id FROM guild_settings WHERE guild_id = %s", (guild_id,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return int(result[0]) if result else None
