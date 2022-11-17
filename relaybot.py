from tkinter import N
from turtle import update
import discord
from discord.ext import commands
from obswebsocket import obsws, requests 
from datetime import datetime
from random import randint, choice, seed
from time import sleep
from pandas import Timestamp, Timedelta
from shutil import copy
import os
import livesplit

admins = [
    "WitherMan#0111",
    "Christian Royle#6808",
    "Ludavis#4854",
    "Exeloar#7295"
]
LIVESPLIT_ENABLED = False
OBS_ENABLED = True
BOT_CHANNEL_ID = 0


if LIVESPLIT_ENABLED:
    timer = livesplit.Livesplit(ip="localhost")

if OBS_ENABLED:
    host = "localhost"
    port = 4444
    password = ""

    ws = obsws(host, port)
    ws.connect()

seed((Timestamp.now()-Timestamp(1970,1,1)).total_seconds())
isStarted = False
startTime = 0
currentScene = ""
currentPlayer = [
    0,
    0,
    0
]
teamEmblemCounts = [
    0,
    0,
    0
]
teamTimes = [
    0,
    0,
    0
]
teams = [
    ["Kosmic#5678","DatsunHLS30#6039","fleedle_deedle#2330","Exeloar#7295"],
    ["Monkey#1665","SnapKick#9895","Brobey#5801","Clam#2923",],
    ["tylltoons#4360","RealMim#8947","Kyrrone#1039","Samura1man#6028"]
]
teamReady = [
    False,
    False,
    False
]
teamFinished = [
    False,
    False,
    False
]
relayFinished = True # Used to check for synchronization 
currentAudioPlayer = teams[0][0]

with open('resources/token.txt', 'r') as file:
    TOKEN = file.read()
with open('resources/BotChannelID.txt', 'r') as file:
    BOT_CHANNEL_ID = int(file.read())

copy("resources/ActiveAudioIcon.png",f"resources/team1-activeaudioicon.png")

def isAdmin(ctx):
    return str(ctx.author) in admins

async def handle_command(ctx):
    global currentPlayer
    global startTime
    global isStarted
    global teamReady
    global teamEmblemCounts

    if ctx.content == "!help":
        await ctx.channel.send("Commands:\n\
            !ready to ready up your team\n\
            !next to switch to the next runner. This will auto switch the streamer POV & increment emblem count for your team\n\
            !prev to revert an earned emblem")
            
        return

    if ctx.content.split(" ")[0] == "!forcenext":
        if isAdmin(ctx):
            await nextCommand(int(ctx.content.split(" ")[1]) - 1, currentPlayer[int(ctx.content.split(" ")[1]) - 1],ctx)
            return

    if ctx.content.split(" ")[0] == "!forceready":
        if isAdmin(ctx):
            teamNum = int(ctx.content.split(" ")[1])
            readyCommand(teamNum - 1)
            await ctx.channel.send(f"Team #{teamNum} is now ready")
            return

    if ctx.content.split(" ")[0] == "!forceunready":
        if isAdmin(ctx):
            teamNum = int(ctx.content.split(" ")[1])
            unreadyCommand(teamNum - 1)
            await ctx.channel.send(f"Team #{teamNum} is no longer ready")
            return

    if ctx.content.split(" ")[0] == "!forceemblems":
        if isAdmin(ctx):
            emblemVals = ctx.content.split(" ")[1].split(",")
            for i in range(len(teams)):
                teamEmblemCounts[i] = int(emblemVals[i])
            refreshEmblemCounts()
            return
            
    if ctx.content.split(" ")[0] == "!forceplayers":
        if isAdmin(ctx):
            playerVals = ctx.content.split(" ")[1].split(",")
            for i in range(len(teams)):
                currentPlayer[i] = int(playerVals[i])
            switchToScene()
            return

    if ctx.content == "!forcereset":
        if isAdmin(ctx):
            resetState()
    
    if ctx.content == "!forcestart":
        if isAdmin(ctx):
            teamReady[0] = True
            teamReady[1] = True
            teamReady[2] = True
            await ctx.channel.send("GO!")
            startTime = datetime.now()
            if LIVESPLIT_ENABLED:
                timer.startTimer()
            isStarted = True

    if ctx.content == "!start":
        ready = True
        for i in range(len(teamReady)):
            if not teamReady[i]:
                await ctx.channel.send(f"Team #{i+1} is not ready")
                ready = False
        if not ready:
            return
        
        if isAdmin(ctx):
            await ctx.channel.send("Race begins in 10 seconds")
            for i in range(10):
                await ctx.channel.send(10-i)
                sleep(1)
            await ctx.channel.send("GO!")
            startTime = datetime.now()
            if LIVESPLIT_ENABLED:
                timer.startTimer()
            isStarted = True
        return
    
    if ctx.content == "!cancel":
        if isAdmin(ctx):
            await ctx.channel.send("Race Cancelled. Teams must ready up again")
            if LIVESPLIT_ENABLED:
                timer.reset()
            resetState()
        return

    if ctx.content == "!ready":
        if not startTime == 0:
            return
        for team in range(len(teams)):
            for player in range(len(teams[team])):
                if teams[team][player] == str(ctx.author):
                    readyCommand(team)
                    await ctx.channel.send(f"Team #{team+1} is now ready")
                    return

    if ctx.content == "!unready":
        if not startTime == 0:
            return
        for team in range(len(teams)):
            for player in range(len(teams[team])):
                if teams[team][player] == str(ctx.author):
                    unreadyCommand(team)
                    await ctx.channel.send(f"Team #{team+1} is no longer ready")
                    return

    if ctx.content == "!next":
        if isStarted:
            for team in range(len(teams)):
                for player in range(len(teams[team])):
                    if teams[team][player] == str(ctx.author):
                        await nextCommand(team, currentPlayer[team], ctx)
                        break
                else:
                    continue
                break
        return
    
    if ctx.content == "!prev":
        if isStarted:
            for team in range(len(teams)):
                for player in range(len(teams[team])):
                    if teams[team][player] == str(ctx.author):
                        await prevCommand(team, currentPlayer[team], ctx)
                        break
                else:
                    continue
                break
        return

    if ctx.content == "!status":
        await ctx.channel.send(f"Status:\n\
            Team #1: {teamEmblemCounts[0]} emblems, current player {teams[0][currentPlayer[0]]}\n\
            Team #2: {teamEmblemCounts[1]} emblems, current player {teams[1][currentPlayer[1]]}\n\
            Team #3: {teamEmblemCounts[2]} emblems, current player {teams[2][currentPlayer[2]]}")
        return

def refreshFinalTimes(team, clear = False):
    with open(f'resources/team{team+1}-finaltime.txt', 'w') as file:
        if clear:
            file.write("")
        else:
            file.write((teamTimes[team] - startTime + Timestamp("00:00:00")).strftime("%H:%M:%S"))

def refreshEmblemCounts(teams = [0,1,2]):
    for team in teams:
        with open(f'resources/team{team+1}-emblemcount.txt', 'w') as file:
            file.write("x"+str(teamEmblemCounts[team]))

def refreshCurrentAudio():
    global currentAudioPlayer
    
    currentTeam = 0
    for i in range(3):
        if currentAudioPlayer in teams[i]:
            currentTeam = i
            break
    if not currentPlayer[currentTeam] == teams[currentTeam].index(currentAudioPlayer):
        options = []
        for team in range(len(teamEmblemCounts)):
            if not teamEmblemCounts[team] == 56 and not team == currentTeam:
                options.append(team)
        
        if len(options) == 0 and not teamEmblemCounts[currentTeam] == 56:
            options.append(currentTeam)

        if len(options) == 0:
            return
        
        newTeam = choice(options)
        currentAudioPlayer = teams[newTeam][currentPlayer[newTeam]]

        oldFile = f"resources/team{currentTeam+1}-activeaudioicon.png"

        if os.path.exists(oldFile):
            os.rename(oldFile,f"resources/team{newTeam+1}-activeaudioicon.png")
        else:
            copy("resources/ActiveAudioIcon.png",f"resources/team{newTeam+1}-activeaudioicon.png")
    if OBS_ENABLED:     
        for i in range(3):
            for j in range(4):
                if not currentAudioPlayer == teams[i][j]:
                    ws.call(requests.SetMute(teams[i][j].split("#")[0],True))
        ws.call(requests.SetMute(currentAudioPlayer.split("#")[0],False))

    

async def nextCommand(team, player, ctx):
    global currentScene
    global teamEmblemCounts
    global teamTimes
    global startTime
    global currentPlayer
    global teamFinished
    
    player = player + 1
    player = player % 4
    currentPlayer[team] = player

    teamEmblemCounts[team]+=1
    nextPlayer = teams[team][player].split("#")[0]
    await ctx.channel.send(f"Team #{team+1} earned emblem #{teamEmblemCounts[team]}. {nextPlayer} is now the current player")

    refreshEmblemCounts([team])

    if teamEmblemCounts[team] == 56:
        teamTimes[team] = datetime.now()
        teamFinished[team] = True
        refreshFinalTimes(team)
        await ctx.channel.send(f'Team #{team+1} has finished with a time of {(teamTimes[team] - startTime + Timestamp("00:00:00")).strftime("%H:%M:%S")}')
        if all(teamFinished):
            if LIVESPLIT_ENABLED:
                timer.stopTimer()
            RelayFinished()
            switchToScene("Relay Finished")
            await ctx.channel.send("Everyone is Finished!")
            return
        
    switchToScene()

async def prevCommand(team, player, ctx):
    global currentScene
    global teamEmblemCounts
    global teamTimes
    global startTime
    global currentPlayer
    global relayFinished
    
    if teamEmblemCounts[team] == 0:
        return

    player -= 1
    if player == -1:
        player = 3
    currentPlayer[team] = player

    teamEmblemCounts[team]-=1
    prevPlayer = teams[team][player].split("#")[0]
    await ctx.channel.send(f"Revert team #{team+1} earning emblem #{teamEmblemCounts[team] + 1}. {prevPlayer} is now the current player")

    with open(f'resources/team{team+1}-emblemcount.txt', 'w') as file:
        file.write("x"+str(teamEmblemCounts[team]))

    if all(teamFinished):
        while not relayFinished:
            sleep(1)
        relayFinished = False
        
    if teamFinished:
        teamFinished[team] = False
        teamTimes[team] = 0
        refreshFinalTimes(team,True)
    switchToScene()


def readyCommand(team):
    global teamReady
    teamReady[team] = True

def unreadyCommand(team):
    global teamReady
    teamReady[team] = False

def updateSceneName():
    global currentScene

    currentScene = teams[0][currentPlayer[0]].split("#")[0] + "-"\
                  +teams[1][currentPlayer[1]].split("#")[0] + "-"\
                  +teams[2][currentPlayer[2]].split("#")[0]


def updateCurrentPlayer():
    for team in range(3):
        with open(f'resources/team{team+1}-currentplayer.txt', 'w') as file:
            file.write(str(teams[team][currentPlayer[team]].split("#")[0]))

def refreshHiddenSources():
    if OBS_ENABLED:
        for team in range(len(teams)):
            if teamFinished[team]:
                for player in range(len(teams[team])):
                    '''
                    The idea is to have teams that are complete not have streams up behind their final times, but idk how to do it unfortunately.
                    '''
                    #ws.call(requests.getSource(teams[team][player].split("#")[0]).makeInvisible())



def switchToScene(sceneName = ""):
    global currentScene

    updateSceneName()
    if not sceneName == "":
        currentScene = sceneName
    print(f"Switching Scenes to {currentScene}")
    updateCurrentPlayer()
    if OBS_ENABLED:
        ws.call(requests.SetCurrentScene(currentScene))
    refreshCurrentAudio()
    refreshHiddenSources()

def resetState():
    global startTime
    global currentScene
    global currentPlayer
    global teamEmblemCounts
    global teamTimes
    global teamReady
    global isStarted
    global relayFinished

    isStarted = False
    startTime = 0
    currentScene = 0
    currentPlayer = [
        0,
        0,
        0
    ]
    teamEmblemCounts = [
        0,
        0,
        0
    ]
    teamTimes = [
        0,
        0,
        0
    ]
    teamReady = [
        False,
        False,
        False
    ]
    relayFinished = False
    updateSceneName()
    
client = discord.Client(intents = discord.Intents(message_content = True, messages=True, voice_states=True, guilds=True))

commentators = []

def refreshCommentators():
    with open(f'resources/commentators.txt', 'w') as file:
        for commentator in commentators:
            file.write(commentator+"\n")

@client.event
async def on_voice_state_update(member, before, after):
    name = str(member).split("#")[0]
    if str(after.channel) == "Relay Commentary":
        if name not in commentators: 
            commentators.append(name)
    else:
        if name in commentators:
            commentators.remove(name)
    refreshCommentators()

@client.event
async def on_ready():
    channel = client.get_channel(BOT_CHANNEL_ID)
    await channel.send('Bot is initialized')

@client.event
async def on_message(ctx):
    if ctx.author == client.user:
        return
    await handle_command(ctx)

def RelayFinished():
    global relayFinished

    for team in range(3):
        file = [f'resources/team{team+1}-currentplayer.txt',f'resources/team{team+1}-activeaudioicon.png']

        if os.path.exists(file[0]):
            os.remove(file[0])

        if os.path.exists(file[1]):
            os.remove(file[1])

    if OBS_ENABLED:
        for i in range(3):
            for j in range(4):
                if not currentAudioPlayer == teams[i][j]:
                    ws.call(requests.SetMute(teams[i][j].split("#")[0],True))
        ws.call(requests.SetCurrentScene("Relay Finished"))

    relayFinished = True
    

print("Bot is initialized")
refreshEmblemCounts()
refreshCommentators()
switchToScene()

client.run(TOKEN)
