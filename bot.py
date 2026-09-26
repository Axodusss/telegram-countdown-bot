import os
from datetime import datetime, timezone
from telegram import Bot

TOKEN = os.environ["BOT_TOKEN"]
CHANNEL_ID = os.environ["CHANNEL_ID"]
MESSAGE_ID = int(os.environ["MESSAGE_ID"])

TARGET_DATE = datetime(2026, 11, 6, tzinfo=timezone.utc)


def get_days_left():
    now = datetime.now(timezone.utc)
    return max(0, (TARGET_DATE - now).days)


def main():
    text = f"⏳ До 6 ноября осталось: {get_days_left()} дней"

    bot = Bot(token=TOKEN)

    import asyncio

    async def update():
        await bot.edit_message_text(
            chat_id=CHANNEL_ID,
            message_id=MESSAGE_ID,
            text=text
        )

    asyncio.run(update())


if __name__ == "__main__":
    main()
