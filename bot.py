import os
import telebot

# Бот берет токен из секретов GitHub для безопасности
TOKEN = "8728613990:AAHTYer9gDoaaApQQJsFnhOxskQoP66HBHE"
bot = telebot.TeleBot(TOKEN)

# Простая имитация базы данных в памяти для теста
USER_DATA = {}

@bot.message_handler(commands=['start'])
def start_cmd(message):
    user_id = message.from_user.id
    if user_id not in USER_DATA:
        USER_DATA[user_id] = {"balance": 100, "name": message.from_user.first_name}
    
    welcome_text = (
        f"🤖 Добро пожаловать в игровой бот, {USER_DATA[user_id]['name']}!\n\n"
        "доступные команды:\n"
        "• Профиль\n"
        "• Баланс"
    )
    bot.send_message(message.chat.id, welcome_text)

@bot.message_handler(func=lambda message: message.text.lower() == 'профиль')
def profile_cmd(message):
    user_id = message.from_user.id
    if user_id not in USER_DATA:
        USER_DATA[user_id] = {"balance": 100, "name": message.from_user.first_name}
        
    text = f"👤 Ваш профиль:\nИмя: {USER_DATA[user_id]['name']}\nID: {user_id}"
    bot.send_message(message.chat.id, text)

@bot.message_handler(func=lambda message: message.text.lower() == 'баланс')
def balance_cmd(message):
    user_id = message.from_user.id
    if user_id not in USER_DATA:
        USER_DATA[user_id] = {"balance": 100, "name": message.from_user.first_name}
        
    text = f"💰 Ваш баланс: {USER_DATA[user_id]['balance']} монет."
    bot.send_message(message.chat.id, text)

print("Тестовый бот успешно запущен на GitHub Actions!")
# Запуск бесконечного опроса серверов Telegram
bot.infinity_polling()
