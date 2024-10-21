import configparser
import time
from datetime import datetime
import requests
from telethon import TelegramClient, events


# https://api.telegram.org/bot8075899006:AAGSiOBswyDjph6hmYCdvOepawb3HUD17DA/getUpdates
# "id":-1002450320001,"title":"Bank"
# "id":-1002312877293,"title":"Nafas
# "id":-1002360529448,"title":"Fatima
# "id":-1002456271503,"title":"Babak
# "id":-1002415833982,"title":"Shima
# "id":-1002162467176,"title":"Sina
# "id":-1002309641189,"title":"Omid
# "id":-1002419927054,"title":"Farnoush
# "id":-1002429242950,"title":"Tara
# "id":-1002290733189,"title":"Farnaz
# "id":-1002451394374,"title":"Majid

class Player:
    credit = 0

    def __init__(self, id, name, nickname):
        self.id = id
        self.name = name
        self.nickname = nickname

    def send_message(self, message) -> None:
        url = 'https://api.telegram.org/bot8075899006:AAGSiOBswyDjph6hmYCdvOepawb3HUD17DA/sendMessage?chat_id=' + \
              self.id + '&text=' + message
        requests.get(url)


def evaluate_message(message):
    try:
        if (message[0:3].upper() in players) and (message[3:6].upper() in players):
            if players[message[0:3].upper()].credit - int(message[6:]) >= 0:
                players[message[0:3].upper()].credit -= int(message[6:])
                players[message[3:6].upper()].credit += int(message[6:])
                players[message[0:3].upper()].send_message('You paid ' + message[6:] + ' to ' +
                                                           players[message[3:6].upper()].name + '.' + '\n' +
                                                           'You have ' + str(players[message[0:3].upper()].credit) +
                                                           ' credit.')
                players[message[3:6].upper()].send_message('You got ' + message[6:] + ' from ' +
                                                           players[message[0:3].upper()].name + '.' + '\n' +
                                                           'You have ' + str(players[message[3:6].upper()].credit) +
                                                           ' credit.')
            else:
                Bank.send_message(players[message[0:3].upper()].name + ' has not enough credit.')
        elif message[0:5].upper() == 'RESET':
            for player in players.values():
                player.credit = int(message[5:])
                player.send_message('You have ' + str(player.credit) + ' credit.')
        elif message.upper() == "LIST":
            result = ''
            for player in players.values():
                result += player.nickname + ' ' + player.name + ' ' + str(player.credit) + '\n'
            Bank.send_message(result)
        elif ('=' in message) and (message[0:3].upper() in players):
            players[message[0:3].upper()].credit = int(message[4:])
            players[message[0:3].upper()].send_message('You have ' + str(message[4:]) + ' credit.')
        elif ('-' in message) and (message[0:3].upper() in players):
            if players[message[0:3].upper()].credit - int(message[4:]) >= 0:
                players[message[0:3].upper()].credit -= int(message[4:])
                players[message[0:3].upper()].send_message('You paid ' + str(message[4:]) + ' to the bank.' + '\n' +
                                                           'You have ' + str(players[message[0:3].upper()].credit) +
                                                           ' credit.')
            else:
                Bank.send_message(players[message[0:3].upper()].name + ' has not enough credit.')
        elif ('+' in message) and (message[0:3].upper() in players):
            players[message[0:3].upper()].credit += int(message[4:])
            players[message[0:3].upper()].send_message('You got ' + str(message[4:]) + ' from the bank.' + '\n' +
                                                       'You have ' + str(players[message[0:3].upper()].credit) +
                                                       ' credit.')
        elif (message[0:3].upper() == "RE-") and (message[3:6].upper() in players):
            players[message[6:9].upper()] = players.pop(message[3:6].upper())
            players[message[6:9].upper()].nickname = message[6:9].upper()
            players[message[6:9].upper()].name = message[9:]

    except Exception as e:
        print(e)
    # for player in players.values():
    #    print(player.nickname + ' ' + player.name + ' ' + str(player.credit))


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
        print(datetime.now())
        evaluate_message(message)
    except:
        pass


Bank = Player('-1002450320001', 'Bank', '___')
Majid = Player('-1002451394374', 'Majid', 'MAJ')
Farnaz = Player('-1002290733189', 'Farnaz', 'FAR')
Tara = Player('-1002429242950', 'Tara', 'TAR')
Farnoush = Player('-1002419927054', 'Farnoush', 'FAN')
Omid = Player('-1002309641189', 'Omid', 'OMI')
Sina = Player('-1002162467176', 'Sina', 'SIN')
Shima = Player('-1002415833982', 'Shima', 'SHI')
Babak = Player('-1002456271503', 'Babak', 'BAB')
Fatima = Player('-1002360529448', 'Fatima', 'FAT')
Nafas = Player('-1002312877293', 'Nafas', 'NAF')
players = {
    Majid.nickname: Majid,
    Farnaz.nickname: Farnaz,
    Tara.nickname: Tara,
    Farnoush.nickname: Farnoush,
    Omid.nickname: Omid,
    Sina.nickname: Sina,
    Shima.nickname: Shima,
    Babak.nickname: Babak,
    Fatima.nickname: Fatima,
    Nafas.nickname: Nafas
}
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
