import asyncio
import time

class Conversation(object):

    def __init__(self, bot):
        self.bot = bot
        self.updates = []

        self.chat_id = None
        self.from_id = None
        self.identifier = None

    async def execute(self, update):
        try:
            self.push(update)
            command = self.updates[0].text.split(' ')[0]
            
            if command in self.bot.commands.keys():
                self.bot.commands[command](self)
            else:
                self.send('Unbekannter Befehl')

            with self.bot.lock:
                self.bot.conversations.pop(self.identifier, None)

            #    await asyncio.sleep(1)

        except:
            print("An exception occurred")

    #def wait_for_update(self):
    #    while True:
    #        print('he')
    #        if len(self.updates) > 1:
    #            return self.updates[1]
    #        time.sleep(1)
            

    def send(self, message):
        params = {"chat_id": self.chat_id, "text": message}
        self.bot._post('sendMessage', params)

    def push(self, update_raw):
        update = Update(update_raw)
        print(f'[{update.chat_id}]{update.from_username}: {update.text}')
        
        self.updates.append(update)
        

class Update(object):

    def __init__(self, update_raw):
        # TODO: check Type
        
        self.update_raw = update_raw
        self.chat_id = update_raw['message']['chat']['id']
        self.from_id = update_raw['message']['from']['id']
        self.from_username = update_raw['message']['from']['username']

        self.text = update_raw['message']['text']
