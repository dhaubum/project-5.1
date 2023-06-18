import telebot
import qrcode
import os
import concurrent.futures

bot = telebot.TeleBot('TOKEN')

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.reply_to(message, 'send the text that is needed in the qr code')

def generate_qr_code(message):
    text = message.text
    qr = qrcode.QRCode(version=10, box_size=10)
    qr.add_data(text.encode('utf-8'))
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    image_code = "qr_code.png"
    img.save(image_code)
    with open(image_code, "rb") as file:
        bot.send_photo(message.chat.id, file)
    os.remove(image_code)

@bot.message_handler(func=lambda message: True)
def process(message):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.submit(generate_qr_code, message)

bot.polling(none_stop=True)
