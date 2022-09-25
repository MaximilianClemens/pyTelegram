import requests
import json
import time

class Bot(object):

    def __init__(self, token):
        """ Telegram Bot """
        
        self.token = token
        self.commands = {}
        self.run = True
        self.baseurl = 'https://api.telegram.org'
        self.command_desc = {}

    def command(self, command, desc=None):
        """ Add new command to Bot """
        if desc:
            self.command_desc[command] = desc

        return lambda f: self.commands.update({command: f})

    def start(self):
        """ Start Bot execution """
        # TODO: Update Bot commands 

        offset = 0
        while self.run:
            response_updates = requests.get('{}/bot{}/getUpdates?offset={}'.format(self.baseurl, self.token, offset))
            # TODO: check Statuscode
            # TODO: Handle errors
            data = response_updates.json()
            if data['ok']:
                # loop new Message
                # TODO: Handle more the 100 Messages?
                for update in data['result']:
                    # Handle Message from User
                    self.handle(update)
                    
                    # Update offset
                    if update['update_id'] >= offset:
                        offset = update['update_id']+1
            # TODO: Check api rate limit
            time.sleep(0.5)

    def handle(self, update):
        """ Handle new Message """
        
        username = update['message']['from']['username']
        text = update['message']['text']
        chat_id = update['message']['chat']['id']
        print('[{}]{}: {}'.format(chat_id, username, text))

        splitted_text = text.split(' ', 1)
        if splitted_text[0] in self.commands.keys():
            response = self.commands[splitted_text[0]](*splitted_text[1:])

            params = {"chat_id": chat_id, "text": response}
            message = requests.post('{}/bot{}/sendMessage'.format(self.baseurl, self.token), params=params)
