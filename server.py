from flask import Flask, request, jsonify
import discord
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
DISCORD_TOKEN = os.getenv("MTMxNzg1NjcwNjc0MjQ1MjI3NA.Gvck4a.y-vZ2deUwrSxeQuVKNsZWOTsJLvfmisdlOQZSY")
GUILD_ID = int(os.getenv("1251889614776696943"))  # 디스코드 서버 ID
ROBLOX_TO_DISCORD = {
    "123456": "987654321",  # Roblox ID -> Discord ID 매핑
}

intents = discord.Intents.default()
intents.guilds = True
intents.guild_members = True

client = discord.Client(intents=intents)

@app.route("/team-change", methods=["POST"])
def team_change():
    data = request.json
    roblox_id = str(data.get("RobloxId"))
    new_team = data.get("NewTeam")

    discord_id = ROBLOX_TO_DISCORD.get(roblox_id)
    if not discord_id:
        return jsonify({"error": "Discord ID not found"}), 404

    asyncio.run_coroutine_threadsafe(update_role(discord_id, new_team), client.loop)
    return jsonify({"status": "success"}), 200

async def update_role(discord_id, team_name):
    guild = client.get_guild(GUILD_ID)
    member = guild.get_member(int(discord_id))

    if not member:
        print(f"Member with ID {discord_id} not found")
        return

    # 역할 이름을 팀 이름과 매칭
    role = discord.utils.get(guild.roles, name=team_name)
    if not role:
        print(f"Role '{team_name}' not found")
        return

    # 기존 역할 제거 후 새 역할 추가
    await member.edit(roles=[role])
    print(f"Updated role for {member.display_name} to {role.name}")

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")

if __name__ == "__main__":
    client.loop.create_task(client.start(DISCORD_TOKEN))
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
