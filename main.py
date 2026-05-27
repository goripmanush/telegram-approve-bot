Here is the completely clean, English-configured code for your 7 Telegram bots. All your bot tokens, your channel link, and the auto-reaction systems are pre-configured.
### 🛠️ How to run the code:
**Step 1: Install Required Libraries**
Open your terminal or command prompt and run:
```bash
pip install requests schedule

```
**Step 2: Save and Run**
Save the code below into a file named trade_crypto_bot.py and run it:
```bash
python trade_crypto_bot.py

```
### 💻 Complete Python Code (trade_crypto_bot.py)
```python
import time
import requests
import schedule

# --- CONFIGURATION ---
CHANNEL_ID = "@Tradecryptolife"

# Bot Tokens Provided by You
TOKEN_1 = "8742755067:AAED_xD9uLZE0NH6K9av7uMDFnVpzvHJxhs"   # Crypto Alert Bot
TOKEN_2 = "8854485261:AAH9e9SHq2xAcY6ABBIhqmfM21EUjyYh2Bw"   # Meme Bot
TOKEN_3 = "7549790569:AAGk-9atIfsDKEj83jtHooM4MSKd04ZARx8"   # Quotes Bot

# List of 4 Bots assigned for Auto-Reactions
REACTION_BOTS = [
    "7126896765:AAF3YK18lMHY-IBe6Dc7c2mwAJ2ZxsyEfOI",  # Bot 4
    "7595974396:AAHO_cPoA-BjXhkoz5G4lENV9jPESzR2GjA",  # Bot 5
    "7988071625:AAHV1QNvzdxXlfybIVwNX4fIiGbkdP-H7R8",  # Bot 6
    "7960741317:AAGkCsoTL-9uE9LLdynVgV5XhGb354opKY4"   # Bot 7
]

# Emojis for reactions
EMOJIS = ["🥰", "❤️", "🔥", "🤣", "🐳"]

# List of Crypto Coin IDs to track (CoinGecko API IDs)
COIN_IDS = [
    "bitcoin", "ethereum", "binancecoin", "ripple", "solana", "cardano", "dogecoin", "polkadot", 
    "polygon", "shiba-inu", "tron", "litecoin", "uniswap", "avalanche-2", "chainlink", "stellar",
    "cosmos", "okb", "ethereum-classic", "near", "monero", "filecoin", "lido-dao", "aptos", 
    "hedera-hashgraph", "vechain", "internet-computer", "kaspa", "fantom", "optimism"
]

price_cache = {}

# ----------------------------------------------------------------
# 🔥 AUTO REACTION SYSTEM
# ----------------------------------------------------------------
def give_reactions(message_id):
    """Triggers Bots 4, 5, 6, and 7 to react to the newly posted channel message"""
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
                time.sleep(0.5)  # Safe delay between bot reactions
            except Exception as e:
                print(f"Reaction Error (Bot {i+4}): {e}")

# ----------------------------------------------------------------
# 📈 1. CRYPTO PRICE MONITOR (Bot 1)
# ----------------------------------------------------------------
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
                
                # Check price movement if previous price exists in cache
                if coin in price_cache:
                    old_price = price_cache[coin]
                    change = ((current_price - old_price) / old_price) * 100
                    
                    # Trigger alert if movement is 0.5% or more
                    if abs(change) >= 0.5:
                        emoji = "📈" if change > 0 else "📉"
                        msg = f"{emoji} **{coin.upper()} Alert!**\n\nPrice: ${current_price:,.4f}\nChange: {change:+.2f}%"
                        
                        # Post alert to channel
                        url_send = f"https://api.telegram.org/bot{TOKEN_1}/sendMessage"
                        r = requests.post(url_send, data={"chat_id": CHANNEL_ID, "text": msg, "parse_mode": "Markdown"}).json()
                        
                        # Add automatic reactions to this post
                        if r.get('ok'):
                            give_reactions(r['result']['message_id'])
                            
                price_cache[coin] = current_price
    except Exception as e:
        print(f"Crypto Alert Error: {e}")

# ----------------------------------------------------------------
# 😂 2. AUTOMATIC MEME POSTER (Bot 2)
# ----------------------------------------------------------------
def post_meme():
    print("🖼️ [Bot 2] Fetching and posting a meme...")
    try:
        res = requests.get("https://meme-api.com/gimme/wholesomememes").json()
        if 'url' in res:
            meme_url = res['url']
            caption = res.get('title', 'Crypto Life Meme! 😂')
            
            # Post meme photo to channel
            url_send = f"https://api.telegram.org/bot{TOKEN_2}/sendPhoto"
            r = requests.post(url_send, data={"chat_id": CHANNEL_ID, "photo": meme_url, "caption": caption}).json()
            
            # Add automatic reactions to this post
            if r.get('ok'):
                give_reactions(r['result']['message_id'])
    except Exception as e:
        print(f"Meme Poster Error: {e}")

# ----------------------------------------------------------------
# 💡 3. DAILY TRADING TIPS / QUOTES (Bot 3)
# ----------------------------------------------------------------
def post_crypto_quotes():
    print("💡 [Bot 3] Posting Daily Trading Tip...")
    msg = "💡 **Tip of the day:** Always manage your risk before looking at profits! 🚀\n\n#TradingTips"
    
    url_send = f"https://api.telegram.org/bot{TOKEN_3}/sendMessage"
    r = requests.post(url_send, data={"chat_id": CHANNEL_ID, "text": msg, "parse_mode": "Markdown"}).json()
    
    if r.get('ok'):
        give_reactions(r['result']['message_id'])

# ----------------------------------------------------------------
# 🕒 SCHEDULER SETTINGS
# ----------------------------------------------------------------

# Checks prices every 5 minutes
schedule.every(5).minutes.do(check_crypto_prices)

# Posts a meme daily at 12:00 PM
schedule.every().day.at("12:00").do(post_meme)

# Posts trading tips daily at 9:00 PM (21:00)
schedule.every().day.at("21:00").do(post_crypto_quotes)

# --- MAIN LOOP ---
if __name__ == "__main__":
    print("=========================================")
    print("🚀 All 7 Bots are Configured and Starting...")
    print("🔥 Auto-Reaction System is ACTIVE!")
    print("=========================================")
    
    # Run an initial price check to set up initial price cache values
    check_crypto_prices()
    
    while True:
        schedule.run_pending()
        time.sleep(1)

```

