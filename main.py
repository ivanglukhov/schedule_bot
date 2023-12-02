from model import schedule
import telebot
token = "6548534848:AAEI-ddGiV0BQe8grWlgztOEtjdwEK2JwCU"
bot = telebot.TeleBot(token)
schedule1 = schedule()

button_list = [
    telebot.types.InlineKeyboardButton(text='Расписание недели', callback_data='show_all_days'),
    telebot.types.InlineKeyboardButton(text='Удалить день', callback_data='delete_by_date'),
]

delete_flag = False



@bot.message_handler(commands=['start'])
def start(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    for i in button_list:
        keyboard.add(i)
    bot.send_message(message.chat.id, text='Действие', reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
def show_all_days(call):
    if call.data == 'show_all_days':
        for day in schedule1.select_all_days():
            s = 'Дата: '+str(day[1]) + '\n'
            s += 'Кол-во уроков: '+str(day[2])+ '\n'
            s += 'Место проведения: '+str(day[3])+ '\n'
            s += 'Уроки: '+str(day[4])
            bot.send_message(call.message.chat.id, s)
    if call.data == 'delete_by_date':
        global delete_flag
        delete_flag = True

        bot.send_message(call.message.chat.id, 'Введите дату')
    
@bot.message_handler(content_types=['text'])
def delete_day(message):
    if delete_flag == True:
        date = message.text
        schedule1.delete_by_date(date)

bot.polling(none_stop=True)