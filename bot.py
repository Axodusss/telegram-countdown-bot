import os
import asyncio
from datetime import datetime, timezone

from telegram import Bot
from telegram.ext import Application, CommandHandler

TOKEN = os.environ["BOT_TOKEN"]

# Дата, до которой идёт отсчёт
TARGET_DATE = datetime(2027, 1, 1, tzinfo=timezone.utc)

# Сюда позже впишем ID твоего канала
CHANNEL_ID = os.environ.get("CHANNEL_ID")

# ID сообщения, которое бот будет обновлять
MESSAGE_ID = None


def get_days_left():
    now = datetime.now(timezone.utc)
    delta = TARGET_DATE - now
    return max(0, delta.days)


async def update_countdown(bot):
    global MESSAGE_ID

    if not CHANNEL_ID:
        return

    text = f"⏳ До 1 января 2027 года осталось: {get_days_left()} дней"

    if MESSAGE_ID is None:
        message = await bot.send_message(
            chat_id=CHANNEL_ID,
            text=text
        )
        MESSAGE_ID = message.message_id
    else:
        await bot.edit_message_text(
            chat_id=CHANNEL_ID,
            message_id=MESSAGE_ID,
            text=text
        )


async def countdown_loop(application):
    while True:
        try:
            await update_countdown(application.bot)
        except Exception as e:
            print("Ошибка:", e)

        await asyncio.sleep(86400)


async def start(update, context):
    await update.message.reply_text(
        "Бот работает! Отсчёт будет автоматически обновляться."
    )


async def main():
    application = (
        Application.builder()
        .token(TOKEN)
        .build()
    )

    application.add_handler(
        CommandHandler("start", start)
    )

    await application.initialize()
    await application.start()

    asyncio.create_task(countdown_loop(application))

    await application.updater.start_polling()

    try:
        await asyncio.Event().wait()
    finally:
        await application.updater.stop()
        await application.stop()
        await application.shutdown()


if __name__ == "__main__":
    asyncio.run(main())
