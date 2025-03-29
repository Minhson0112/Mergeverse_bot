import discord
from discord import app_commands
from discord.ext import commands
import requests
from bot.config import BACKEND_HOST
from ..utils.channel_check import is_channel_allowed

BACKEND_URL = f"{BACKEND_HOST}/api/global-sun-rank"

class GlobalSun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="globalsun", description="Top 10 người tạo ra Mặt Trời nhanh nhất toàn cầu")
    async def global_sun(self, interaction: discord.Interaction):
        if not await is_channel_allowed(interaction):
            await interaction.response.send_message(
                "⚠️ Bot không được phép hoạt động ở kênh này. Hãy dùng lệnh `/setchannel` để thiết lập.",
                ephemeral=True
            )
            return
        
        discord_id = interaction.user.id

        try:
            response = requests.get(BACKEND_URL, params={"discord_id": discord_id})
            data = response.json()

            embed = discord.Embed(
                title="🌞 Top 10 Người Tạo Mặt Trời Nhanh Nhất",
                description="Dựa trên mốc thời gian tạo ra Mặt Trời (càng nhanh càng tốt)",
                color=discord.Color.orange()
            )

            # Danh sách top 10
            top10 = data.get("top10", [])
            if not top10:
                embed.add_field(name="Không có dữ liệu", value="Chưa ai tạo ra Mặt Trời!", inline=False)
            else:
                for i, player in enumerate(top10, start=1):
                    total_seconds = player["sun_time"] // 1000
                    minutes = total_seconds // 60
                    seconds = total_seconds % 60
                    embed.add_field(
                        name=f"#{i} {player['username']}",
                        value=f"☀️ {minutes} phút {seconds} giây",
                        inline=False
                    )

            # Xếp hạng người dùng
            user_rank = data.get("user_rank")
            user_time = data.get("user_time")

            if user_rank is not None and user_time is not None:
                total_seconds = user_time // 1000
                minutes = total_seconds // 60
                seconds = total_seconds % 60
                embed.set_footer(
                    text=f"📊 {interaction.user.name}, bạn đang xếp hạng #{user_rank} với {minutes} phút {seconds} giây."
                )
            else:
                embed.set_footer(text="🤔 Bạn chưa từng tạo ra Mặt Trời. Hãy chơi game bằng lệnh /play!")

            await interaction.response.send_message(embed=embed)

        except Exception as e:
            print(f"Lỗi khi gọi API /global-sun-rank: {e}")
            await interaction.response.send_message("⚠️ Có lỗi xảy ra khi lấy bảng xếp hạng.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(GlobalSun(bot))
