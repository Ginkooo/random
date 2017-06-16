import fbchat

CONFIG_FILE = '/home/ginko/.config/pyfbchat/config'
CONFIG = dict()

with open(CONFIG_FILE, 'r') as f:
    for line in f:
        key, value = line.split(':')
        CONFIG[key.lower()] = value

client = fbchat.Client(CONFIG['id'], CONFIG['password'])

friends = client.getUsers("Filip Demski")
dem = friends[0]

while True:
    client.send(dem.uid, input())
