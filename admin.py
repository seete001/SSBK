import sqlite3
import asyncio
from telegram import Bot
import config
import schedule
import time

TOKEN = config.BOT_TOKEN
ChatID = config.CHAT_ID
DB_PATH = config.DB_FILE_PATH

bot = Bot(token=TOKEN)
loop = asyncio.get_event_loop()  # Reuse this loop


# Fetch next message to send
def get_next_message():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM contacts WHERE sent IS NULL LIMIT 1")
    row = cursor.fetchone()
    if row:
        message = (
            f"ID: {row[0]}\n"
            f"Name: {row[1]}\n"
            f"Email: {row[2]}\n"
            f"Phone: {row[3]}\n"
            f"Description: {row[4]}"
        )
        # Mark as sent
        cursor.execute("UPDATE contacts SET sent=1 WHERE id=?", (row[0],))
        conn.commit()
        conn.close()
        return message
    conn.close()
    return None


# Async send function
async def send_message_async(text):
    await bot.send_message(chat_id=ChatID, text=text)


# Job function for scheduler
def job():
    message = get_next_message()
    if message:
        try:
            loop.create_task(send_message_async(message))
        except Exception as e:
            print(f"Error scheduling message: {e}")
    else:
        print("No new messages to send.")


# Schedule job every 30 seconds
schedule.every(30).seconds.do(job)

print("Bot scheduler started...")
try:
    while True:
        schedule.run_pending()
        time.sleep(1)
except KeyboardInterrupt:
    print("Exiting...")
finally:
    loop.run_until_complete(bot.close())
