import time
import requests
import schedule
from flask import Flask
from threading import Thread

# --- Flask Web Server Setup (To keep Render alive) ---
app = Flask('')

@app.route('/')
def home():
    return "Bot is running 24/7!"

def run_web_server():
    app.run(host='0.0.0.0', port=8080)

# --- TELEGRAM CONFIGURATION ---
CHANNEL_ID = "@Tradecryptolife"

TOKEN_1 = "8742755067:AAED_xD9uLZE0NH6K9av7uMDFnVpzvHJxhs"   # Crypto Alert Bot
TOKEN_2 = "8854485261:AAH9e9SHq2xAcY6ABBIhqmfM21EUjyYh2Bw"   # Meme Bot
TOKEN_3 = "7549790569:AAGk-9atIfsDKEj83jtHooM4MSKd04ZARx8"   # Quotes Bot

REACTION_BOTS = [
    "7126896765:AAF3YK18lMHY-IBe6Dc7c2mwAJ2ZxsyEfOI",  # Bot 4
    "7595974396:AAHO_cPoA-BjXhkoz5G4lENV9jPESzR2GjA",  # Bot 5
    "7988071625:AAHV1QNvzdxXlfybIVwNX4fIiGbkdP-H7R8",  # Bot 6
    "7960741317:AAGkCsoTL-9uE9LLdynVgV5XhGb354opKY4"   # Bot 7
]

EMOJIS = ["🥰", "❤️", "🔥", "🤣", "🐳"]

COIN_IDS = [
    "bitcoin", "ethereum", "binancecoin", "ripple", "solana", "cardano", "dogecoin", "polkadot", 
    "polygon", "shiba-inu", "tron", "litecoin", "uniswap", "avalanche-2", "chainlink", "stellar",
    "cosmos", "okb", "ethereum-classic", "near", "monero", "filecoin", "lido-dao", "aptos", 
    "hedera-hashgraph", "vechain", "internet-computer", "kaspa", "fantom", "optimism"
]

price_cache = {}

def give_reactions(message_id):
    print(f"⚡ [Reaction System] Reacting to post ID: {message_id}")
    for i, bot_token in enumerate(REACTION_BOTS):
        if i < len(EMOJIS):
            emoji = EMOJIS[i]
            url = f"https://api.telegram.org/bot{bot_token}/setMessageReaction"
            payload = {
                "chat_id": CHANNEL_ID,
                "message_id": message_id,
                "reaction": [{"type": "emoji", "emoji": emoji}],
                "is_big": True
            }
            try:
                requests.post(url, json=payload)
                time.sleep(0.5)
            except Exception as e:
                print(f"Reaction Error (Bot {i+4}): {e}")

def check_crypto_prices():
    global price_cache
    print("🔄 [Bot 1] Checking crypto prices...")
    ids_string = ",".join(COIN_IDS)
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={ids_string}&vs_currencies=usd"
    
    try:
        response = requests.get(url).json()
        for coin in COIN_IDS:
            if coin in response:
                current_price = response[coin]['usd']
                if coin in price_cache:
                    old_price = price_cache[coin]
                    change = ((current_price - old_price) / old_price) * 100
                    
                    if abs(change) >= 0.5:
                        emoji = "📈" if change > 0 else "📉"
                        msg = f"{emoji} **{coin.upper()} Alert!**\n\nPrice: ${current_price:,.4f}\nChange: {change:+.2f}%"
                        url_send = f"https://api.telegram.org/bot{TOKEN_1}/sendMessage"
                        r = requests.post(url_send, data={"chat_id": CHANNEL_ID, "text": msg, "parse_mode": "Markdown"}).json()
                        if r.get('ok'):
                            give_reactions(r['result']['message_id'])
                            
                price_cache[coin] = current_price
    except Exception as e:
        print(f"Crypto Alert Error: {e}")

def post_meme():
    print("🖼️ [Bot 2] Fetching and posting a meme...")
    try:
        res = requests.get("https://meme-api.com/gimme/wholesomememes").json()
        if 'url' in res:
            meme_url = res['url']
            caption = res.get('title', 'Crypto Life Meme! 😂')
            url_send = f"https://api.telegram.org/bot{TOKEN_2}/sendPhoto"
            r = requests.post(url_send, data={"chat_id": CHANNEL_ID, "photo": meme_url, "caption": caption}).json()
            if r.get('ok'):
                give_reactions(r['result']['message_id'])
    except Exception as e:
        print(f"Meme Poster Error: {e}")

def post_crypto_quotes():
    print("💡 [Bot 3] Posting Daily Trading Tip...")
    msg = "💡 **Tip of the day:** Always manage your risk before looking at profits! 🚀\n\n#TradingTips"
    url_send = f"https://api.telegram.org/bot{TOKEN_3}/sendMessage"
    r = requests.post(url_send, data={"chat_id": CHANNEL_ID, "text": msg, "parse_mode": "Markdown"}).json()
    if r.get('ok'):
        give_reactions(r['result']['message_id'])

# --- SCHEDULER SETTINGS ---
schedule.every(5).minutes.do(check_crypto_prices)
schedule.every().day.at("12:00").do(post_meme)
schedule.every().day.at("21:00").do(post_crypto_quotes)

if __name__ == "__main__":
    print("=========================================")
    print("🚀 Starting Web Server and Bots...")
    print("=========================================")
    
    # Start the web server in a background thread
    t = Thread(target=run_web_server)
    t.start()
    
    # Run initial price check
    check_crypto_prices()
    
    while True:
        schedule.run_pending()
        time.sleep(1)

