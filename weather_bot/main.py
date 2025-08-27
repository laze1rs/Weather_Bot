import telebot
from telebot.types import *
import requests
from API.config import TOKEN, API_KEY

bot = telebot.TeleBot(TOKEN)
API = API_KEY

#Commands to enter city
@bot.message_handler(commands=['start', 'weather'])
def start(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    weather1 = KeyboardButton(text='/weather')#Command to enter city
    markup.add(weather1)
    bot.send_message(message.chat.id, 'Hi, please tell me name of city to get weather.', reply_markup=markup)

#Find out the city from the user and getting weather
@bot.message_handler(func=lambda message: True)
def weather(message):
    try:
        city = message.text.strip().lower()
        res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&units=metric')
        bot.send_message(message.chat.id, f'Temp in degrees Celsius:  {res.json()['main']['temp']}')
        bot.send_message(message.chat.id, f'Wind speed(m/s): {res.json()["wind"]["speed"]}')
    except Exception: #exception to get sure that user entered real city
        bot.send_message(message.chat.id, 'Please enter a city name')
        bot.register_next_step_handler(message, weather)

bot.polling(none_stop=True)