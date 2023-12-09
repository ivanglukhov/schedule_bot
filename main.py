from model import schedule
import telebot
token = "6548534848:AAEI-ddGiV0BQe8grWlgztOEtjdwEK2JwCU"
bot = telebot.TeleBot(token)
schedule1 = schedule()

button_list = [
    telebot.types.InlineKeyboardButton(text='Расписание недели', callback_data='show_all_days'),
    telebot.types.InlineKeyboardButton(text='Удалить день', callback_data='delete_by_date'),
    telebot.types.InlineKeyboardButton(text='Добавить день', callback_data='add_new_day'),
]

delete_flag = False

keyboard = telebot.types.InlineKeyboardMarkup()
for i in button_list:
    keyboard.add(i)

params_new_day_count = 0
new_day = ['','','','']
params_new_day_desc = [
    'Введите кол-во уроков: ',
    'Введите место: ',
    'Введите уроки: ',
]
def add_new_day(message):
    global params_new_day_count
    if params_new_day_count == 3:
        new_day[params_new_day_count] = message.text
        schedule1.create_day(new_day[0], new_day[1], new_day[2], new_day[3])
        bot.send_message(message.chat.id, text='Действие', reply_markup=keyboard)
    else:
        new_day[params_new_day_count] = message.text
        params_new_day_count += 1
        bot.send_message(message.chat.id, text=params_new_day_desc[params_new_day_count-1])
        bot.register_next_step_handler(message, add_new_day)
    print(params_new_day_count, new_day)


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, text='Действие', reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
def call_handler(call):
    if call.data == 'show_all_days':
        if len(schedule1.select_all_days()) > 0:
            for day in schedule1.select_all_days():
                s = 'Дата: '+str(day[1]) + '\n'
                s += 'Кол-во уроков: '+str(day[2])+ '\n'
                s += 'Место проведения: '+str(day[3])+ '\n'
                s += 'Уроки: '+str(day[4])
                bot.send_message(call.message.chat.id, s)
        else:
            bot.send_message(call.message.chat.id, 'Нет записей')
    if call.data == 'add_new_day':
        bot.send_message(call.message.chat.id, 'Введите дату:')
        bot.register_next_step_handler(call.message, add_new_day)


    #bot.send_message(call.message.chat.id, text='Действие', reply_markup=keyboard)


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
