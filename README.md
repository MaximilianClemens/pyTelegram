#Python Telegram Bot
Simple Telegram Bot Library, example: 
```python
import telegram

token = '0123456789:YourToken'
bot = telegram.Bot(token)

# Register Commands
@bot.command('/start', 'Hello World')
def start(conversation):
    conversation.send('Hello World!')

# Run it..
bot.start()

```
![Image of Sample](https://raw.githubusercontent.com/MaximilianClemens/pytelegram/main/.github/images/simple_bot.jpg)
