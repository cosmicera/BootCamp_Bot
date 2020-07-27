import requests, asyncio, discord, os
from bs4 import BeautifulSoup
from discord.ext import commands

Name = "qxt"
hdr = {'Accept-Language': 'ko_KR,en;q=0.8', 'User-Agent': (
    'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Mobile Safari/537.36')}

class PUBGPlayer:
    def __init__(self):
     self.nickname = ""
     self.kda = ""
     self.tier = ""
     self.rp = ""
     self.avg = ""

    def parseOPGG(name):
     Container = {}
     Container
       
     self.nickname = name
     #https://dak.gg/profile/Archi-hong
     #https://pubg.op.gg/user/Archi-hong
     url = 'https://dak.gg/profile/' + self.nickname
     req = requests.get(url, headers=hdr)
     html = req.text
     soup = BeautifulSoup(html, 'html.parser')

     for i in soup.select('div.userData > span.nick'):
         UserNickname = i.text
     Container['UserNickname'] = UserNickname.strip()
     
     for i in soup.select('#profile .profileContent>.modeSummary .modeItem.ranked .mode-section.tpp .stats .stats-item.kd .value'):
         KDA = i.text
     self.kda = KDA.strip()
     
     for i in soup.select('#profile .profileContent>.modeSummary .modeItem.ranked .mode-section.tpp .stats .stats-item.deals .value'):
         AVG = i.text
     self.avg = AVG.strip()
     
     for i in soup.select('#profile .profileContent>.modeSummary .modeItem.ranked .mode-section.tpp .rating .value'):
         Tier = i.text
     self.tier = Tier.strip()
     
     for i in soup.select('#profile .profileContent>.modeSummary .modeItem.ranked .mode-section.tpp .rating .caption'):
         RP = i.text
     self.rp = RP.strip()

def printSummonerInfo(Container):
    #rankCase = ['솔로', '자유']
        if Container['UserNickname'] != '':
            print("==================================")
            if len(Container['Tier']):
                print(Container['UserNickname'] + "님의 랭크 정보입니다.")
                print("==================================")
                print("K/D/A: " + Container['KDA'])
                print("Deals average: " + Container['AVG'])
                print("Tier: " + Container['Tier'] + " (" + Container['RP'] + ")")
            else:
                print(Container['UserNickname'] + "님은 Unranked입니다.")
                print("==================================")

"""
if __name__ == "__main__":
    printSummonerInfo(parseOPGG("kakaotaemin"))
    printSummonerInfo(parseOPGG("inhoss"))
    printSummonerInfo(parseOPGG("kakaobugang"))
    printSummonerInfo(parseOPGG("Archi-hong"))
    printSummonerInfo(parseOPGG("yorksin"))
    printSummonerInfo(parseOPGG("Campcos"))
    printSummonerInfo(parseOPGG("EunJi_12"))
"""

#bot setting
token_path = os.path.dirname( os.path.abspath(__file__) ) + "\\token.txt"
t = open(token_path, "r", encoding="utf_8")
token = t.read().split()[0]
game = discord.Game("!도움")
bot = commands.Bot(command_prefix='!')

#bot run
@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online, activity=discord.Game('Test bot'))
    print("봇 시작")

@bot.event
async def on_message(message):
    await bot.process_commands(message)

@bot.command()
async def 도움(ctx):
    await ctx.send("무엇을 도와드릴까요?")

@bot.command(pass_context=True)
async def 전적(ctx):
    player = PUBGPlayer()
    player.parseOPGG("kakaotaemin")
    embed=discord.Embed(title= player.nickname + "님의 랭크 정보입니다.")
    await ctx.send(embed=embed)


bot.run(token)
