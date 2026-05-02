import discord
import os
from datetime import datetime, timedelta

intents = discord.Intents.default()
intents.voice_states = True
intents.message_content = True

client = discord.Client(intents=intents)

# ====== サーバー設定 ======
SERVER_SETTINGS = {
    1494675235226783776: {  # ←サーバーID
        "normal_role": 1494681199925395587,
        "late_role": 1494681285090742343,
        "channel": 1494856055635841044
    }
}
# =========================

@client.event
async def on_ready():
    print(f"ログインしたよ: {client.user}")

@client.event
async def on_voice_state_update(member, before, after):

    # 入室したときだけ
    if before.channel is None and after.channel is not None:

        channel = after.channel

        # 🔇 フリールーム（OParty Beastなど）を無視
        if channel.name.startswith("free"):
            return

        # 人間だけカウント
        members = [m for m in channel.members if not m.bot]

        # 最初の1人だけ
        if len(members) == 1:

            # 🇯🇵 日本時間
            hour = (datetime.utcnow() + timedelta(hours=9)).hour
            is_late_night = 0 <= hour < 6

            guild_id = member.guild.id

            if guild_id not in SERVER_SETTINGS:
                return

            config = SERVER_SETTINGS[guild_id]

            # ロール取得
            normal_role = member.guild.get_role(config["normal_role"])
            late_role = member.guild.get_role(config["late_role"])

            # チャンネル取得
            notify_channel = client.get_channel(config["channel"])

            # ロール付与
            if is_late_night:
                if late_role:
                    await member.add_roles(late_role)
            else:
                if normal_role:
                    await member.add_roles(normal_role)

            # 通知
            if notify_channel:
                if is_late_night:
                    await notify_channel.send(f"🌙 {member.mention} が深夜にVC参加！")
                else:
                    await notify_channel.send(f"☀️ {member.mention} がVC参加！")


client.run(os.environ['DISCORD_BOT_TOKEN'])
