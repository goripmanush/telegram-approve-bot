import telebot

# Bot Token for @TradeLifeApproveBot
TOKEN = "8742755067:AAED_xD9uLZE0NH6K9av7uMDFnVpzvHJxhs"
bot = telebot.TeleBot(TOKEN)

@bot.chat_join_request_handler()
def auto_approve(chat_join_request):
    try:
        # Approve user request instantly
        bot.approve_chat_join_request(chat_join_request.chat.id, chat_join_request.from_user.id)
        print(f"Successfully Approved: {chat_join_request.from_user.first_name}")
    except Exception as e:
        print(f"Error approving member: {e}")

if __name__ == "__main__":
    print("Auto-Approve Bot is running perfectly...")
    bot.infinity_polling()
  
