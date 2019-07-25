import discord
import apscheduler
import time
import asyncio
import os
from apscheduler.schedulers.asyncio import AsyncIOScheduler

client = discord.Client()
sched = AsyncIOScheduler()
sched.start()
msg_ch = None

@client.event
async def on_ready():
    print('You \'ve logged in as {0.user}'.format(client))
    await client.change_presence(status=discord.Status.idle, activity=discord.Game("나스호른과 SM"))
    print('Operation is started.')
    
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('#operation test'):
        await message.channel.send('정상')
        print(message.channel)
        print(type(message.channel))
        global msg_ch
        msg_ch = message.channel
        sch()
    
    elif message.content.startswith('#help'):
        await message.channel.send('사용법\n작동확인:\#operation test\n태그추가:\#태그받기\n태그삭제:\#태그떼기')

    elif message.content.startswith('#태그받기'):
        role = '원스토어'
        user = message.author
        await user.add_roles(discord.utils.get(user.guild.roles, name=role))
        await message.channel.send('원스토어 태그부여 완료')
        print(message.author)
    
    elif message.content.startswith('#태그떼기'):
        role = '원스토어'
        user = message.author
        await user.remove_roles(discord.utils.get(user.guild.roles, name=role))
        await message.channel.send('원스토어 태그삭제 완료')
        print(message.author)
        
async def job1():
    await msg_ch.send('<@&602701751501717504> 딸랑 딸랑 원스토어 출석해라')
    print('알림 발송')
    now = time.localtime()
    s = "%04d-%02d-%02d %02d:%02d:%02d" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)
    print(s)

async def job2():
    await msg_ch.send('<@&602701751501717504> 딸랑 딸랑 원스토어 출석준비')
    print('발송 대기')
    now = time.localtime()
    s = "%04d-%02d-%02d %02d:%02d:%02d" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)
    print(s)    

def sch():
    sched.add_job(job2, 'cron', hour = "23", minute = "40")
    sched.add_job(job1, 'cron', hour = "23", minute = "50")
    sched.add_job(job2, 'cron', hour = "0", minute = "0")
    sched.add_job(job1, 'cron', hour = "0", minute = "10")

client.run('NjAyNjYwMjA2MjExNDk4MDI0.XTUFLg.kPiaUFmOTfhzMuk3vVeSgS4D6rQ')