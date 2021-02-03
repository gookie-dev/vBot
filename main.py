import discord, os, random
from functions import asciiArt
from keep_alive import keep_alive

client = discord.Client()


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')


@client.event
async def on_message(message):
    if message.author == client.user:
        return


    msg = message.content
    valoColor = 0xff4655
    draw = True


    ### team generator ###

    if msg.startswith('vAdd'):
      if draw:
        userStr = msg[5:]
        userLst = userStr.split(" ")
        otherLst = []
        while len(userLst) > 5:
          cUser = random.choice(userLst)
          otherLst.append(cUser)
          userLst.remove(cUser)
        attacker = ""
        for user in otherLst:
          attacker += user + "\r"
        defender = ""
        for user in userLst:
          defender += user + "\r"
        await message.channel.send(embed = discord.Embed(title = "Die Teams wurden ausgelost:", color = valoColor)
        .add_field(name = 'Attacker:', value = attacker, inline = True)
        .add_field(name = 'Defender:', value = defender, inline = True))


    ### map generator ###

    if msg.startswith('vMap'):
      await message.channel.send(embed = random.choice([
        discord.Embed(title = "Ascent", description = "Es wird auf dieser Map gespielt", color = valoColor).set_image(url = 'https://i.imgur.com/qcp6cno.jpg'),
        discord.Embed(title = "Bind", description = "Es wird auf dieser Map gespielt", color = valoColor).set_image(url = 'https://i.imgur.com/ksQA601.jpg'),
        discord.Embed(title = "Icebox", description = "Es wird auf dieser Map gespielt", color = valoColor).set_image(url = 'https://i.imgur.com/V9DIq0s.jpg'),
        discord.Embed(title = "Haven", description = "Es wird auf dieser Map gespielt", color = valoColor).set_image(url = 'https://i.imgur.com/YNd5dLw.jpg'),
        discord.Embed(title = "Split", description = "Es wird auf dieser Map gespielt", color = valoColor).set_image(url = 'https://i.imgur.com/hKoKFAO.jpg'),]))


    ### fun ###

    if msg.startswith('vPing'):
        await message.channel.send('Pong')


    if msg.startswith('vGLHF'):
        embed = discord.Embed(description = asciiArt('GLHF'), color = valoColor)
        await message.channel.send(embed = embed)


    if msg.startswith('vGG'):
        embed = discord.Embed(description = asciiArt('GG'), color = valoColor)
        await message.channel.send(embed = embed)


    if msg.startswith('vTY4T'):
        embed = discord.Embed(description = asciiArt('TY4T'), color = valoColor)
        await message.channel.send(embed = embed)

keep_alive()
client.run(os.getenv('TOKEN'))