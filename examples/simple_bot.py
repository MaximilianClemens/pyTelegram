import telegram
from secret import API_TOKEN

bot = telegram.Bot(API_TOKEN)

@bot.command('/start', 'Hallo Welt')
def start():
    return 'Hallo Welt!'

bot.start()
