from statistics import covariance
import telegram
from secret import API_TOKEN

bot = telegram.Bot(API_TOKEN)

# Register Commands
@bot.command('/start', 'Hello World')
def start(conversation):
    conversation.send('Hello World!')

bot.update_commands()

# Run it..
bot.start()
