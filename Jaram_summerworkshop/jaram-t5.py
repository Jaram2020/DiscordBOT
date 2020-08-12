import discord
import asyncio
import os
import sys
import urllib.request
import json
import random
import apscheduler
import datetime
import time
from apscheduler.schedulers.asyncio import AsyncIOScheduler


#Papago API id/pw
n_id = "JLPMmTXOBkFMJ7rhAm1u"
n_secret = "WUECYHv2Wg"

sched = AsyncIOScheduler()
sched.start()
client = discord.Client()

class Vote:
    before_start = 0
    voting = 1
    end = 2

    def __init__(self, title, by):
        self.counts = []
        self.title = title
        self.choices = []
        self.by = by
        self.status = 0

    def start(self):
        for _ in self.choices:
            self.counts.append([])


votes = []

#디스코드 우상단 봇 status 설정
@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.idle, activity=discord.Game("Team5 | $help"))
    print('Operating...')

#메세지 봇(prefix:#)
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('#help'):
        await message.channel.send(embed = embed)

    elif message.content.startswith('#번역'): #번역 [도착 언어] [목표 문장(출발 언어는 자동 감지)]
        from_lan = message.content[4:6]
        target_text = message.content[7:]
        await message.channel.send("```" + pst_detection(from_lan, target_text) + "```")
    
    elif message.content.startswith('#teamsplit'):
        await team_Split(message) 

    elif message.content.startswith('#add sched'): #add sched YYYY MM DD HH mm contents
        contents = message.content.split(" ")
        add_sch(contents[2:], message)
        await message.channel.send(embed = discord.Embed(title = contents[-1],description = (contents[-1]+" 일정이 추가되었습니다."),color=0x00ff56))

    elif message.content.startswith('#rmv sched'): #rmv sched contents
        contents = message.content.split(" ")
        rst = rmv_sch(contents[-1], message)
        if rst == 0:
            await message.channel.send(embed = discord.Embed(title = contents[-1],description = (contents[-1]+" 일정이 삭제되었습니다."),color=0x00ff56))
        else:
            await message.channel.send(embed = discord.Embed(title = contents[-1],description = (contents[-1]+"은(는) 없는 일정입니다."),color=0x00ff56))
        

    elif message.content.startswith('#vote'):
        await vote_func(message) 
    
    elif message.content.startswith('#게임을 시작하자'):
        await game(message)
    elif message.content.startswith('#ping'):
        latency = client.latency
        await message.channel.send('#pong! ' + str(round(latency,4)*1000) + 'ms')


# 1.번역 //Translator 전상민
def pst_detection(to_lan, target_text):
    encQuery = urllib.parse.quote(target_text)
    data = "query=" + encQuery
    url = "https://openapi.naver.com/v1/papago/detectLangs"
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id",n_id)
    request.add_header("X-Naver-Client-Secret",n_secret)
    response = urllib.request.urlopen(request, data=data.encode("utf-8"))
    rescode = response.getcode()
    if(rescode == 200):
        from_lan = response.read().decode('utf-8')[13:15]
        return pst_translation(from_lan, to_lan, target_text)
    else:
        print("Error Code(Language_Detection):" + rescode)

def pst_translation(from_lan, to_lan, target_text):
    encText = urllib.parse.quote(target_text)
    data = "source=" + from_lan + "&target=" + to_lan + "&text=" + encText
    url = "https://openapi.naver.com/v1/papago/n2mt"
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id",n_id)
    request.add_header("X-Naver-Client-Secret",n_secret)
    response = urllib.request.urlopen(request, data=data.encode("utf-8"))
    rescode = response.getcode()
    if(rescode==200):
        response_body = response.read().decode('utf-8')
        jDict = json.loads(response_body)
        result = jDict['message']['result']['translatedText']
        print(result)
        return result
    else:
        print("Error Code:" + rescode)

embed = discord.Embed(title = "How to use?", color = 0x00ff56)
embed.set_author(name = "Jaram_Team5")
embed.add_field(name = "#help" , value = "사용법 안내", inline = False)
embed.add_field(name = "#번역 [도착언어] [목표 문장(출발 언어는 자동 감지)]" , value = "ko - 한국어\nen - 영어\nja - 일본어\nzh-CN - 중국어 간체\nzh-TW - 중국어 번체\nvi - 베트남어\nde - 독일어\nth - 태국어\nru - 러시아어\nfr - 프랑스어\nit - 이탈리아어", inline = False)
embed.add_field(name = "#teamsplit" , value = "이모티콘을 이용해 팀을 나눌 수 있습니다.", inline = False)
embed.add_field(name = "#add sched YYYY MM DD HH mm " , value = "특정 날짜와 시간에 스케줄을 추가합니다.", inline = False)
embed.add_field(name = "#rmv sched schedule" , value = "추가한 스케줄을 제거합니다.", inline = False)
embed.add_field(name = "#게임을 시작하자", value = "봇과 가위바위보 게임을 시작합니다.", inline = False)
embed.add_field(name = "#ping", value = "Discord 서버와의 반응속도를 확인합니다.", inline = False)
embed.add_field(name = "#vote", value = "투표를 진행합니다. #vote help를 쳐서 더 자세한 기능을 확인하세요.", inline = False)
embed.set_footer(text = "Jaram summer workshop Team 5 / Powered by discord.py OSP")

# 2.팀스플릿  //team_Split 임종협
async def team_Split(message) :
    #이모티콘 리스트
    #1은 1번 팀, 2는 2번 팀, OK는 팀 결정 후 종료.
    emojiList = ['1️⃣','2️⃣','🆗']
    list1 = []
    list2 = []

    #메시지에 이모티콘 추가
    for i in emojiList :
        await message.add_reaction(i)   
        
    #중간 출력
    await message.channel.send('이모티콘을 눌러 팀을 나눠주세요.\n2개밖에 안 되니까 더 안 되냐고 묻지 마세요.\n팀 결정이 모두 끝나면, ok 버튼을 눌러주세요.\n60초 후 자동으로 종료됩니다.')
    #실제 통신 시간 간의 문제가 있어서, 잠깐 시간을 주는 겁니다.
    #이 부분은 리팩토링 필요!
    await asyncio.sleep(60)



    #만약 OK 버튼을 누르면 밑에 있는 printer 출력하고 종료
    list1 = message.reactions[0].users()
    list2 = message.reactions[1].users()
    if(message.reactions[2].count < 2) : 
        return
    else :
        await list_Printer(list1, list2, message)
        return

#출력 메소드
async def list_Printer(list1, list2, message) :
    #출력
    await message.channel.send('OK. 팀 스플릿을 종료합니다.\n밑의 결과를 확인해주세요.\n')
    #빈 스트링
    string = ''
    
    #팀 1 string
    string += await list_Adder(list1, 1)
    #구분선
    string += '-------------\n'
    #팀 2 string
    string += await list_Adder(list2, 2)
    #최종 보내기
    await message.channel.send(string)

#string을 완성시켜주는 메소드
async def list_Adder(list0, teamNum) :
    #코드를 줄이기 위해서...
    i = -1
    #빈 스트링
    string = ''
    string += str(teamNum) + '번 팀 :\n'
    #~번 팀 : 
    #   n. 이름 
    async for element in list0 :
        i += 1
        if i == 0 : continue
        string += '    ' + str(i) + '. ' + element.name + '\n'
    return string

# 3.스케줄 알림 //announce_Schedule 이강재
def add_sch(con, message):
    sched.add_job(job_add, 'cron', year = con[0], month = con[1], day = con[2], hour = con[3], minute = con[4], args = [con, message], id = con[5])
    return 

async def job_add(time, message):
    notice_setTime = time[0] + "년 " + time[1] + "월 " + time[2] + "일 "  + time[3] + "시 " + time[4] + "분에 " + time[5] + "이(가) 시작합니다."
    await message.channel.send(embed=discord.Embed(title="스케줄 설정",timestamp = datetime.datetime.utcnow(),description = notice_setTime))
    return 

def rmv_sch(sch_id, message):
    try:
        sched.remove_job(sch_id)
        return 0
    except apscheduler.jobstores.base.JobLookupError:
        return 

# 4.투표 기능 //vote 장효석
async def vote_func(message):
    args = message.content.split(' ')
    # vote [make|edit|remove|start|end|list|info]

    if args[1] == 'make':  # #vote make [제목] "투표 생성"
        title = str(message.content).replace('#vote make ', '')
        votes.append(Vote(title=title, by=message.author.name + '#' + message.author.discriminator, ))
        await message.channel.send("투표가 추가되었습니다")
    elif args[1] == 'list':  # #vote list "투표 리스트"
        idx = 1
        if len(votes) == 0:
            embed = discord.Embed()
            embed.add_field(name="오류", value="등록된 투표가 존재하지 않습니다.")
            await message.channel.send(embed=embed)
        else:
            embed = discord.Embed()
            for vote in votes:
                text = str(idx) + ". " + vote.title + " / " + vote.by + " / "
                if vote.status == 0:
                    text += "투표 시작 전"
                elif vote.status == 1:
                    text += "투표 중"
                elif vote.status == 2:
                    text += "투표 종료"
                embed.add_field(name="제목", value=text, inline=False)
            await message.channel.send(embed=embed)
    elif args[1] == 'remove':  # #vote remove [index] "투표 삭제"
        vote = votes[int(args[2]) - 1]
        if vote.by != message.author.name + '#' + message.author.discriminator:
            await message.channel.send("투표를 생성한 유저가 아닙니다")
        else:
            await message.channel.send(args[2] + "번째 투표가 제거되었습니다")
            votes.remove(vote)
    elif args[1] == 'clean':  # #vote clean "종료된 투표 전체 삭제"
        cnt = 0
        for vote in votes:
            if vote.status == Vote.end:
                votes.remove(vote)
        await message.channel.send("종료된 투표 " + str(cnt) + "개가 삭제되었습니다")
    elif args[1] == 'start':  # #vote start [index] "투표 시작"
        vote = votes[int(args[2]) - 1]
        if vote.by != message.author.name + '#' + message.author.discriminator:
            await message.channel.send("투표를 생성한 유저가 아닙니다")
        else:
            await message.channel.send(args[2] + "번째 투표가 시작되었습니다")
            vote.status = Vote.voting
            vote.start()
    elif args[1] == 'end':  # #vote start [index] "투표 종료"
        vote = votes[int(args[2]) - 1]
        if vote.by != message.author.name + '#' + message.author.discriminator:
            await message.channel.send("투표를 생성한 유저가 아닙니다")
        else:
            await message.channel.send(args[2] + "번째 투표가 종료되었습니다")
            vote.status = Vote.end
    elif args[1] == 'edit':
        vote = votes[int(args[2]) - 1]
        if vote.by != message.author.name + '#' + message.author.discriminator:
            await message.channel.send("투표를 생성한 유저가 아닙니다")
        elif vote.status != 0:
            await message.channel.send("투표 시작 전에만 항목을 변경할 수 있습니다")
        else:
            if args[3] == 'add':  # #vote edit [index] add [항목] "투표 항목 추가"
                choice = str(message.content).replace('#vote edit ' + args[2] + ' add ', '')
                vote.choices.append(choice)
                await message.channel.send("항목이 추가되었습니다")
            if args[3] == 'edit':  # #vote edit [index] edit [index] [항목] "투표 항목 변경"
                new_choice = str(message.content).replace('#vote edit ' + args[2] + ' edit ' + args[4] + ' ', '')
                vote.choices[int(args[4]) - 1] = new_choice
                await message.channel.send("항목이 변경되었습니다")
            if args[3] == 'remove':  # #vote edit [index] remove [index] "투표 항목 제거"
                choice = vote.choice[int(args[3]) - 1]
                vote.choices.remove(choice)
                await message.channel.send("항목이 제거되었습니다")
    elif args[1] == 'info':  # #vote info [index] "투표 상세 정보"
        vote = votes[int(args[2]) - 1]
        embed = discord.Embed()
        embed.add_field(name="제목", value=vote.title, inline=False)
        embed.add_field(name="만든 사람", value=vote.by, inline=False)
        s = ""
        if vote.status == 0:
            s += "투표 시작 전"
        elif vote.status == 1:
            s += "투표 중"
        elif vote.status == 2:
            s += "투표 종료"
        embed.add_field(name="상태", value=s, inline=False)
        idx = 1
        for choice in vote.choices:
            val = choice
            if vote.status != 0:
                val += " / " + str(len(vote.counts[idx - 1])) + "표"
            embed.add_field(name="항목" + str(idx), value=val, inline=False)
            idx += 1
        await message.channel.send(embed=embed)
    elif args[1] == 'help':
        embed = discord.Embed(title="#vote help")
        embed.add_field(name='#vote make [투표 제목]', value='투표 제목의 투표를 생성합니다', inline=False)
        embed.add_field(name='#vote list', value='투표 리스트를 보여줍니다', inline=False)
        embed.add_field(name='#vote remove [투표 번호]', value='지정한 투표를 삭제합니다', inline=False)
        embed.add_field(name='#vote clean', value='종료된 모든 투표를 삭제합니다', inline=False)
        embed.add_field(name='#vote start [투표 번호]', value='지정한 투표를 시작합니다', inline=False)
        embed.add_field(name='#vote end [투표 번호]', value='지정한 투표를 종료합니다', inline=False)
        embed.add_field(name='#vote edit [투표 번호] add [항목]', value='지정한 투표에 새 항목을 추가합니다', inline=False)
        embed.add_field(name='#vote edit [투표 번호] edit [항목 번호] [항목]', value='지정한 투표의 지정한 항목의 내용을 수정합니다', inline=False)
        embed.add_field(name='#vote edit [투표 번호] remove [항목 번호]', value='지정한 투표의 지정한 항목을 삭제합니다', inline=False)
        embed.add_field(name='#vote info [투표 번호]', value='지정한 투표의 상세 정보를 보여줍니다', inline=False)
        embed.add_field(name='#vote [투표 번호] [항목 번호]', value='지정한 투표의 지정한 항목에 투표합니다', inline=False)

        await message.channel.send(embed=embed)
    else:
        vote = votes[int(args[1]) - 1]
        if vote.status != 1:
            await message.channel.send("투표가 진행중이 아닙니다")
        else:
            for count in vote.counts:
                if message.author.name + '#' + message.author.discriminator in count:
                    count.remove(message.author.name + '#' + message.author.discriminator)

            vote.counts[int(args[2]) - 1].append(message.author.name + '#' + message.author.discriminator)

            await message.channel.send(vote.title + " 투표의 " + vote.choices[int(args[2]) - 1] + " 항목에 투표되었습니다")

# 5.가위바위보 게임 //game 황다빈
async def game(message):
    rsp = ["가위","바위","보"]
    embed = discord.Embed(title="가위바위보",description="5초내로 (가위/바위/보)를 써주세요!", color=0x00aaaa)
    channel = message.channel
    msg1 = await message.channel.send(embed=embed)
    def check(m):
        return m.author == message.author and m.channel == channel
    try:
        msg2 = await client.wait_for('message', timeout=5.0, check=check)
    except asyncio.TimeoutError:
        await msg1.delete()
        embed = discord.Embed(title="가위바위보",description="왜 안내세요? 갈래요!", color=0x00aaaa)
        await message.channel.send(embed=embed)
        return
    else:
        await msg1.delete()
        bot_rsp = str(random.choice(rsp))
        user_rsp  = str(msg2.content)
        answer = ""
        if bot_rsp == user_rsp:
            answer = "저는 " + bot_rsp + "를 냈고, 당신은 " + user_rsp + "를 냈어요!\n" + "비겼습니다!"
        elif (bot_rsp == "가위" and user_rsp == "바위") or (bot_rsp == "보" and user_rsp == "가위") or (bot_rsp == "바위" and user_rsp == "보"):
            answer = "저는 " + bot_rsp + "를 냈고, 당신은 " + user_rsp + "를 내셨내요.\n" + "당신의 승리입니다!"
        elif (bot_rsp == "바위" and user_rsp == "가위") or (bot_rsp == "가위" and user_rsp == "보") or (bot_rsp == "보" and user_rsp == "바위"):
            answer = "저는 " + bot_rsp + "를 냈고, 당신은 " + user_rsp + "를 내셨내요.\n" + "흣흠 제가 이겼어요!"
        else:
            answer == "정확하게 다시 입력해주세요!"
            await message.channel.send(embed=embed)
            return
        embed = discord.Embed(title="가위바위보",description=answer, color=0x00aaaa)
        await message.channel.send(embed=embed)
        return


# #디스코드 봇 token
client.run('NzQyNTcyNDMzMjk4Njg2MDAz.XzIEeA.7hh6zcrhppHh1p4N8qX801vNEbY')
n_id = "JLPMmTXOBkFMJ7rhAm1u"
n_secret = "WUECYHv2Wg"