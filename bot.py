"""
Telegram-бот: анализатор надёжности паролей + генератор.

Команды:
  /start   — приветствие и краткая инструкция
  /help    — список команд
  /generate [длина] — сгенерировать надёжный пароль (по умолчанию 16 символов)

Обычное текстовое сообщение — бот воспринимает как пароль для проверки.
"""

import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandObject
from aiogram.types import Message

from checker import format_report
from generator import generate_password

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")

WELCOME_TEXT = (
    "👀 Привет! Я замочек, который повидал слишком много паролей типа `123456`.\n\n"
    "Кинь мне свой пароль текстом — оценю его по шкале от «взломают за 2 секунды» "
    "до «даже спецслужбы попотеют».\n\n"
    "🔹 /generate — выдам тебе нормальный пароль, а не то, что ты обычно придумываешь\n"
    "🔹 /generate 20 — пароль на 20 символов, если параноишь по-крупному\n\n"
    "⚠️ Только не присылай сюда пароли от реальных аккаунтов — используй тестовые. "
    "Я, конечно, замочек добрый и ничего не сохраняю, но привычка хорошая."
)

HELP_TEXT = (
    "Доступные команды:\n"
    "/start — приветствие\n"
    "/help — эта справка\n"
    "/generate [длина] — сгенерировать пароль\n\n"
    "Чтобы проверить пароль — просто отправь его сообщением."
)


async def cmd_start(message: Message) -> None:
    await message.answer(WELCOME_TEXT)


async def cmd_help(message: Message) -> None:
    await message.answer(HELP_TEXT)


async def cmd_generate(message: Message, command: CommandObject) -> None:
    length = 16
    if command.args:
        try:
            length = int(command.args.strip())
        except ValueError:
            await message.answer("Длина должна быть числом, например: /generate 20")
            return

    try:
        password = generate_password(length=length)
    except ValueError as e:
        await message.answer(f"Ошибка: {e}")
        return

    await message.answer(
        f"Сгенерированный пароль:\n`{password}`\n\n"
        f"Длина: {length} символов",
        parse_mode="Markdown",
    )


async def check_password(message: Message) -> None:
    password = message.text
    report = format_report(password)

    try:
        await message.delete()
    except Exception:
        pass

    await message.answer(report)


async def main() -> None:
    if not BOT_TOKEN:
        raise RuntimeError(
            "Не найден BOT_TOKEN. Установи переменную окружения BOT_TOKEN "
            "с токеном, полученным от @BotFather."
        )

    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    dp.message.register(cmd_start, Command("start"))
    dp.message.register(cmd_help, Command("help"))
    dp.message.register(cmd_generate, Command("generate"))
    dp.message.register(check_password, F.text)

    logger.info("Бот запущен")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())