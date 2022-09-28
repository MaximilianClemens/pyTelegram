# Python Telegram Bot
Simple Telegram Bot Library, example: 
```python
import telegram

token = '0123456789:YourToken'
bot = telegram.Bot(token)

# Register Commands
@bot.command('/start', 'Hello World')
async def start(conversation):
    conversation.send('Hello World!')

@bot.command('/name', 'What\'s your Name?')
async def name(conversation):
    conversation.send('What\'s your Name?')
    while True:
        response = await asyncio.create_task(conversation.get_response())
        if response.text:
            conversation.send(f'Hello {response.text}')
            break
        else:
            conversation.send('Please enter your Name.')

bot.update_commands()

# Run it..
bot.start()

```
![Image of Sample](https://raw.githubusercontent.com/MaximilianClemens/pytelegram/main/.github/images/simple_bot.jpg)

# Install

```
pip install requests
pip install git+hhttps://github.com/MaximilianClemens/pytelegram.git
```
