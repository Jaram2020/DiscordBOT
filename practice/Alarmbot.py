import discord
import datetime
import time

client = discord.Client()

@client.event
async def on_ready():
    print('You \'ve logged in as {0.user}'.format(client))
    await client.change_presence(status=discord.Status.idle, activity=discord.Game("나스호른과 SM"))
    
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('#operation test'):
        await message.channel.send('정상')
        print(message)

    if message.content.startswith('#operation start'):
        print('Operation is started.')
        await message.channel.send('심심할때마다 시작시키면 완장이 아봉먹임.')
        lct = datetime.datetime.now()
        while True: #<@&602701751501717504> 원스토어 태그 #
            if (lct.hour == 23 and lct.minute == 50) or (lct.hour == 0 and lct.minute == 10):
                await message.channel.send('<@&602701751501717504> 원스토어 출석해라')
                print('알림 발송')
            if (lct.hour == 23 and lct.minute == 45) or (lct.hour == 0 and lct.minute == 5):
                await message.channel.send('<@&602701751501717504> 원스토어 출석준비')
                print('발송 대기')
                time.sleep(300)
            if (lct.hour == 23 and lct.minute == 40) or (lct.hour == 0 and lct.minute == 0):
                await message.chaneel.send('<@&602701751501717504> 원스토어 출석준비')
                print('발송 대기')
                time.sleep(300)
            if lct.hour == 23 and lct.minute > 39:
                time.sleep(30)
            elif lct.hour == 23:
                time.sleep(600)
            elif lct.hour == 0 and lct.minute <11:
                time.sleep(30)
            else :
                time.sleep(3600)
            lct = datetime.datetime.now()

client.run('NjAyNjYwMjA2MjExNDk4MDI0.XTUFLg.kPiaUFmOTfhzMuk3vVeSgS4D6rQ')