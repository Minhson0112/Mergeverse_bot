import discord
from discord import app_commands
from discord.ext import commands
import requests
from ..utils.channel_check import is_channel_allowed
from bot.config import BACKEND_HOST

BACKEND_URL = f"{BACKEND_HOST}/api/local-rank-season"

class LocalRankSeason(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="localrankseason", description="Xem bảng xếp hạng theo mùa trong server này")
    @app_commands.describe(season="Nhập số mùa bạn muốn xem")
    async def local_rank_season(self, interaction: discord.Interaction, season: int = None):
        if not await is_channel_allowed(interaction):
            await interaction.response.send_message(
                "⚠️ Bot không được phép hoạt động ở kênh này. Hãy dùng lệnh `/setchannel` để thiết lập.",
                ephemeral=True
            )
            return

        if season is None:
            await interaction.response.send_message("❗ Hãy nhập mùa bạn muốn xem, ví dụ: `/localrankseason season: 1`", ephemeral=True)
            return

        guild_id = interaction.guild.id

        try:
            response = requests.get(BACKEND_URL, params={
                "guild_id": guild_id,
                "season": season
            })

            if response.status_code == 404:
                # Phân biệt giữa "season không tồn tại" và "server không có dữ liệu"
                if data.get("not_found"):
                    await interaction.response.send_message("❌ Server này chưa có dữ liệu cho mùa này.")
                else:
                    await interaction.response.send_message("❌ Mùa này không tồn tại.")
                return

            data = response.json()

            if data.get("is_current_season"):
                await interaction.response.send_message("🔁 Đây là mùa hiện tại. Vui lòng dùng lệnh `/localrank` để xem.")
                return

            top10 = data.get("top10", [])
            embed = discord.Embed(
                title=f"🏆 Xếp Hạng Mùa {season} ({interaction.guild.name})",
                description=f"Top 10 người chơi trong mùa {season}",
                color=discord.Color.gold()
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
            print(f"❌ Lỗi khi gọi API local-rank mùa {season}: {e}")
            await interaction.response.send_message("⚠️ Có lỗi xảy ra khi truy vấn dữ liệu mùa.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(LocalRankSeason(bot))
