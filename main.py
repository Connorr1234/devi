import discord
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions
import json
import asyncio


def get_prefix(client, message):
    try:
        with open('data/prefixes.json', 'r') as f:
            prefixes = json.load(f)

        return prefixes[str(message.guild.id)]
    except:
        return '?'

description = '''Bot coded in discord.py by ruperrt#0001'''
bot = commands.Bot(command_prefix=get_prefix, description=description)

bot.remove_command("help")

with open('data/reports.json', encoding='utf-8') as f:
  try:
    report = json.load(f)
  except ValueError:
    report = {}
    report['users'] = []

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print('------')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="?help Vers 1.0"))
    
@bot.event
async def on_member_join(member):
    role = discord.utils.get(member.guild.roles, id="725430416944791564")
    await bot.add_roles(member, role)
    

@bot.command()
async def help(ctx):
        em = discord.Embed(title="Devi Help", description="", color=0x00a8ff)
        em.add_field(name="`?ban`", value="Bans the user provided from the discord server that he is on.")
        em.add_field(name="`?mute`", value="This command gives a user a 'Muted' Role. They are now muted.")
        em.add_field(name="`?kick`", value="This command Kicks a user from the discord server..")
        em.add_field(name="`?prefix`", value="Changes the bot prefix.")
        em.add_field(name="`?new`", value="This command creates a new ticket for support.")
        em.add_field(name="`?close`", value="This command closes a open ticket.")
        em.add_field(name="`?warn`", value="This command can be used to warn a user and then a reason provided.")
        em.add_field(name="`?purge`", value="This command purges a certain amount of messages in a channel.")
        em.add_field(name="`?slowmode`", value="Sets a slowmode delay of a channel.")
        em.set_footer(text="Devi by ruperrt#0001 Vers 1.0")
        await ctx.send(embed=em)
        
@bot.command()
async def ping(ctx):

    start = time.monotonic()
    msg = await ctx.send('Pinging...')
    millis = (time.monotonic() - start) * 1000
    heartbeat = ctx.bot.latency * 1000
    em = discord.Embed(title="Ping", description=f'Ping: {heartbeat:,.2f}ms\t', color=0x00a8ff)
    await msg.edit(embed=em)

        
@bot.command()
async def poll(msg,*,pollquestion):
  embed=discord.Embed(title=pollquestion, color=0x0000ff)
  embed.set_author(name=msg.author,icon_url=msg.author.avatar_url)
  embed.set_footer(text="Devi by ruperrt#0001 Vers 1.0")
  pineapple = await msg.send(embed=embed)

  poo = "\U0001f44d"
  wee = "\U0001f44e"
  await pineapple.add_reaction(poo)
  await pineapple.add_reaction(wee)
    
@bot.command()    
@commands.has_permissions(manage_messages=True)
async def slowmode(ctx, delay: int):
  if not 0 <= delay <= 21600:
    return await ctx.send("Invalid delay. Please input delay between 0 (off) and 21600.")
  await ctx.channel.edit(slowmode_delay=delay)
    
@bot.command()
async def invite(ctx):
    try:
        await ctx.author.send("https://discord.com/oauth2/authorize?client_id=725386908959506602&scope=bot&permissions=>")
        em = discord.Embed(title="Complete", description="", color=0x00a8ff)
        em.add_field(name="Hello,", value="Please check your private messages")
        em.set_footer(text="Devi by ruperrt#0001 Vers 1.0")
        await ctx.send(embed=em)
    except:
        em = discord.Embed(title="Error", description="", color=0x00a8ff)
        em.add_field(name="Hello,", value="Unable to send, your private messages are turnt off")
        em.set_footer(text="Devi by ruperrt#0001 Vers 1.0")
        await ctx.send(embed=em)

@bot.command()
@has_permissions(administrator=True)
async def prefix(ctx, prefix):
    """
    Changes the server prefix for the bot!
    """
    with open('data/prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes[str(ctx.guild.id)] = prefix

    with open('data/prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)
    embed=discord.Embed(title="The bots prefix is now:", description=f"{prefix}")
    embed.set_author(name="Prefix changed")
    embed.set_footer(text="Devi by ruperrt#0001 Vers 1.0")
    await ctx.send(embed=embed)


@bot.command(aliases=['stats'])
async def info(ctx):
    embed = discord.Embed(title="Bot Statistics", colour=0x36393E)
    embed.set_author(name="Devi",
                    icon_url="https://cdn.discordapp.com/attachments/725385942273228853/725405454364311592/e0407c8de9ac65037f069a8324c28bf0.png")
    embed.set_footer(text="Creator: ruperrt#0001 | Devi v1.0",
                    icon_url="https://cdn.discordapp.com/avatars/722537801970876527/1711a32482ff5f6ba303e46a6ee30b3f.png?size=1024")
    embed.add_field(name="**Some Info**", value="**Developer:** <@531737282982445066>\n**Coded in:** discord.py\n**Support:** https://discord.gg/Z7dPexg")
    embed.add_field(name="**Bot Stats**", value=f"**Bot Users:** {len(bot.users)}\n**Servers using me:** {len(bot.guilds)}")
        
    await ctx.send(embed=embed)






@bot.command()
@has_permissions(kick_members=True)
async def kick(ctx, member : discord.Member, *, reason=None):
    await member.kick(reason=reason)
    embed=discord.Embed(title="Kick", description="Member Successfully Kicked.")
    embed.set_footer(text="Devi by ruperrt#0001 Vers 1.0")
    await ctx.send(embed=embed)

@bot.command()
@has_permissions(ban_members=True)
async def ban(ctx, member : discord.Member, *, reason=None):
    await member.ban(reason=reason)
    embed=discord.Embed(title="Ban", description="Member Successfully Banned.")
    embed.set_footer(text="Devi by ruperrt#0001 Vers 1.0")
    await ctx.send(embed=embed)

@bot.command()
@has_permissions(administrator=True)
async def mute(ctx, user: discord.Member):
    role = discord.utils.get(ctx.guild.roles, name="Muted")
    await user.add_roles(role)
    await ctx.send("Member Successfully Muted!")

@bot.command()
@has_permissions(administrator=True)
async def unmute(ctx, user: discord.Member):
    role = discord.utils.get(ctx.guild.roles, name="Muted")
    await user.remove_roles(role)
    await ctx.send("Member Successfully Unmuted!")

@bot.command()
@has_permissions(administrator=True)
async def announce(ctx, *,announcement):
    channel = bot.get_channel(725445110896001114)
    embed=discord.Embed(title="New Announcement!", description=(announcement))
    embed.set_footer(text="Devi by ruperrt#0001 Vers 1.0")
    await channel.send(embed=embed)

@bot.command(pass_context = True)
@has_permissions(manage_roles=True, ban_members=True)
async def warn(ctx,user:discord.User,*reason:str):
  if not reason:
    await ctx.send("Please provide a reason")
    return
  reason = ' '.join(reason)
  for current_user in report['users']:
    if current_user['name'] == user.name:
      current_user['reasons'].append(reason)
      break

  else:
    report['users'].append({
      'name':user.name,
      'reasons': [reason,]
    })
  with open('data/reports.json','w+') as f:
    json.dump(report,f)
    await ctx.send("User Successfully warned!")
                              

@bot.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def purge(ctx, limit: int):
      await ctx.channel.purge(limit=limit)
      await ctx.send('Cleared by {}'.format(ctx.author.mention))


@bot.command(pass_context = True)
async def warnings(ctx,user:discord.User):
  for current_user in report['users']:
    if user.name == current_user['name']:
      await ctx.send(f"{user.name} has been reported {len(current_user['reasons'])} times : {','.join(current_user['reasons'])}")
      break
  else:
    await ctx.send(f"{user.name} has never been reported")  

@bot.command()
async def new(ctx, *, args = None):

    await bot.wait_until_ready()

    if args == None:
        message_content = "Please wait, we will be with you shortly!"
    
    else:
        message_content = "".join(args)

    with open("data/data.json") as f:
        data = json.load(f)

    ticket_number = int(data["ticket-counter"])
    ticket_number += 1

    ticket_channel = await ctx.guild.create_text_channel("ticket-{}".format(ticket_number))
    await ticket_channel.set_permissions(ctx.guild.get_role(ctx.guild.id), send_messages=False, read_messages=False)

    for role_id in data["valid-roles"]:
        role = ctx.guild.get_role(role_id)

        await ticket_channel.set_permissions(role, send_messages=True, read_messages=True, add_reactions=True, embed_links=True, attach_files=True, read_message_history=True, external_emojis=True)
    
    await ticket_channel.set_permissions(ctx.author, send_messages=True, read_messages=True, add_reactions=True, embed_links=True, attach_files=True, read_message_history=True, external_emojis=True)

    em = discord.Embed(title="New ticket from {}#{}".format(ctx.author.name, ctx.author.discriminator), description= "{}".format(message_content), color=0x00a8ff)
    em.set_footer(text="Devi by ruperrt#0001 Vers 1.0")
                     
    await ticket_channel.send(embed=em)

    pinged_msg_content = ""
    non_mentionable_roles = []

    if data["pinged-roles"] != []:

        for role_id in data["pinged-roles"]:
            role = ctx.guild.get_role(role_id)

            pinged_msg_content += role.mention
            pinged_msg_content += " "

            if role.mentionable:
                pass
            else:
                await role.edit(mentionable=True)
                non_mentionable_roles.append(role)
        
        await ticket_channel.send(pinged_msg_content)

        for role in non_mentionable_roles:
            await role.edit(mentionable=False)
    
    data["ticket-channel-ids"].append(ticket_channel.id)

    data["ticket-counter"] = int(ticket_number)
    with open("data/data.json", 'w') as f:
        json.dump(data, f)
    
    created_em = discord.Embed(title="Devi Tickets", description="Your ticket has been created at {}".format(ticket_channel.mention), color=0x00a8ff)
    
    await ctx.send(embed=created_em)

@bot.command()
async def close(ctx):
    with open('data/data.json') as f:
        data = json.load(f)

    if ctx.channel.id in data["ticket-channel-ids"]:

        channel_id = ctx.channel.id

        def check(message):
            return message.author == ctx.author and message.channel == ctx.channel and message.content.lower() == "close"

        try:

            em = discord.Embed(title="Devi Tickets", description="Are you sure you want to close this ticket? Reply with `close` if you are sure.", color=0x00a8ff)
        
            await ctx.send(embed=em)
            await bot.wait_for('message', check=check, timeout=60)
            await ctx.channel.delete()

            index = data["ticket-channel-ids"].index(channel_id)
            del data["ticket-channel-ids"][index]

            with open('data/data.json', 'w') as f:
                json.dump(data, f)
        
        except asyncio.TimeoutError:
            embed = discord.Embed(title="Devi Tickets", description="You have run out of time to close this ticket. Please run the command again.", color=0x00a8ff)
            await ctx.send(embed=embed)







bot.run('lol")               
 
