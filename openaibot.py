import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import openai

# Получение токенов из переменных окружения
BOT_TOKEN = "8007113493:AAHhkVCFkxp5YrGJiXSE-tYf5o-ephLrO3g"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Проверяем, загружены ли токены
if not BOT_TOKEN:
    raise ValueError("Не найден BOT_TOKEN. Убедись, что переменная окружения установлена.")
if not OPENAI_API_KEY:
    raise ValueError("Не найден OPENAI_API_KEY. Убедись, что переменная окружения установлена.")

# Инициализация бота и OpenAI
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)
openai.api_key = OPENAI_API_KEY

# Создание клавиатуры для удобства
keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard.add(KeyboardButton("/help"))

# Обработчик команды /start
@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    await message.answer(
        "Привет! Я бот на базе ИИ. Напиши мне что-нибудь, и я постараюсь помочь!\n\n"
        "Ты можешь воспользоваться командой /help, чтобы узнать больше.",
        reply_markup=keyboard
    )

# Обработчик команды /help
@dp.message_handler(commands=["help"])
async def help_command(message: types.Message):
    await message.answer(
        "Вот что я умею:\n"
        "- Отвечать на твои вопросы.\n"
        "- Помогать с любыми задачами.\n\n"
        "Просто напиши мне сообщение, и я отвечу!"
    )

# Обработчик обычных сообщений
@dp.message_handler()
async def handle_message(message: types.Message):
    try:
        # Запрос к OpenAI
        response = openai.ChatCompletion.create(
            model="gpt-4o",  # Используем модель GPT-4o
            messages=[{"role": "user", "content": message.text}]
        )
        # Ответ пользователю
        reply = response["choices"][0]["message"]["content"]
        await message.answer(reply)
    except Exception as e:
        await message.answer("Произошла ошибка. Попробуй позже.")
        print(f"Ошибка: {e}")

if __name__ == "__main__":
    from aiogram.utils import executor
    print("Бот запущен!")
    executor.start_polling(dp, skip_updates=True)
