import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import WebAppInfo, ReplyKeyboardMarkup, KeyboardButton

# Replace with your API Token from BotFather
API_TOKEN = '8770553491:AAGmSVYbgz66eUCFXJyflUCZq9N2xtQeF6U'

# Configure logging
logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Create the keyboard with Web App button
def get_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    # Your game link
    web_app = WebAppInfo(url="https://shahzodagzamov06-sketch.github.io/4096-pro")
    button = KeyboardButton(text="🎮 Play 4096 Pro", web_app=web_app)
    keyboard.add(button)
    return keyboard

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply(
        "Welcome to 4096 Pro Bot! 🚀\n\n"
        "Experience the next level of the classic puzzle game. "
        "Click the button below to start playing directly inside Telegram!",
        reply_markup=get_keyboard()
    )

@dp.message_handler(commands=['help'])
async def send_help(message: types.Message):
    await message.reply(
        "How to play:\n"
        "1. Click the 'Play 4096 Pro' button.\n"
        "2. Swipe tiles to merge them.\n"
        "3. Reach the 4096 tile to win!\n\n"
        "Powered by Nexus AI Project."
    )

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
