import discord
from discord import app_commands
from discord.ext import commands
import requests
from ..utils.channel_check import is_channel_allowed
from bot.config import BACKEND_HOST

BACKEND_URL = f"{BACKEND_HOST}/api/global-rank-season"

class GlobalRankSeason(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="globalrankseason", description="Xem bảng xếp hạng toàn cầu của các mùa trước")
    @app_commands.describe(season="Nhập số mùa bạn muốn xem")
    async def global_rank_season(self, interaction: discord.Interaction, season: int = None):
        if not await is_channel_allowed(interaction):
            await interaction.response.send_message(
                "⚠️ Bot không được phép hoạt động ở kênh này. Hãy dùng lệnh `/setchannel` để thiết lập.",
                ephemeral=True
            )
            return

        if season is None:
            await interaction.response.send_message("❗ Hãy nhập mùa bạn muốn xem, ví dụ: `/globalrankseason season: 1`", ephemeral=True)
            return

        try:
            response = requests.get(BACKEND_URL, json={ "season": season })
            if response.status_code == 404:
                await interaction.response.send_message("❌ Mùa này không tồn tại.", ephemeral=True)
                return

            data = response.json()

            if data.get("is_current_season"):
                await interaction.response.send_message("🔁 Đây là mùa hiện tại. Vui lòng dùng lệnh `/globalrank` để xem", ephemeral=True)
                return

            top10 = data.get("top10", [])
            embed = discord.Embed(
                title=f"🌍 Xếp Hạng Toàn Cầu - Mùa {season}",
                description="Top 10 người chơi trên toàn thế giới",
                color=discord.Color.green()
            )

            if not top10:
                embed.add_field(name="Không có dữ liệu", value="Không có ai đạt thành tích trong mùa này.", inline=False)
            else:
                for i, player in enumerate(top10, start=1):
                    embed.add_field(
                        name=f"#{i} {player['username']}",
                        value=f"🏆 {player['score']} điểm",
                        inline=False
                    )

            await interaction.response.send_message(embed=embed)

        except Exception as e:
            print(f"❌ Lỗi khi gọi API /global-rank-season: {e}")
            await interaction.response.send_message("⚠️ Có lỗi xảy ra khi lấy bảng xếp hạng.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(GlobalRankSeason(bot))
