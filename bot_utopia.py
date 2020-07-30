import time, amanobot, amanobot.helper, pprint, requests, re
from bs4 import BeautifulSoup
from amanobot.loop import MessageLoop
from amanobot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from amanobot.delegate import (per_chat_id, create_open, pave_event_space, include_callback_query_chat_id)


class opGG():
    def __init__(self, username):
        self.name = username
        self.solo = None
        self.flex = None

    def update(self):
        html = requests.get('https://br.op.gg/summoner/userName=' + self.name).text
        soup = BeautifulSoup(html, 'html.parser')
        try:
            self.solo = {
                'Wins': soup.find("span", {"class": "wins"}).text,
                'Losses': soup.find("span", {"class": "losses"}).text,
                'LP': re.search(r'\d*\s{0,1}LP', soup.find("span", {"class": "LeaguePoints"}).text).group(),
                'Rank': re.search(r'\w*\s\d', soup.find("div", {"class": "TierRank"}).text).group(),
                'Win Ratio': re.search(r'\d*%', soup.find("span", {"class": "winratio"}).text).group()
            }
        except:
            pass
        try:
            self.flex = {
                'Wins': soup.find("span", {"class": "sub-tier__gray-text"}).text.split(' ')[1],
                'Losses': soup.find("span", {"class": "sub-tier__gray-text"}).text.split(' ')[2],
                'LP': re.search(r'\d*\s{0,1}LP', soup.find("div", {"class": "sub-tier__league-point"}).text).group(),
                'Rank': re.search(r'\w*\s\d', soup.find("div", {"class": "sub-tier__rank-tier"}).text).group(),
                'Win Ratio': re.search(r'\d*%', soup.find("div", {"class": "sub-tier__gray-text"}).text).group()
            }
        except:
            pass
        return self.solo, self.flex


class Chat(amanobot.helper.ChatHandler):
    def __init__(self, *args, **kwargs):
        super(Chat, self).__init__(*args, **kwargs)

    def on_chat_message(self, msg):
        pprint.pprint(msg)

        if 'entities' in msg:
            if msg['entities'][0]['type'] == 'bot_command':
                tamanho = msg['entities'][0]['length']
                comando = msg['text'][:tamanho]
                argumento = msg['text'][tamanho:]
                if comando == '/check':
                    if len(argumento) == 0:
                        self.sender.sendMessage('Check de quem porra??')
                        return
                    self.sender.sendMessage('Opa, ja pego as info...')
                    solo, flex = opGG(argumento).update()
                    try:
                        msg = f'_Informações de {argumento}_ - *Solo Q*\n'
                        for key, item in solo.items():
                            msg += f'\n        *{key}:* {item}'
                        self.sender.sendMessage(msg, parse_mode='Markdown')
                    except:
                        self.sender.sendMessage("Não encontrei informações da Solo Q de " + argumento)
                    try:
                        msg = f'_Informações de {argumento}_ - *Flex*\n'
                        for key, item in flex.items():
                            msg += f'\n        *{key}:* {item}'
                        self.sender.sendMessage(msg, parse_mode='Markdown')
                        return
                    except:
                        self.sender.sendMessage("Não encontrei informações da Flex de " + argumento)
                        return

    def on_callback_query(self, msg):
        query_id, from_id, query_data = amanobot.glance(msg, flavor='callback_query')
        pass

    def on__idle(self, event):
        # print('Em caso de dúvidas, contate a STI por telefone. O ramal 0000.')
        pass


TOKEN = '1366501748:AAHD61_3d0brQKvpGDCRt3caB7sG5yJJx-M'

bot = amanobot.DelegatorBot(TOKEN, [
    include_callback_query_chat_id(
        pave_event_space())(
        per_chat_id(types='all'), create_open, Chat, timeout=10),
])
MessageLoop(bot).run_as_thread()
print('Listening ...')

while 1:
    time.sleep(10)