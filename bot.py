import os
import asyncio
from datetime import datetime, timezone
from telegram import Bot

TOKEN = os.environ["BOT_TOKEN"]
CHANNEL_ID = os.environ["CHANNEL_ID"]
MESSAGE_ID = int(os.environ["MESSAGE_ID"])

TARGET_DATE = datetime(2026, 11, 6, tzinfo=timezone.utc)


async def main():
    now = datetime.now(timezone.utc)

    if now >= TARGET_DATE:
        text = "🎉 Сегодня можно получать права!"
    else:
        days_left = (TARGET_DATE - now).days
        text = f"⏳ Осталось {days_left} дней до получения водительских прав на имя Сергея ⏳"

    async with Bot(token=TOKEN) as bot:
        await bot.edit_message_text(
            chat_id=CHANNEL_ID,
            message_id=MESSAGE_ID,
            text=text
        )

    print(f"Сообщение обновлено: {text}")


if __name__ == "__main__":
    asyncio.run(main())
