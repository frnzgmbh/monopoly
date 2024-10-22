import configparser
import os
import time
import json
import requests
from telethon import TelegramClient, events
from os import walk
from typing import List


# https://api.telegram.org/bot8075899006:AAGSiOBswyDjph6hmYCdvOepawb3HUD17DA/getUpdates?offset=-1
# data = [
# '-1002450320001,Bank,___,0',
# '-1002312877293,Nafas,NAF,0',
# '-1002360529448,Fatima,FAT,0',
# '-1002456271503,Babak,BAB,0',
# '-1002415833982,Shima,SHI,0',
# '-1002162467176,Sina,SIN,0',
# '-1002309641189,Omid,OMI,0',
# '-1002419927054,Farnoush,FAN,0',
# '-1002429242950,Tara,TAR,0',
# '-1002290733189,Farnaz,FAR,0',
# '-1002451394374,Majid,MAJ,0',
# '-1002447487658,Ali",ALI,0',
# '-1002463222025,Maryam",MAR,0']


class Player:
    def __init__(self, line: str):
        self.id = str(line.split(',')[0])
        self.name = str(line.split(',')[1])
        self.nickname = str(line.split(',')[2])
        self.credit = str(line.split(',')[3])

    def send_message(self, message) -> None:
        url = 'https://api.telegram.org/bot8075899006:AAGSiOBswyDjph6hmYCdvOepawb3HUD17DA/sendMessage?chat_id=' + \
              self.id + '&text=' + message
        requests.get(url)


def get_player_list() -> List[Player]:
    player_file_list = []
    for (_, _, file_names) in walk(os.getcwd()):
        for file_name in file_names:
            if '.' not in file_name and file_name[0] == '-':
                player_file_list.append(file_name)
    result = []
    for player_file_name in player_file_list:
        f = open(player_file_name, 'r+')
        line = f.readline()
        result.append(Player(line))
        f.close()
    return result


def get_player(nickname) -> Player:
    result = None
    for player in get_player_list():
        if player.nickname == nickname:
            result = player
            break
    return result


def replace_player(old_nickname, new_nickname, new_name):
    result_player = get_player(old_nickname)
    if result_player is not None:
        result_player.nickname = new_nickname
        result_player.name = new_name
        open(result_player.id, 'w').close()
        f = open(result_player.id, 'r+')
        f.write(str(result_player.id) + ',' +
                str(result_player.name) + ',' +
                str(result_player.nickname) + ',' +
                str(result_player.credit))
        f.close()


def update_credit(nickname: str, new_credit: str):
    result_player = get_player(nickname)
    if result_player is not None:
        result_player.credit = str(new_credit)
        open(result_player.id, 'w').close()
        f = open(result_player.id, 'r+')
        f.write(str(result_player.id) + ',' +
                str(result_player.name) + ',' +
                str(result_player.nickname) + ',' +
                str(result_player.credit))
        f.close()


def evaluate_message(message):
    try:
        if (message[0:3].upper() == "RE-") and (get_player(message[3:6].upper()) is not None):
            replace_player(message[3:6].upper(), message[6:9].upper(), message[9:])
        elif (get_player(message[0:3].upper()) is not None) and \
                (get_player(message[3:6].upper()) is not None):
            debitor = get_player(message[0:3].upper())
            creditor = get_player(message[3:6].upper())
            if int(debitor.credit) - int(message[6:]) >= 0:
                debitor.credit = str(int(debitor.credit) - int(message[6:]))
                creditor.credit = str(int(creditor.credit) + int(message[6:]))
                update_credit(debitor.nickname, debitor.credit)
                update_credit(creditor.nickname, creditor.credit)
                debitor.send_message('You paid ' + message[6:] + ' to ' + creditor.name + '.\n' +
                                     'You have ' + debitor.credit + ' credit.')
                creditor.send_message('You got ' + message[6:] + ' from ' + debitor.name + '.\n' +
                                      'You have ' + creditor.credit + ' credit.')
            else:
                bank.send_message(debitor.name + ' has not enough credit.')
        elif message.upper() == "LIST":
            result = ''
            for player in get_player_list():
                result += player.nickname + ' ' + player.name + ' ' + str(player.credit) + '\n'
            bank.send_message(result)
        elif (message[0:5].upper() == 'RESET'):
            for player in get_player_list():
                update_credit(player.nickname, str(int(message[5:])))
                player.send_message('You have ' + message[5:] + ' credit.')
        elif ('=' in message) and (get_player(message[0:3].upper()) is not None):
            player = get_player(message[0:3].upper())
            update_credit(player.nickname, str(int(message[4:])))
            player.send_message('You have ' + str(message[4:]) + ' credit.')
        elif ('-' in message) and (get_player(message[0:3].upper()) is not None):
            player = get_player(message[0:3].upper())
            if int(player.credit) - int(message[4:]) >= 0:
                update_credit(player.nickname, str(int(player.credit) - int(message[4:])))
                player.send_message('You paid ' + str(message[4:]) + ' to the bank.' + '\n' +
                                    'You have ' + str(int(player.credit) - int(message[4:])) + ' credit.')
            else:
                bank.send_message(player.name + ' has not enough credit.')
        elif ('+' in message) and (get_player(message[0:3].upper()) is not None):
            player = get_player(message[0:3].upper())
            update_credit(player.nickname, str(int(player.credit) + int(message[4:])))
            player.send_message('You got ' + str(message[4:]) + ' from the bank.' + '\n' +
                                'You have ' + str(int(player.credit) + int(message[4:])) + ' credit.')
    except:
        pass


config = configparser.ConfigParser()
config.read("config.ini")
api_id = config['Telegram']['api_id']
api_hash = config['Telegram']['api_hash']
api_hash = str(api_hash)
phone = config['Telegram']['phone']
username = config['Telegram']['username']
client = TelegramClient(username, api_id, api_hash)


@client.on(events.NewMessage(chats='https://t.me/+SoCRvXlrBqE4NjZk'))
async def my_event_handler(event):
    try:
        message = str(event.raw_text)
        evaluate_message(message)
    except:
        pass


bank = Player('-1002450320001,Bank,___,0')

while True:
    try:
        client.start()
        client.run_until_disconnected()
    except:
        try:
            client.disconnect()
        except:
            pass
        time.sleep(5)
    time.sleep(5)
