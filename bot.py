import os
import asyncio
from datetime import datetime
from zoneinfo import ZoneInfo
from telegram import Bot

TOKEN = os.environ["BOT_TOKEN"]
CHANNEL_ID = os.environ["CHANNEL_ID"]
MESSAGE_ID = int(os.environ["MESSAGE_ID"])

TARGET_DATE = datetime(2026, 11, 6, tzinfo=ZoneInfo("Europe/Moscow"))


async def main():
    now = datetime.now(ZoneInfo("Europe/Moscow"))

    if now.date() >= TARGET_DATE.date():
        text = "🎉 Сегодня можно получать права, поздравляю Вас, Сергей!😎 🏎️ 💸"
    else:
        days_left = (TARGET_DATE.date() - now.date()).days
        text = f"⏳ Осталось {days_left} дней до получения водительских прав на имя Сергея ⏳"

    async with Bot(token=TOKEN) as bot:
        try:
            await bot.edit_message_text(
                chat_id=CHANNEL_ID,
                message_id=MESSAGE_ID,
                text=text
            )
            print(f"Сообщение обновлено: {text}")

        except Exception as e:
            if "Message is not modified" in str(e):
                print("Сообщение уже содержит актуальный текст.")
            else:
                raise


if __name__ == "__main__":
    asyncio.run(main())
