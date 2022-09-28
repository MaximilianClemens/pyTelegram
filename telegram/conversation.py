import asyncio
import time

class Conversation(object):

    def __init__(self, bot):
        self.bot = bot
        self.updates = []

        self.chat_id = None
        self.from_id = None
        self.identifier = None
        self.execution = True

    async def execute(self, update):
        command = ''
        try:
            self.push(update)
            command = self.updates[0].text.split(' ')[0]
            self.updates[0].read = True
            if command in self.bot.commands.keys():
                await asyncio.create_task(self.bot.commands[command](self))
            else:
                self.send('Unbekannter Befehl')

        except Exception:
            #self.bot.logger.error("Fatal error in main loop", exc_info=True)

            if not self.execution:
                self.send(f'[Command {command} aborted.]')
        finally:
            self.cleanup()

    def cleanup(self):
        with self.bot.lock:
            self.bot.conversations.pop(self.identifier, None)

    async def get_response(self):
        while self.execution:
            for update in self.updates:
                if not update.read:
                    update.read = True
                    return update
            await asyncio.sleep(0.5)
        if not self.execution:
            raise Exception('Conversation aborted')

    def send(self, message):
        params = {"chat_id": self.chat_id, "text": message}
        self.bot._post('sendMessage', params)
        print(f'[{self.chat_id}]BOT: {message}')

    def push(self, update_raw):
        update = Update(update_raw)
        if update.text:
            print(f'[{update.chat_id}]{update.from_username}: {update.text}')
        else:
            print(f'[{update.chat_id}]{update.from_username}: {update.type}')

        self.updates.append(update)


class Update(object):

    def __init__(self, update_raw):
        self.update_raw = update_raw
        self.chat_id = update_raw['message']['chat']['id']
        self.from_id = update_raw['message']['from']['id']
        self.from_username = update_raw['message']['from']['username']

        self.type = 'unkn'
        self.text = None
        self.document = None
        self.photo = None

        if 'text' in update_raw['message']:
            self.text = update_raw['message']['text']
            self.type = 'text'
        if 'document' in update_raw['message']:
            self.document = update_raw['message']['document']
            self.type = 'document'
        if 'photo' in update_raw['message']:
            self.photo = update_raw['message']['photo']
            self.type = 'photo'

        self.read = False
