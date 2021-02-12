import discord
from discord.ext import commands
import os
import asyncio
import firebase_admin
from firebase_admin import credentials, firestore
import json



configvars = {
    "type": "service_account",
    "project_id": os.environ.get("project_id"),
    "private_key": os.environ.get('private_key').replace('\\n', '\n'),
    "client_email": os.environ.get("client_email"),
    "client_id": os.environ.get("client_id"), 
    "auth_uri": os.environ.get("auth_uri"),
    "token_uri": os.environ.get("token_uri"),
    "auth_provider_x509_cert_url": os.environ.get("auth_provider_x509_cert_url"),
    "client_x509_cert_url": os.environ.get("client_x509_cert_url")
}

json.dump(configvars, open('stuffs.json', 'w'))
cred = credentials.Certificate('stuffs.json')
default_app = firebase_admin.initialize_app(cred)
intents = discord.Intents.default()
db = firestore.client()

doc_ref = db.collection("guilds").document(str(msg.guild.id))
data = doc_ref.get().to_dict()
# now you have data.prefix as the prefix

intents.guilds = True
intents.members = True
client = commands.Bot(command_prefix=commands.when_mentioned_or(str(data.prefix)), intents = intents)
client.remove_command("help")
TOKEN = TOKEN = os.environ.get("TOKEN")


#cred = credentials.Certificate('stuffs.json')
#default_app = firebase_admin.initialize_app(cred)

#work?


# make sure I am doing this
def is_it_me(ctx):
    return ctx.author.id == 654142589783769117


# Help
class MyHelpCommand(commands.MinimalHelpCommand):
    async def send_pages(self):
        destination = self.get_destination()
        e = discord.Embed(color=discord.Color(0x9ef), description='')
        for page in self.paginator.pages:
            e.description += page
        await destination.send(embed=e)

client.help_command = MyHelpCommand()




# Commands
@client.command(aliases=["pong"],description="Returns the latency of the bot.")
async def ping(ctx):
    embed = discord.Embed(
        title="PING",
        description=
        f":ping_pong: Pong! The ping is **{round(client.latency *1000)}** milliseconds!",
        color=0x00ff00)
    await ctx.send(embed=embed)

@client.command(hidden=True)
async def credits(ctx):
    em = discord.Embed(
        title="Credits",
        description=
        "Creator/Owner: <insert name here>#XXXX\nProfile Picture: <insert name here>#XXXX\nBig helpers and contributers: ElectronDev and Fumseck of Zeldevs, Isukali"
    )
    em.set_footer(text = "If you found this command, have a cookie :cookie: lol. :)")
    await ctx.send(embed=em)

#prefix command. gives bot prefix
@client.command(description="Returns the prefix of the bot. \nif you add an argument, it changes the bot's prefix.`BETA` (custom prefix doesnt work yet)")
async def prefix(ctx, prefix = None):
    embed1 = discord.Embed(
        title='Prefix',
        description=f"This Bot's prefix is `>>`",
        color=discord.Color.blue())
    embed2 = discord.Embed(
        title='Prefix',
        description=f"This Bot's prefix has been changed to `{prefix}`",
        color=discord.Color.green())
    doc_ref = db.collection('guild').document(str(ctx.guild.id))

    if prefix == None:
        
        await ctx.send(embed=embed1)
    else:
        doc_ref.set({
            'prefix': prefix
        }, merge = True)
        await ctx.send(embed=embed2)

@client.command(hidden=True)
@commands.check(is_it_me)
async def sudosay(ctx,type,  location, *, content):
    location = location.replace("<", "")
    location = location.replace(">", "")
    location = location.replace("@!", "")
    location = location.replace("#", "")
    if type =="user":
          channel = client.get_user(int(location))
    elif type =="channel":
          channel = client.get_channel(int(location))
    await channel.send(content)
    await ctx.send(f"Sent to {channel.name} successfully.")

@sudosay.error
async def ssay_error(error, ctx):
    em1 = discord.Embed(title = "Sudosay Command", description="`>>sudosay <channel | user> <id of user/channel> <content>", color = discord.Color(0xf00))
    if isinstance(error, discord.ext.commands.errors.BadArgument): 
        await ctx.send("honestly this is a BadArgument Error",embed=em1)
    elif isinstance(error, discord.ext.commands.errors.MissingPermissions): 
        await ctx.send("This bot cannot send messages here.", embed = em1)
    elif isinstance(error, discord.ext.commands.errors.MissingRequiredArgument, embed= em1): 
        await ctx.send("are you missing something?")
    else:
        await ctx.send(f"```\n{error}\n\nPlease try again and stuff.", embed = em1)
        raise error





# Cog stuff
cogs = ['cogs.utils', 'cogs.moderation', 'cogs.fun', 'cogs.say', 'cogs.info'] #'cogs.events', 

for cog in cogs:
    try:
        client.load_extension(cog)
    except Exception as e:
        print(f"e1: Could not load cog {cog}:{str(e)}")


# alerts if bot is ready
@client.event
async def on_ready():
    await client.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name="404: <insert movie here> not found"))
    print("<Bot is Ready.>")


#Load cog
@client.command(hidden=True)
@commands.check(is_it_me)
async def loadcog(ctx, cogname=None, hidden=True):
    if cogname is None:
        await ctx.send("-_-")
        return
    try:
        client.load_extension(cogname)
    except Exception as e:
        print(f"Could not load cog {cog}:{str(e)}")
        await ctx.send("-_-")
    else:
        print('Loaded Cog Succesfully')
        await ctx.send(f"{cog} is online.")


#Unload cog
@client.command(hidden=True)
@commands.check(is_it_me)
async def unloadcog(ctx, cogname=None, hidden=True):
    if cogname is None:
        return
        await ctx.send("-_-")
    try:
        client.unload_extension(cogname)
    except Exception as e:
        print(f"Could not unload cog {cog}:{str(e)}")
        await ctx.send("-_-")
    else:
        print('Unloaded Cog Succesfully')
        await ctx.send(f"{cog} is offline.")


        
client.run(TOKEN)