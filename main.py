import telebot
import requests
import time
import threading
import random

# ==========================================
# 🔑 TOKENS & CONFIGURATION
# ==========================================
APPROVE_TOKEN = "8742755067:AAED_xD9uLZE0NH6K9av7uMDFnVpzvHJxhs"
ALERT_TOKEN = "8854485261:AAH9e9SHq2xAcY6ABBIhqmfM21EUjyYh2Bw"
MEME_TOKEN = "7549790569:AAGk-9atIfsDKEj83jtHooM4MSKd04ZARx8"
LIKE_TOKEN_1 = "7126896765:AAF3YK18lMHY-IBe6Dc7c2mwAJ2ZxsyEfOI"
LIKE_TOKEN_2 = "7595974396:AAHO_cPoA-BjXhkoz5G4lENV9jPESzR2GjA"

CHANNEL_ID = "@Tradecryptolife"

# Bot Instances
approve_bot = telebot.TeleBot(APPROVE_TOKEN)
meme_bot = telebot.TeleBot(MEME_TOKEN)
like_bot = telebot.TeleBot(LIKE_TOKEN_1)

# ==========================================
# 1. AUTO APPROVE BOT (@TradeLifeApproveBot)
# ==========================================
@approve_bot.chat_join_request_handler()
def auto_approve(message):
    try:
        approve_bot.approve_chat_join_request(message.chat.id, message.from_user.id)
        print(f"✅ Approved User: {message.from_user.first_name}")
    except Exception as e:
        print(f"Approve Error: {e}")

def run_approve_bot():
    print("🚀 Auto-Approve Bot Running...")
    try:
        approve_bot.remove_webhook() # 🔥 Webhook error fix
        time.sleep(1)
        approve_bot.infinity_polling()
    except Exception as e:
        print(f"Approve Polling Error: {e}")

# ==========================================
# 2. CRYPTO ALERT BOT (0.5% UP/DOWN)
# ==========================================
COINS = "bitcoin,ethereum,binancecoin,solana,ripple,cardano,dogecoin,toncoin,ondo-us-dollar-yield"
API_URL = "https://api.coingecko.com/api/v3/coins/markets"

def get_prices():
    try:
        params = {'vs_currency': 'usd', 'ids': COINS, 'order': 'market_cap_desc'}
        response = requests.get(API_URL, params=params, timeout=10)
        if response.status_code == 200:
            return {coin['id']: coin['current_price'] for coin in response.json()}
    except Exception as e:
        print(f"API Error: {e}")
    return None

def send_alert(message):
    url = f"https://api.telegram.org/bot{ALERT_TOKEN}/sendMessage"
    payload = {"chat_id": CHANNEL_ID, "text": message, "parse_mode": "Markdown"}
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print(f"Alert Send Error: {e}")

def run_crypto_alert():
    print("🚀 Crypto 0.5% Alert Bot Running...")
    last_prices = get_prices()
    while True:
        time.sleep(60) # Checks price every 60 seconds
        current_prices = get_prices()
        if not current_prices or not last_prices:
            continue

        for coin_id, current_price in current_prices.items():
            last_price = last_prices.get(coin_id)
            if not last_price:
                continue
            
            change = ((current_price - last_price) / last_price) * 100
            coin_name = coin_id.upper()
            
            if change >= 0.5:
                send_alert(f"🟢 *PUMP ALERT*\n\n🪙 Coin: #{coin_name}\n💰 Price: ${current_price:,.4f}\n📈 Change: +{change:.2f}%\n⏱️ Interval: Last 1 Min")
            elif change <= -0.5:
                send_alert(f"🔴 *DUMP ALERT*\n\n🪙 Coin: #{coin_name}\n💰 Price: ${current_price:,.4f}\n📉 Change: {change:.2f}%\n⏱️ Interval: Last 1 Min")
        last_prices = current_prices

# ==========================================
# 3. CRYPTO MEME BOT (@GoogleWab3bot)
# ==========================================
MEMES = [
    "😂 Checked my crypto portfolio today... Even my stablecoins are crying. 📉 #CryptoLife",
    "🚀 Buying the dip of the dip of the dip... Help, I am officially out of money! 📉💀",
    "😎 Me explaining to my family why holding 100 million meme coins is a solid retirement plan. 🐕🪙",
    "📉 Bitcoin drops 1%: *Panic Sell!*\n📈 Bitcoin pumps 1%: *Where is my Lamborghini?* 🏎️",
    "🥱 Sleep is for people who don't trade crypto. We watch charts 24/7. 📊👁️",
    "🤑 Buy High, Sell Low. This is the ultimate crypto trader strategy! 💸📉"
]

def run_meme_bot():
    print("🚀 Meme Bot Running...")
    while True:
        try:
            meme_bot.send_message(CHANNEL_ID, random.choice(MEMES))
            print("✅ Meme Posted!")
        except Exception as e:
            print(f"Meme Error: {e}")
        time.sleep(7200) # Posts a meme every 2 hours (7200 seconds)

# ==========================================
# 4 & 5. AUTO REACTION BOTS (Emoji Likes)
# ==========================================
EMOJIS = ["🔥", "🥰", "🤣", "⭐", "👍", "🚀", "👏", "❤️"]

@like_bot.channel_post_handler()
def auto_react(message):
    try:
        emoji1 = random.choice(EMOJIS)
        emoji2 = random.choice(EMOJIS)
        
        # Bot 1 Reaction (@Sstetn_bot)
        like_bot.set_message_reaction(message.chat.id, message.message_id, [telebot.types.ReactionTypeEmoji(emoji1)], is_big=False)
        
        # Bot 2 Reaction (@BTCUSwalletbot) via API Call
        url = f"https://api.telegram.org/bot{LIKE_TOKEN_2}/setMessageReaction"
        payload = {"chat_id": message.chat.id, "message_id": message.message_id, "reaction": [{"type": "emoji", "emoji": emoji2}]}
        requests.post(url, json=payload)
        
        print(f"✅ Reacted with {emoji1} & {emoji2}")
    except Exception as e:
        print(f"Reaction Error: {e}")

def run_like_bot():
    print("🚀 Auto Like/React Bots Running...")
    try:
        like_bot.remove_webhook() # 🔥 Webhook error fix
        time.sleep(1)
        like_bot.infinity_polling()
    except Exception as e:
        print(f"Like Bot Polling Error: {e}")

# ==========================================
# 🔥 MAIN RUNNER
# ==========================================
if __name__ == "__main__":
    print("🌟 System Starting: Cleaning old connections & Running all 5 Bots...")
    
    threading.Thread(target=run_approve_bot, daemon=True).start()
    threading.Thread(target=run_crypto_alert, daemon=True).start()
    threading.Thread(target=run_meme_bot, daemon=True).start()
    threading.Thread(target=run_like_bot, daemon=True).start()
    
    while True:
        time.sleep(1)

