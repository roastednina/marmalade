import discord
from discord.ext import commands
from datetime import datetime

# ====== サーバー設定 ======
SERVER_SETTINGS = {
    1494675235226783776: {  # ←サーバーID
        "normal_role": 1494681199925395587,
        "late_role": 1494681285090742343,
        "channel": 1494856055635841044
    }
}
# =========================

intents = discord.Intents.default()
intents.voice_states = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"ログイン成功: {bot.user}")

@bot.event
async def on_voice_state_update(member, before, after):

  　 print("イベントきた", member.name)
    print("before:", before.channel)
    print("after:", after.channel)

    # 入室したときだけ
    if before.channel is None and after.channel is not None:

        channel = after.channel

        # 人間だけカウント
        members = [m for m in channel.members if not m.bot]

        # 最初の1人だけ
        if len(members) == 1:

            hour = datetime.now().hour
            is_late_night = 0 <= hour < 6

            guild_id = member.guild.id

            if guild_id not in SERVER_SETTINGS:
                return

            config = SERVER_SETTINGS[guild_id]

            role_id = config["late_role"] if is_late_night else config["normal_role"]
            text_channel = bot.get_channel(config["channel"])

            if text_channel:

                # 🎀 色（深夜はちょっと落ち着かせる）
                if is_late_night:
                    color = discord.Color.from_rgb(180, 150, 200)  # 落ち着き紫
                    footer_text = "よふかししすぎないでね 🐾"
                else:
                    color = discord.Color.from_rgb(255, 182, 193)  # ピンク
                    footer_text = "あそびにおいで〜 🐾"

                embed = discord.Embed(
                    title="🐾 だれか来たよ〜",
                    description=f"✨ {member.mention} が {channel.name} に入ったよっ",
                    color=color
                )

                embed.set_thumbnail(url=member.display_avatar.url)

                embed.set_author(
                    name=f"{member.display_name} さん",
                    icon_url=member.display_avatar.url
                )

                embed.set_footer(text=footer_text)

                await text_channel.send(
                    content=f"<@&{role_id}>",
                    embed=embed
                )

# ====== トークン ======
import os
bot.run(os.getenv("TOKEN"))

