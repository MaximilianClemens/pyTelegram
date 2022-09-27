import asyncio
import telegram
from secret import API_TOKEN

bot = telegram.Bot(API_TOKEN)

# Register Commands
@bot.command('/start', 'Hello World')
async def start(conversation):
    conversation.send('Hello World!')

@bot.command('/name', 'What\'s your Name?')
async def name(conversation):
    conversation.send('What\'s your Name?')
    while True:
        # TODO: Cancle when user sends other command
        response = await asyncio.create_task(conversation.get_response())
        if response.text:
            conversation.send(f'Hello {response.text}')
            break
        else:
            conversation.send('Please enter your Name.')

bot.update_commands()

# Run it..
bot.start()
