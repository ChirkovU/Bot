import os
import telebot
import random
import time

TOKEN = "8728613990:AAHTYer9gDoaaApQQJsFnhOxskQoP66HBHE"
bot = telebot.TeleBot(TOKEN)
USER_DATA = {}

def init_user(uid, name):
    if uid not in USER_DATA:
        USER_DATA[uid] = {"balance": 500, "bank": 0, "name": name, "last_work": 0}

@bot.message_handler(commands=['start', 'help'])
def help_cmd(message):
    init_user(message.from_user.id, message.from_user.first_name)
    menu = (
        "🎮 ИГРОВОЕ МЕНЮ:\n\n"
        "• Профиль — Ваша статистика\n"
        "• Баланс — Деньги в кармане\n"
        "• Банк [сумма] — Положить в банк\n"
        "• Снять [сумма] — Снять из банка\n"
        "• Работа — Заработать (раз в 60 сек)\n"
        "• Казино [ставка] — Игра X2 или слив"
    )
    bot.send_message(message.chat.id, menu)

@bot.message_handler(func=lambda m: m.text.lower() == 'профиль')
def profile_cmd(message):
    uid = message.from_user.id
    init_user(uid, message.from_user.first_name)
    u = USER_DATA[uid]
    bot.send_message(message.chat.id, f"👤 Игрок: {u['name']}\n🆔 ID: {uid}\n💵 На руках: {u['balance']}\n🏦 В банке: {u['bank']}")

@bot.message_handler(func=lambda m: m.text.lower() == 'баланс')
def balance_cmd(message):
    uid = message.from_user.id
    init_user(uid, message.from_user.first_name)
    bot.send_message(message.chat.id, f"💰 Ваш баланс: {USER_DATA[uid]['balance']} монет.")

@bot.message_handler(func=lambda m: m.text.lower() == 'работа')
def work_cmd(message):
    uid = message.from_user.id
    init_user(uid, message.from_user.first_name)
    u = USER_DATA[uid]
    curr = time.time()
    
    if curr - u["last_work"] < 60:
        bot.send_message(message.chat.id, f"⏳ Отдыхайте еще {int(60 - (curr - u['last_work']))} сек.")
        return
        
    earn = random.randint(30, 80)
    u["balance"] += earn
    u["last_work"] = curr
    bot.send_message(message.chat.id, f"🔨 Вы поработали и получили {earn} монет!")

@bot.message_handler(func=lambda m: m.text.lower().startswith(('банк ', 'снять ')))
def bank_cmd(message):
    uid = message.from_user.id
    init_user(uid, message.from_user.first_name)
    u = USER_DATA[uid]
    parts = message.text.split()
    
    if len(parts) < 2 or not parts[1].isdigit():
        return
    amt = int(parts[1])

    if parts[0].lower() == 'банк':
        if u["balance"] < amt: return bot.send_message(message.chat.id, "❌ Нет денег.")
        u["balance"] -= amt; u["bank"] += amt
        bot.send_message(message.chat.id, f"🏦 Положили {amt} в банк.")
    else:
        if u["bank"] < amt: return bot.send_message(message.chat.id, "❌ Нет денег в банке.")
        u["bank"] -= amt; u["balance"] += amt
        bot.send_message(message.chat.id, f"🏦 Сняли {amt} со счета.")

@bot.message_handler(func=lambda m: m.text.lower().startswith('казино '))
def casino_cmd(message):
    uid = message.from_user.id
    init_user(uid, message.from_user.first_name)
    u = USER_DATA[uid]
    parts = message.text.split()
    
    if len(parts) < 2 or not parts[1].isdigit(): return
    bet = int(parts[1])
    if bet <= 0 or u["balance"] < bet: return bot.send_message(message.chat.id, "❌ Неверная ставка.")
        
    if random.choice([True, False]):
        u["balance"] += bet
        bot.send_message(message.chat.id, f"🔴 ПОБЕДА! +{bet} монет. Баланс: {u['balance']}")
    else:
        u["balance"] -= bet
        bot.send_message(message.chat.id, f"⚫️ СЛИВ! -{bet} монет. Баланс: {u['balance']}")

print("Бот готов к запуску!")
bot.infinity_polling()
