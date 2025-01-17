import discord
from discord.ext import commands
import requests

bot = commands.Bot(command_prefix='/')

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.command()
async def 인증(ctx, code: str):
    user_id = str(ctx.author.id)
    url = "https://teamchange-9b5cf8e928e3.herokuapp.com/verify"
    response = requests.post(url, json={'code': code, 'discord_id': user_id})
    data = response.json()

    if data['success']:
        role = discord.utils.get(ctx.guild.roles, name="Verified")
        await ctx.author.add_roles(role)
        await ctx.send("인증이 성공했습니다! 역할이 부여되었습니다.")
    else:
        await ctx.send("인증에 실패했습니다. 다시 시도해 주세요.")

bot.run('MTMyOTA0NDQ0MTU5MTMyMDY4Nw.GRvupJ.d5uQkQTJSm0N52QtTHD-Gu9vt15sX00KQIvDs8')
