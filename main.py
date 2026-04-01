import os
import logging
import asyncio
from aiohttp import web
import google.generativeai as genai
from telegram import Update, InlineQueryResultGame, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler, InlineQueryHandler

# --- 1. SOZLAMALAR (O'zingiznikini yozing) ---
BOT_TOKEN = '8770553491:AAGmSVYbgz66eUCFXJyflUCZq9N2xtQeF6U'
GEMINI_API_KEY = 'AIzaSyDqD2SRHdmNsoTlG-FS0K-yMB9QnHbpSGo' # Google AI Studio-dan olgan kalitni shu yerga qo'ying
GAME_SHORT_NAME = 'play4096'
GAME_URL = 'https://shahzodagzamov06-sketch.github.io/4096-pro/'

# Gemini AI sozlamasi
genai.configure(api_key=GEMINI_API_KEY)
ai_model = genai.GenerativeModel('gemini-1.5-flash')

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# --- 2. RENDER UCHUN WEB SERVER (Port xatosini yo'qotish) ---
async def handle(request):
    return web.Response(text="Nexus AI 4096 Bot is Running!")

async def start_web_server():
    app = web.Application()
    app.router.add_get('/', handle)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.environ.get("PORT", 8080))
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    print(f"Web server started on port {port}")

# --- 3. BOT FUNKSIYALARI ---

# Start buyrug'i (O'yinni yuboradi)
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_game(GAME_SHORT_NAME)

# AI bilan gaplashish (/ask savol)
async def ask_ai(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_query = " ".join(context.args)
    if not user_query:
        await update.message.reply_text("Please ask a question! Example: /ask How to play?")
        return
    
    response = ai_model.generate_content(user_query)
    await update.message.reply_text(f"🤖 **Nexus AI:**\n\n{response.text}", parse_mode="Markdown")

# Play tugmasi bosilganda o'yinni ochish
async def game_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if query.game_short_name == GAME_SHORT_NAME:
        await query.answer(url=GAME_URL)

# Inline rejimda o'yinni qidirish
async def inline_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.inline_query.query
    results = [InlineQueryResultGame(id='1', game_short_name=GAME_SHORT_NAME)]
    await update.inline_query.answer(results)

# --- 4. ASOSIY ISHGA TUSHIRISH ---
async def main():
    # 1. Web serverni orqa fonda yurgizish (Render uchun)
    asyncio.create_task(start_web_server())

    # 2. Botni sozlash
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    
    # Handlerlarni qo'shish
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("ask", ask_ai))
    application.add_handler(CallbackQueryHandler(game_callback))
    application.add_handler(InlineQueryHandler(inline_query))

    # 3. Botni yurgizish
    async with application:
        await application.initialize()
        await application.start()
        await application.updater.start_polling()
        print("Bot is polling...")
        
        # Bot va Server to'xtab qolmasligi uchun cheksiz kutish
        while True:
            await asyncio.sleep(3600)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
