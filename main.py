import discord, os, random, requests, json
from discord_slash  import SlashCommand, SlashContext
from discord.utils  import get
from keep_alive     import keep_alive
from PIL            import ImageFont
from PIL            import ImageDraw
from replit         import db
from PIL            import Image
client = discord.Client(intents = discord.Intents.all())

slash = SlashCommand(client, sync_commands = True) 
valoColor = 0xff4655
global draw
global msgMasg
draw = False
drawMsg = None
global playerLst
global words
playerLst = []
guild_ids = [541302782062362664, 657669724649553990]

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    await client.change_presence(activity = discord.Activity(type = discord.ActivityType.listening, name = "vHelp"))

@client.event
async def on_raw_reaction_remove(payload):
  global draw
  global playerLst
  global drawMsg
  if draw and drawMsg is not None and payload.message_id == drawMsg.id and payload.member != client.user and str(payload.emoji) == "<:valorant:766334247072956427>" and len(playerLst) > 1:
    for player in playerLst:
      if player.id == payload.user_id:
        playerLst.remove(player)
  playerStr = ''
  for player in playerLst:
    playerStr += "<@!" + str(player.id) + ">" + "\r"
  if playerStr != '':
    await drawMsg.edit(embed = discord.Embed(title = "Team Generator:", description = "Alle 10 Spieler müssen mit <:valorant:766334247072956427> reagieren um an der Auslosung teil zu nehmen.", color = valoColor).add_field(name = 'Spieler:', value = playerStr, inline = False))
    
  if draw and drawMsg is not None and payload.message_id == drawMsg.id and payload.member != client.user and str(payload.emoji) == "<:valorant:766334247072956427>" and len(playerLst) == 1:
    for player in playerLst:
      if player.id == payload.user_id:
        playerLst.remove(player)
  playerStr = ''
  for player in playerLst:
    playerStr += "<@!" + str(player.id) + ">" + "\r"
  if playerStr == '':
    await drawMsg.edit(embed = discord.Embed(title = "Team Generator:", description = "Alle 10 Spieler müssen mit <:valorant:766334247072956427> reagieren um an der Auslosung teil zu nehmen.", color = valoColor))

@client.event
async def on_raw_reaction_add(payload):
  global drawMsg
  global playerLst
  global draw
  if drawMsg is not None and payload.message_id == drawMsg.id and payload.member != client.user and draw and str(payload.emoji) == "<:valorant:766334247072956427>":
    if payload.member not in playerLst and len(playerLst) < 10:
      playerLst.append(payload.member)
      playerStr = ''
      for player in playerLst:
        playerStr += "<@!" + str(player.id) + ">" + "\r"
      await drawMsg.edit(embed = discord.Embed(title = "Team Generator:", description = "Alle 10 Spieler müssen mit <:valorant:766334247072956427> reagieren um an der Auslosung teil zu nehmen.", color = valoColor).add_field(name = 'Spieler:', value = playerStr, inline = False))
      if len(playerLst) == 10:
        draw = False
        cLst = playerLst
        otherLst = []
        while len(cLst) > 5:
          cUser = random.choice(cLst)
          otherLst.append(cUser)
          cLst.remove(cUser)
        attacker = ""
        for user in otherLst:
          attacker += "<@!" + str(user.id) + ">" + "\r"
        defender = ""
        for user in cLst:
          defender += "<@!" + str(user.id) + ">" + "\r"
        with open('words.txt', 'r') as filehandle:
          words = json.load(filehandle)
        teams = random.choice(["Team " + random.choice(words), random.choice(words) + " Esports", random.choice(words) + " GG"]) + " VS " + random.choice(["Team " + random.choice(words), random.choice(words) + " Esports", random.choice(words) + " GG"])
        img = Image.open("vDrawSRC.png")
        draw = ImageDraw.Draw(img)
        w, h = draw.textsize(teams, font = ImageFont.truetype("Anton-Regular.ttf", 80))
        draw.text(((1920-w)/2, 130), teams, font = ImageFont.truetype("Anton-Regular.ttf", 80))
        draw.text((180, 283), otherLst[0].name, font = ImageFont.truetype("Anton-Regular.ttf", 72))
        draw.text((180, 449), otherLst[1].name, font = ImageFont.truetype("Anton-Regular.ttf", 72))
        draw.text((180, 619), otherLst[2].name, font = ImageFont.truetype("Anton-Regular.ttf", 72))
        draw.text((180, 785), otherLst[3].name, font = ImageFont.truetype("Anton-Regular.ttf", 72))
        draw.text((180, 963), otherLst[4].name, font = ImageFont.truetype("Anton-Regular.ttf", 72))
        draw.text(((1920-180)-draw.textsize(cLst[0].name, font = ImageFont.truetype("Anton-Regular.ttf", 72))[0], 283), cLst[0].name, font = ImageFont.truetype("Anton-Regular.ttf", 72))
        draw.text(((1920-180)-draw.textsize(cLst[1].name, font = ImageFont.truetype("Anton-Regular.ttf", 72))[0], 449), cLst[1].name, font = ImageFont.truetype("Anton-Regular.ttf", 72))
        draw.text(((1920-180)-draw.textsize(cLst[2].name, font = ImageFont.truetype("Anton-Regular.ttf", 72))[0], 619), cLst[2].name, font = ImageFont.truetype("Anton-Regular.ttf", 72))
        draw.text(((1920-180)-draw.textsize(cLst[3].name, font = ImageFont.truetype("Anton-Regular.ttf", 72))[0], 785), cLst[3].name, font = ImageFont.truetype("Anton-Regular.ttf", 72))
        draw.text(((1920-180)-draw.textsize(cLst[4].name, font = ImageFont.truetype("Anton-Regular.ttf", 72))[0], 963), cLst[4].name, font = ImageFont.truetype("Anton-Regular.ttf", 72))
        img.paste(Image.open(requests.get(otherLst[0].avatar_url, stream=True).raw).resize((128, 128)), (3, 266))
        img.paste(Image.open(requests.get(otherLst[1].avatar_url, stream=True).raw).resize((128, 128)), (3, 436))
        img.paste(Image.open(requests.get(otherLst[2].avatar_url, stream=True).raw).resize((128, 128)), (3, 603))
        img.paste(Image.open(requests.get(otherLst[3].avatar_url, stream=True).raw).resize((128, 128)), (3, 768))
        img.paste(Image.open(requests.get(otherLst[4].avatar_url, stream=True).raw).resize((128, 128)), (3, 947))
        img.paste(Image.open(requests.get(cLst[0].avatar_url, stream=True).raw).resize((128, 128)), (1789, 266))
        img.paste(Image.open(requests.get(cLst[1].avatar_url, stream=True).raw).resize((128, 128)), (1789, 436))
        img.paste(Image.open(requests.get(cLst[2].avatar_url, stream=True).raw).resize((128, 128)), (1789, 603))
        img.paste(Image.open(requests.get(cLst[3].avatar_url, stream=True).raw).resize((128, 128)), (1789, 768))
        img.paste(Image.open(requests.get(cLst[4].avatar_url, stream=True).raw).resize((128, 128)), (1789, 947))
        img.save('vDrawDST.png')
        file = discord.File("vDrawDST.png", filename="image.png")
        await msgMsg.channel.send(file = file, embed = discord.Embed(title = "Die Teams wurden ausgelost:", color = valoColor).add_field(name = 'Attacker:', value = attacker, inline = True).add_field(name = 'Defender:', value = defender, inline = True).set_image(url="attachment://image.png"))

@client.event
async def on_message(message):

    if message.author == client.user:
     return

    global msgMsg
    global draw
    global drawMsg
    global playerLst
    msg = message.content

    if msg.startswith('vGLHF'):
      await message.channel.send(embed = discord.Embed(description = """\
@░░░░░░██████╗░░██╗░░░░░░ @░░░░░░██╔════╝░██║░░░░░░ @░░░░░░██║░░██╗░██║░░░░░░ @░░░░░░██║░░╚██╗██║░░░░░░ @░░░░░░╚██████╔╝███████╗░ @░░░░░░░╚═════╝░╚══════╝░ @░░░░░░░░░░░░░░░░░░░░░░░░ @░░░░░░██╗░░██╗███████╗░░ @░░░░░░██║░░██║██╔════╝░░ @░░░░░░███████║█████╗░░░░ @░░░░░░██╔══██║██╔══╝░░░░ @░░░░░░██║░░██║██║░░░░░░░ @░░░░░░╚═╝░░╚═╝╚═╝░░░░░░░ """, color = valoColor))

    if msg.startswith('vGG'):
      await message.channel.send(embed = discord.Embed(description = """\
@░░░░░██████╗░░██████╗░░░ @░░░░██╔════╝░██╔════╝░░░ @░░░░██║░░██╗░██║░░██╗░░░ @░░░░██║░░╚██╗██║░░╚██╗░░ @░░░░╚██████╔╝╚██████╔╝░░ @░░░░░╚═════╝░░╚═════╝░░░   """, color = valoColor))

    if msg.startswith('vTY4T'):
      await message.channel.send(embed = discord.Embed(description = """\
@░░░░░░░░░░░░░░░░░░░░░░░░░ @░━━━━-╮░░░░░░░░░░░░░░░░░░░ @░╰┃░░┣▇━▇░░░░░░░░░░░░░░░░ @░░┃░░┃░░╰━▅╮░░░░░░░░░░░░░ @░░╰┳╯░░╰━━┳╯G░G░░░░░░░░░░░ @░░░╰╮░░┳━━╯T░Y░4░░░░░░░░░░░ @░░░▔▋░░╰╮╭━╮░T░U░T░O░R░I░A░L░ @░╱▔╲▋╰━┻┻╮╲╱▔▔▔╲░░░░░░░░░ @░▏░░▔▔▔▔▔▔▔  O O┃░░░░░░░░░ @░╲╱▔╲▂▂▂▂╱▔╲▂▂▂╱░░░░░░░░░ @░░▏╳▕▇▇▕░▏╳▕▇▇▕░░░░░░░░░░ @░░╲▂╱╲▂╱ ╲▂╱╲▂╱░░░░░░░░░░""", color = valoColor))

    if msg.startswith('vCode'):
      await message.channel.send('https://replit.com/@gookieAT/vBot')

    if msg.startswith('vHelp'):
      embed = discord.Embed(title = "Help Menu", description = "vBot is a  selfmade Discord bot programmed in Python by gookie and privataber. It is supposed to be a small relief when playing Valorant.", color = valoColor)
      embed.add_field(name = "vHelp", value = "Displays this help menu.", inline = False)
      embed.add_field(name = "vDraw", value = "Draw two teams from the players who reacted to the message.", inline = False)
      embed.add_field(name = "vMap", value = "Returns a random map from all Valorant maps.", inline = False)
      embed.add_field(name = "vCode", value = "Returns the python code from this bot.", inline = False)
      embed.add_field(name = "vGG", value = "Returns a GG ASCII art.", inline = False)
      embed.add_field(name = "vGLHF", value = "Returns a GLHF ASCII art.", inline = False)
      embed.add_field(name = "vTY4T", value = "Returns a TY4T ASCII art.", inline = False)
      await message.channel.send(embed = embed)

    if msg.startswith('vDraw'):
      draw = True
      playerLst = []
      drawMsg = await message.channel.send(embed = discord.Embed(title = "Team Generator:", description = "Alle 10 Spieler müssen mit <:valorant:766334247072956427> reagieren um an der Auslosung teil zu nehmen.", color = valoColor))
      await drawMsg.add_reaction('<:valorant:766334247072956427>')
      msgMsg = message

    if msg.startswith('vMap'):
      await message.channel.send(embed = random.choice([
        discord.Embed(title = "Ascent", description = "Es wird auf dieser Map gespielt", color = valoColor).set_image(url = 'https://cdn.discordapp.com/attachments/773615639852089394/836328630971006986/ascent.jpg'),
        discord.Embed(title = "Breeze", description = "Es wird auf dieser Map gespielt", color = valoColor).set_image(url = 'https://cdn.discordapp.com/attachments/707859321316311056/837252010876469258/Valorant-Breeze-Map-Guide-Spike-Sites-Callouts-Strategien-und-Tipps-und.png'),
        discord.Embed(title = "Bind", description = "Es wird auf dieser Map gespielt", color = valoColor).set_image(url = 'https://cdn.discordapp.com/attachments/773615639852089394/836328624243998770/bind.jpg'),
        discord.Embed(title = "Icebox", description = "Es wird auf dieser Map gespielt", color = valoColor).set_image(url = 'https://cdn.discordapp.com/attachments/773615639852089394/836328633647890432/icebox.jpg'),
        discord.Embed(title = "Haven", description = "Es wird auf dieser Map gespielt", color = valoColor).set_image(url = 'https://cdn.discordapp.com/attachments/773615639852089394/836328634151075941/haven.jpg'),
        discord.Embed(title = "Split", description = "Es wird auf dieser Map gespielt", color = valoColor).set_image(url = 'https://cdn.discordapp.com/attachments/773615639852089394/836328629993865216/split.jpg'),]))

@slash.slash(name = 'help', description = 'Displays a help menu.', guild_ids = guild_ids)
async def help(ctx):
    embed = discord.Embed(title = "Help Menu", description = "vBot is a  selfmade Discord bot programmed in Python by gookie and privataber. It is supposed to be a small relief when playing Valorant.", color = valoColor)
    embed.add_field(name = "vHelp", value = "Displays this help menu.", inline = False)
    embed.add_field(name = "vDraw", value = "Draw two teams from the players who reacted to the message.", inline = False)
    embed.add_field(name = "vMap", value = "Returns a random map from all Valorant maps.", inline = False)
    embed.add_field(name = "vCode", value = "Returns the python code from this bot.", inline = False)
    embed.add_field(name = "vGG", value = "Returns a GG ASCII art.", inline = False)
    embed.add_field(name = "vGLHF", value = "Returns a GLHF ASCII art.", inline = False)
    embed.add_field(name = "vTY4T", value = "Returns a TY4T ASCII art.", inline = False)
    await ctx.send(embed = embed)

@slash.slash(name = 'draw', description = 'Draw two teams from the players who reacted to the message.', guild_ids = guild_ids)
async def draw(ctx):
    global msgMsg
    global draw
    global drawMsg
    global playerLst
    draw = True
    playerLst = []
    drawMsg = await ctx.send(embed = discord.Embed(title = "Team Generator:", description = "Alle 10 Spieler müssen mit <:valorant:766334247072956427> reagieren um an der Auslosung teil zu nehmen.", color = valoColor))
    await drawMsg.add_reaction('<:valorant:766334247072956427>')
    msgMsg = ctx

@slash.slash(name = 'map', description = 'Returns a random map from all Valorant maps.', guild_ids = guild_ids)
async def map(ctx):
    await ctx.send(embed = random.choice([
        discord.Embed(title = "Ascent", description = "Es wird auf dieser Map gespielt", color = valoColor).set_image(url = 'https://cdn.discordapp.com/attachments/773615639852089394/836328630971006986/ascent.jpg'),
        discord.Embed(title = "Breeze", description = "Es wird auf dieser Map gespielt", color = valoColor).set_image(url = 'https://cdn.discordapp.com/attachments/707859321316311056/837252010876469258/Valorant-Breeze-Map-Guide-Spike-Sites-Callouts-Strategien-und-Tipps-und.png'),
        discord.Embed(title = "Bind", description = "Es wird auf dieser Map gespielt", color = valoColor).set_image(url = 'https://cdn.discordapp.com/attachments/773615639852089394/836328624243998770/bind.jpg'),
        discord.Embed(title = "Icebox", description = "Es wird auf dieser Map gespielt", color = valoColor).set_image(url = 'https://cdn.discordapp.com/attachments/773615639852089394/836328633647890432/icebox.jpg'),
        discord.Embed(title = "Haven", description = "Es wird auf dieser Map gespielt", color = valoColor).set_image(url = 'https://cdn.discordapp.com/attachments/773615639852089394/836328634151075941/haven.jpg'),
        discord.Embed(title = "Split", description = "Es wird auf dieser Map gespielt", color = valoColor).set_image(url = 'https://cdn.discordapp.com/attachments/773615639852089394/836328629993865216/split.jpg'),]))

@slash.slash(name = 'code', description = 'Returns the python code from this bot.', guild_ids = guild_ids)
async def code(ctx):
    await ctx.send('https://replit.com/@gookieAT/vBot')

@slash.slash(name = 'gg', description = 'Returns a GG ASCII art.', guild_ids = guild_ids)
async def gg(ctx):
    await ctx.send(embed = discord.Embed(description = """\
@░░░░░██████╗░░██████╗░░░ @░░░░██╔════╝░██╔════╝░░░ @░░░░██║░░██╗░██║░░██╗░░░ @░░░░██║░░╚██╗██║░░╚██╗░░ @░░░░╚██████╔╝╚██████╔╝░░ @░░░░░╚═════╝░░╚═════╝░░░   """, color = valoColor))

@slash.slash(name = 'glhf', description = 'Returns a GLHF ASCII art.', guild_ids = guild_ids)
async def glhf(ctx):
    await ctx.send(embed = discord.Embed(description = """\
@░░░░░░██████╗░░██╗░░░░░░ @░░░░░░██╔════╝░██║░░░░░░ @░░░░░░██║░░██╗░██║░░░░░░ @░░░░░░██║░░╚██╗██║░░░░░░ @░░░░░░╚██████╔╝███████╗░ @░░░░░░░╚═════╝░╚══════╝░ @░░░░░░░░░░░░░░░░░░░░░░░░ @░░░░░░██╗░░██╗███████╗░░ @░░░░░░██║░░██║██╔════╝░░ @░░░░░░███████║█████╗░░░░ @░░░░░░██╔══██║██╔══╝░░░░ @░░░░░░██║░░██║██║░░░░░░░ @░░░░░░╚═╝░░╚═╝╚═╝░░░░░░░ """, color = valoColor))

@slash.slash(name = 'ty4t', description = 'Returns a TY4T ASCII art.', guild_ids = guild_ids)
async def ty4t(ctx):
    await ctx.send(embed = discord.Embed(description = """\
@░░░░░░░░░░░░░░░░░░░░░░░░░ @░━━━━-╮░░░░░░░░░░░░░░░░░░░ @░╰┃░░┣▇━▇░░░░░░░░░░░░░░░░ @░░┃░░┃░░╰━▅╮░░░░░░░░░░░░░ @░░╰┳╯░░╰━━┳╯G░G░░░░░░░░░░░ @░░░╰╮░░┳━━╯T░Y░4░░░░░░░░░░░ @░░░▔▋░░╰╮╭━╮░T░U░T░O░R░I░A░L░ @░╱▔╲▋╰━┻┻╮╲╱▔▔▔╲░░░░░░░░░ @░▏░░▔▔▔▔▔▔▔  O O┃░░░░░░░░░ @░╲╱▔╲▂▂▂▂╱▔╲▂▂▂╱░░░░░░░░░ @░░▏╳▕▇▇▕░▏╳▕▇▇▕░░░░░░░░░░ @░░╲▂╱╲▂╱ ╲▂╱╲▂╱░░░░░░░░░░""", color = valoColor))

@slash.slash(name = 'status', description = 'Returns the status from vBot.', guild_ids = guild_ids)
async def status(ctx):
    await ctx.send("https://vbot.betteruptime.com/")

@slash.slash(name = 'rank', description = 'Returns the current rank from the player.', guild_ids = guild_ids, options = [{"name" : "name", "description" : "Use your ingame-name.", "required" : True, "type" : 3}, {"name" : "tagline", "description" : "Use your ingame-tagline without #", "required" : True, "type" : 3}, {"name" : "region", "description" : "Use EU, NA, AP or KR", "required" : True, "type" : 3}, {"name" : "save", "description" : "It links/unlinks the Valorant account to your Discord profile so you can use the /myrank command.", "required" : False, "type" : 5}])
async def rank(ctx : SlashContext, name, tagline, region, save = None):
  if region.lower() not in ["eu", "na", "ap", "kr"]:
    await ctx.send(embed = discord.Embed(title = "Wrong region!", description = "You can use EU, NA, AP or KR", color = valoColor))
    return
  if save is True:
    value = json.dumps({"name": name, "tagline": tagline, "region": region})
    db[str(ctx.author_id)] = value
  if save is False:
    del db[str(ctx.author_id)]
  request = requests.get('https://api.henrikdev.xyz/valorant/v1/mmr/' + region + "/" + name + "/" + tagline).text
  request2 = requests.get('https://api.henrikdev.xyz/valorant/v1/puuid/' + name + "/" + tagline).text
  data = json.loads(request)
  data2 = json.loads(request2)
  data = data["data"]
  data2 = data2["data"]
  embed=discord.Embed(title = "Valorant Rank", color = valoColor)
  file = discord.File("TX_CompetitiveTier_Large_" + str(data["currenttier"]) + ".png", filename="image.png")
  embed.set_thumbnail(url = "attachment://image.png")
  embed.add_field(name = "Player", value = name + "#" + tagline, inline = True)
  embed.add_field(name = "Rank", value = data["currenttierpatched"], inline = True)
  embed.add_field(name = "Elo", value = data["elo"], inline = True)
  embed.add_field(name = "Last competitive game", value = data["mmr_change_to_last_game"], inline = True)
  await ctx.send(file = file, embed = embed)

@slash.slash(name = 'myrank', description = 'Returns the rank from the saved player.', guild_ids = guild_ids)
async def myral(ctx):
  try:
    value = db[str(ctx.author_id)]
    value = json.loads(value)
  except:
    await ctx.send("Your Discord account is not connected to any Valorant account. First use the command /rank with the option save = True.")
    return
  name = value["name"]
  tagline = value["tagline"]
  region = value["region"]
  request = requests.get('https://api.henrikdev.xyz/valorant/v1/mmr/' + region + "/" + name + "/" + tagline).text
  request2 = requests.get('https://api.henrikdev.xyz/valorant/v1/puuid/' + name + "/" + tagline).text
  data = json.loads(request)
  data2 = json.loads(request2)
  data = data["data"]
  data2 = data2["data"]
  role = get(ctx.guild.roles, name = data["currenttierpatched"][:-2])
  await ctx.author.add_roles(role)
  embed=discord.Embed(title = "Valorant Rank", color = valoColor)
  file = discord.File("TX_CompetitiveTier_Large_" + str(data["currenttier"]) + ".png", filename="image.png")
  embed.set_thumbnail(url = "attachment://image.png")
  embed.add_field(name = "Player", value = name + "#" + tagline, inline = True)
  embed.add_field(name = "Rank", value = data["currenttierpatched"], inline = True)
  embed.add_field(name = "Elo", value = data["elo"], inline = True)
  embed.add_field(name = "Last competitive game", value = data["mmr_change_to_last_game"], inline = True)
  await ctx.send(file = file, embed = embed)

@slash.slash(name = 'invite', description = 'Returns the invite link of this server.', guild_ids = guild_ids)
async def invite (ctx):
  await ctx.send('https://discord.gg/ua8WbStHvA')

keep_alive()
client.run(os.getenv('TOKEN'))