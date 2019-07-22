import discord
import os

TOKEN = 'NTkzMjM1MzA1MDM3OTU1MDky.XRLK9g.Ge8G81f60d265MV2yiyzxA9io_s'

client = discord.Client()

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!사용법'):
        embed = discord.Embed(title="수색요정사용법", description="인형 제조시간 : ,hhmm으로 입력 예시)4시간 4분->,0404\n장비/요정제조시간 : .hhmm으로 입력 예시)0시간 52분->.0052 5시간 5분->.0505", color = 0x00ff00)
        msg = '{0.author.mention}'.format(message)
        await client.send_message(message.channel, embed=embed)
    elif message.content.startswith(','):
        infile = open("doll.txt", "r")
        t = infile.read()
        time = str(message.content[1:])
        loc = int(t.find(time))
        if loc == -1 :
            sen = " 처음보는 시간인데요?"
            msg = ('{0.author.mention}' + sen).format(message)
            await client.send_message(message.channel, msg)
        else :
            sen = t[loc+4:t.find("\n",loc)]
            msg = ('{0.author.mention}' + sen).format(message)
            await client.send_message(message.channel, msg)
    elif message.content.startswith('.'):
        infile = open("equip.txt", "r")
        t = infile.read()
        time = str(message.content[1:])
        loc = int(t.find(time))
        if loc == -1 :
            sen = " 처음보는 시간인데요?"
            msg = ('{0.author.mention}' + sen).format(message)
            await client.send_message(message.channel, msg)
        else :
            sen = t[loc+4:t.find("\n",loc)]
            msg = ('{0.author.mention}' + sen).format(message)
            await client.send_message(message.channel, msg)

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    await client.change_presence(game=discord.Game(name="라플비 찾는중...", type = 1))

client.run(TOKEN)