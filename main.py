from telegram import Update, InlineQueryResultGame, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler, InlineQueryHandler

# Replace these with your actual details
BOT_TOKEN = '8770553491:AAGmSVYbgz66eUCFXJyflUCZq9N2xtQeF6U'
GAME_SHORT_NAME = 'play4096'  # The Short Name you gave to BotFather
GAME_URL = 'https://shahzodagzamov06-sketch.github.io/4096-pro'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Sends the game when a user type /start."""
    await update.message.reply_game(GAME_SHORT_NAME)

async def game_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Answers the callback query when the 'Play' button is pressed."""
    query = update.callback_query
    if query.game_short_name == GAME_SHORT_NAME:
        # Telegram will open this URL in the in-app browser
        await query.answer(url=GAME_URL)

async def inline_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Allows users to share the game in any chat."""
    query = update.inline_query.query
    results = [
        InlineQueryResultGame(id='1', game_short_name=GAME_SHORT_NAME)
    ]
    await update.inline_query.answer(results)

if __name__ == '__main__':
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CallbackQueryHandler(game_callback))
    application.add_handler(InlineQueryHandler(inline_query))
    
    print("Bot is running...")
    application.run_polling()
