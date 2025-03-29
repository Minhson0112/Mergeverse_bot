import discord
from discord import app_commands
from discord.ext import commands
import requests
from ..utils.channel_check import is_channel_allowed
from bot.config import BACKEND_HOST

url = f"{BACKEND_HOST}/api/local-rank"

class LocalRank(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="localrank", description="Hiển thị top 10 trong server và thứ hạng của bạn")
    async def local_rank(self, interaction: discord.Interaction):
        if not await is_channel_allowed(interaction):
            await interaction.response.send_message(
                "⚠️ Bot không được phép hoạt động ở kênh này. Hãy dùng lệnh `/setchannel` để thiết lập.",
                ephemeral=True
            )
            return
        
        discord_id = interaction.user.id
        guild_id = interaction.guild.id if interaction.guild else None

        if not guild_id:
            await interaction.response.send_message(
                "⚠️ Lệnh này chỉ hoạt động trong server Discord.", ephemeral=True
            )
            return

        try:
            response = requests.get(url, params={
                "discord_id": discord_id,
                "guild_id": guild_id
            })
            data = response.json()

            embed = discord.Embed(
                title=f"🏅 Bảng Xếp Hạng Server: {interaction.guild.name}",
                color=discord.Color.gold()
            )

            for i, player in enumerate(data["top10"], start=1):
                embed.add_field(
                    name=f"#{i} {player['username']}",
                    value=f"🏆 {player['score']} điểm",
                    inline=False
                )

            user_rank = data.get("user_rank")
            user_score = data.get("user_score")

            if user_rank is not None and user_score is not None:
                embed.set_footer(
                    text=f"📊 {interaction.user.name}, bạn đang xếp hạng #{user_rank} với {user_score} điểm trong server."
                )
            else:
                embed.set_footer(
                    text="🤔 Bạn chưa từng chơi hoặc chưa đồng bộ điểm với server này. Dùng lệnh /play để bắt đầu hoặc /sync để đồng bộ."
                )

            await interaction.response.send_message(embed=embed)

        except Exception as e:
            print(f"Lỗi khi gọi API local-rank: {e}")
            await interaction.response.send_message("⚠️ Có lỗi xảy ra khi lấy bảng xếp hạng server.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(LocalRank(bot))

