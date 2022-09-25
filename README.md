== Python Telegram Bot ==
Build your own Telegram-Bot in seconds..
```python
import telegram

token = '0123456789:YourToken'
bot = telegram.Bot(token)

# Register Commands
@bot.command('/start', 'Hello World')
def start():
    return 'Hello World!'

# Run it..
bot.start()

```
![Image of Sample](https://raw.githubusercontent.com/MaximilianClemens/pytelegram/main/.github/images/simple_bot.jpg)
