import telegram
from secret import API_TOKEN

bot = telegram.Bot(API_TOKEN)

# Register Commands
@bot.command('/start', 'Hello World')
def start():
    return 'Hello World!'

# Run it..
bot.start()
