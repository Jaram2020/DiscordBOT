import discord
import os

client = discord.Client()

@client.event
async def on_ready():
    print('You\'ve logged in as {0.user}'.format(client))
    await client.change_presence(status=discord.Status.idle, activity=discord.Game("나스호른과 SM"))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!사용법'):
        embed=discord.Embed(title="수색요정 사용법", description="인형 제조시간 : ,hhmm으로 입력 예시)4시간 4분->,0404\n장비/요정제조시간 : .hhmm으로 입력 예시)0시간 52분->.0052 5시간 5분->.0505", color=0x00ff00)
        await message.channel.send(embed=embed) 
    elif message.content.startswith(','):
        infile = open("doll.txt", "r")
        t = infile.read()
        time = str(message.content[1:])
        loc = int(t.find(time))
        if loc == -1 :
            sen = " 처음보는 시간인데요?"
            await message.channel.send(sen)
        else :
            sen = t[loc+4:t.find("\n",loc)]
            await message.channel.send(sen)
    elif message.content.startswith('.'):
        infile = open("equip.txt", "r")
        t = infile.read()
        time = str(message.content[1:])
        loc = int(t.find(time))
        if loc == -1 :
            sen = " 처음보는 시간인데요?"
            await message.channel.send(sen)
        else :
            sen = t[loc+4:t.find("\n",loc)]
            await message.channel.send(sen)
            
client.run('NTkzMjM1MzA1MDM3OTU1MDky.XTV9SA.sWOSxNcWjumYS-LVX6bJOxlaXj0')