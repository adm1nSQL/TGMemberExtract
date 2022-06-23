from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
import csv

apiid = 123456
apihash = 'YOURAPIHASH'
phone = '+111111111111'
client = TelegramClient(phone, apiid, apihash)

client.connect()
if not client.isuserauthorized():
    client.sendcoderequest(phone)
    client.signin(phone, input('Enter the code: '))


chats = []
lastdate = None
chunksize = 200
groups=[]
 
result = client(GetDialogsRequest(
             offsetdate=lastdate,
             offsetid=0,
             offsetpeer=InputPeerEmpty(),
             limit=chunksize,
             hash = 0
         ))
chats.extend(result.chats)

for chat in chats:
    try:
        if chat.megagroup== True:
            groups.append(chat)
    except:
        continue

print('Choose a group to extract members from:')
i=0
for g in groups:
    print(str(i) + '- ' + g.title)
    i+=1

gindex = input("Enter a Number: ")
targetgroup=groupsint(g_index)

print('Fetching Members...')
allparticipants = []
allparticipants = client.getparticipants(targetgroup, aggressive=True)

print('Saving In file...')
with open("members.csv","w",encoding='UTF-8') as f:
    writer = csv.writer(f,delimiter=",",lineterminator="\n")
    writer.writerow('username','user id', 'access hash','name','group', 'group id')
    for user in allparticipants:
        if user.username:
            username= user.username
        else:
            username= ""
        if user.firstname:
            firstname= user.firstname
        else:
            firstname= ""
        if user.lastname:
            lastname= user.lastname
        else:
            lastname= ""
        name= (firstname + ' ' + lastname).strip()
        writer.writerow([username,user.id,user.accesshash,name,targetgroup.title, targetgroup.id])      
print('Members extract successfully.')
