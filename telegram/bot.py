import requests
import time
from threading import Lock
import asyncio

import logging


from .conversation import Conversation

class Bot(object):

    def __init__(self, token, session=None):
        """ Telegram Bot """

        # API Access
        self.baseurl = 'https://api.telegram.org'
        self.token = token
        self.logger = logging.getLogger('telegrambot')

        # Bot Commands
        self.commands = {}

        # Bot internal
        self.run = True
        self.session = session
        self.conversations = {}
        self.lock = Lock()

        if not self.session:
            self.session = requests.Session()
            self.session.headers.update(
                {
                    'User-Agent': 'PyTelegram (0.1, +https://github.com/MaximilianClemens/pytelegram)'
                }
            )

    def _request(self, method, action, params, return_json=True):
        """ Internal Requests Wrapper Function """

        # TODO: Error Handling
        response = self.session.request(
            method,
            f'{self.baseurl}/bot{self.token}/{action}',
            json=params
        )

        if return_json:
            return response.json()
        else:
            return response

    def _get(self, action, params=None, return_json=True):
        """ Wrapper for GET-Requests """

        return self._request('GET', action, params, return_json)

    def _post(self, action, params=None, return_json=True):
        """ Wrapper for POST-Requests """

        return self._request('POST', action, params, return_json)

    def command(self, description='No description', hide=False):
        """ Add new command to Bot """

        return lambda function: self.commands.update({
            function.__name__: {
                'function': function,
                'description': description,
                'hide': hide
            }
        })

    def register_handler(self, type):
        pass

    def update_commands(self):
        """ Update Bot Commands """
        
        command_list = []
        for command, data in self.commands.items():
            command_list.append({
                'command': command,
                'description': data['description']
            })

        print(command_list)
            
        self._post('setMyCommands', {
            'commands': command_list
        })

        return self._get('getMyCommands')
    
    def start(self):
        asyncio.run(self.main())

    async def main(self):
        """ Start Bot execution """

        tasks = set()

        offset = 0
        while self.run:
            for update in self._get('getUpdates', {'offset': offset})['result']:
                #print(update)
                if 'message' not in update.keys():
                    # ignore edited messages
                    continue
                chat_id = update['message']['chat']['id']
                from_id = update['message']['from']['id']
                
                identifier = f'{chat_id}-{from_id}'

                conversation = None

                with self.lock:
                    conversion_running = (identifier in self.conversations.keys())
                    is_text = ('text' in update['message'].keys())
                    is_command = (update['message']['text'][0] == '/') if is_text else False
            
                    if is_command:
                        if conversion_running:
                            self.conversations[identifier].execution = False
                        conversation = Conversation(self)
                        conversation.chat_id = chat_id
                        conversation.from_id = from_id
                        conversation.identifier = identifier
                        self.conversations[identifier] = conversation
                        task = asyncio.create_task(conversation.execute(update))
                        tasks.add(task)
                        task.add_done_callback(tasks.discard)
                    elif conversion_running:
                        conversation = self.conversations[identifier]
                        conversation.push(update)

                if update['update_id'] >= offset:
                    offset = update['update_id']+1

            # TODO: Check api rate limit
            await asyncio.sleep(0.5)

        for task in tasks:
            await asyncio.wait({task}, timeout=5.0)
