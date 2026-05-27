import os
import time
import requests
import logging
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, MessageHandler, filters, ContextTypes
import asyncio

# Setup logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# --- CONFIGURATION (Get from Render Environment Variables) ---
CHANNEL_ID = os.getenv("CHANNEL_ID")  # Format: @Tradecryptolife or -100xxxxxxxxx
MEME_BOT_TOKEN = os.getenv("MEME_BOT_TOKEN")
ALERT_BOT_TOKEN = os.getenv("ALERT_BOT_TOKEN")
LIKE_BOT_TOKEN = os.getenv("LIKE_BOT_TOKEN")

# Initialize Bots
meme_bot = Bot(token=MEME_BOT_TOKEN) if MEME_BOT_TOKEN else None
alert_bot = Bot(token=ALERT_BOT_TOKEN) if ALERT_BOT_TOKEN else None

# Track crypto prices for alerts
LAST_PRICES = {"bitcoin": 0.0, "ethereum": 0.0}

# --- TASK 1: CRYPTO MEME POSTER ---
async def post_crypto_meme():
    if not meme_bot or not CHANNEL_ID:
        return
    try:
        # Fetching a random meme from a meme API or Reddit
        response = requests.get("https://meme-api.com/gimme/cryptocurrencymemes").json()
        meme_url = response.get("url")
        if meme_url:
            await meme_bot.send_photo(chat_id=CHANNEL_ID, photo=meme_url, caption="😂 Stay updated, stay ahead! #CryptoMeme")
            logging.info("Meme posted successfully!")
    except Exception as e:
        logging.error(f"Error posting meme: {e}")

async def meme_scheduler():
    while True:
        await post_crypto_meme()
        await asyncio.sleep(14400) # Posts a meme every 4 hours (14400 seconds)

# --- TASK 2: CRYPTO PRICE ALERT (0.5% Change) ---
async def check_crypto_prices():
    global LAST_PRICES
    if not alert_bot or not CHANNEL_ID:
        return
    try:
        # Fetch top crypto prices from CoinGecko
        url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd"
        data = requests.get(url).json()
        
        for coin in ["bitcoin", "ethereum"]:
            current_price = data[coin]["usd"]
            last_price = LAST_PRICES[coin]
            
            if last_price != 0.0:
                # Calculate percentage change
                percent_change = ((current_price - last_price) / last_price) * 100
                
                if abs(percent_change) >= 0.5:
                    direction = "🚀 UP" if percent_change > 0 else "🔻 DOWN"
                    message = f"⚠️ **Crypto Alert!**\n\n🪙 #{coin.upper()} has gone {direction} by {abs(percent_change):.2f}%\n💵 Current Price: ${current_price:,}"
                    await alert_bot.send_message(chat_id=CHANNEL_ID, text=message, parse_mode="Markdown")
            
            LAST_PRICES[coin] = current_price
    except Exception as e:
        logging.error(f"Error checking prices: {e}")

async def price_alert_scheduler():
    while True:
        await check_crypto_prices()
        await asyncio.sleep(60) # Checks every 60 seconds

# --- TASK 3: AUTOMATIC INLINE EMOJI REACTION BUTTONS ---
async def add_reactions(update, context):
    # This triggers whenever a new post comes in the channel
    try:
        channel_post = update.channel_post
        if not channel_post:
            return
            
        # Create Emoji Buttons
        keyboard = [
            [
                InlineKeyboardButton("⭐ 0", callback_data="react_star"),
                InlineKeyboardButton("🤣 0", callback_data="react_laugh"),
                InlineKeyboardButton("🔥 0", callback_data="react_fire"),
                InlineKeyboardButton("♥️ 0", callback_data="react_love"),
                InlineKeyboardButton("🥰 0", callback_data="react_smile")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        # Edit the post to add buttons
        await context.bot.edit_message_reply_markup(
            chat_id=channel_post.chat_id,
            message_id=channel_post.message_id,
            reply_markup=reply_markup
        )
    except Exception as e:
        logging.error(f"Error adding reaction buttons: {e}")

# --- MAIN RUNNER ---
def main():
    # Start the Like/Reaction Bot Application listener
    if LIKE_BOT_TOKEN:
        app = Application.builder().token(LIKE_BOT_TOKEN).build()
        app.add_handler(MessageHandler(filters.ChatType.CHANNEL, add_reactions))
        
        # Get the event loop to run background tasks alongside the bot listener
        loop = asyncio.get_event_loop()
        loop.create_task(meme_scheduler())
        loop.create_task(price_alert_scheduler())
        
        logging.info("All bots are starting...")
        app.run_polling()
    else:
        print("Please provide a LIKE_BOT_TOKEN to start the bot runner.")

if __name__ == "__main__":
    main()

