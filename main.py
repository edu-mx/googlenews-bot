from log import Logger
import rss
from user import User
from telebot import TeleBot

log = Logger()

langs = {
    'pt-br': 'Olá! 🌟 Seu idioma foi definido com sucesso para Português (Brasil). Agora pode escrever à vontade. 😊',
    'pt': 'Olá! 🌟 Seu idioma foi definido com sucesso para Português. Agora pode escrever à vontade. 😊',
    'en': 'Hello! 🌟 Your language has been successfully set to English. You can start writing freely. 😊',
    'es': '¡Hola! 🌟 Tu idioma se ha configurado con éxito como Español. Ahora puedes comenzar a escribir a tus anchas. 😊',
    'tr': 'Merhaba! 🌟 Diliniz başarıyla Türkçe olarak ayarlandı. Artık özgürce yazmaya başlayabilirsiniz. 😊',
    'fr': 'Bonjour ! 🌟 Votre langue a été configurée avec succès en français. Vous pouvez maintenant commencer à écrire librement. 😊',
    'ru': 'Привет! 🌟 Ваш язык успешно установлен как русский. Теперь вы можете начать писать на свободу. 😊',
    'de': 'Hallo! 🌟 Ihre Sprache wurde erfolgreich auf Deutsch festgelegt. Jetzt können Sie frei zu schreiben beginnen. 😊',
    'ja': 'こんにちは！ 🌟 言語が日本語に正常に設定されました。これで自由に書き始めることができます。 😊',
    'zh': '你好！ 🌟 您的语言已成功设置为中文。现在您可以自由地开始写作。 😊'
}

# the token is in token_bot.txt
def get_token_bot(filename='token_bot.txt'):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            token = file.read().strip()
            return token
    except FileNotFoundError as x:
        log.critical('Token not found %s' % x)
        exit('The token_bot.txt file does not exist, create it and add the bot token there;')

token_bot = get_token_bot()
if token_bot:
    bot = TeleBot(token_bot)
else:
    log.error('Token bot not found in file')
    exit('The file does not have a token, please open token_bot.txt and check its integrity.')

# explodes language buttons on the screen
temp_button = None
def keyboard_buttons(msg):
    markup = types.InlineKeyboardMarkup(row_width=2)
    for language in langs.keys():
        button = types.InlineKeyboardButton(language, callback_data=language)
        markup.add(button)
    buttons = bot.send_message(msg.chat.id, 'Choose your preferred language:', reply_markup=markup)
    return buttons.message_id

@bot.message_handler(commands=['help', 'reset', 'search'])
def commands(msg):
    global temp_button
    
    # searching  user language by ID
    data_json = User.get_user(msg.from_user.id)
    
    if msg.text == '/start':
        response = "Hi, I'm a news bot and I'll keep you posted!"
    elif msg.text == '/help':
        response = "I can search on themes, keywords and phrases. send something after /search and I'll tell you everything. Every hour I'll update you on what's going on, in case I hear anything else."
    bot.send_message(msg.chat.id, response)
    
    if data_json == None:
        temp_button = keyboard_buttons(msg)

@bot.callback_query_handler(func=lambda call: call.data in langs.keys())
def config_per_button(call):
    lang_code = call.data
    user_id = call.from_user.id
    user_name = call.from_user.first_name
    user_bot = User(user_id, name=user_name, search=None, lang=lang_code)
    
    if temp_button:
        # After choosing the language, the list of buttons disappears
        bot.delete_message(call.message.chat.id, button_id)
        bot.send_message(call.message.chat.id, langs[lang_code])
    else:
        bot.send_message(call.message.chat.id, '⚠ Error, please clear the conversation history with me so that everything works normally.')
        log.error("I couldn't delete the message with the buttons, I asked the user to clear the conversation.")
    
    if user_name and user_id and lang_code:
        user_bot.save_user()

print('Bot started')
try:
    bot.polling()
except Exception as x:
    print('O bot caiu, motivo: %s'%x)