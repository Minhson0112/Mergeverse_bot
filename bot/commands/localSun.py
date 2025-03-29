import discord
from discord import app_commands
from discord.ext import commands
import requests
from ..utils.channel_check import is_channel_allowed
from bot.config import BACKEND_HOST

BACKEND_URL = f"{BACKEND_HOST}/api/local-sun"

class LocalSun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="localsun", description="Xem top 10 người tạo Mặt Trời nhanh nhất trong server")
    async def local_sun(self, interaction: discord.Interaction):
        if not await is_channel_allowed(interaction):
            await interaction.response.send_message(
                "⚠️ Bot không được phép hoạt động ở kênh này. Hãy dùng lệnh `/setchannel` để thiết lập.",
                ephemeral=True
            )
            return

        discord_id = interaction.user.id
        guild_id = interaction.guild.id

        try:
            response = requests.get(BACKEND_URL, params={
                "discord_id": discord_id,
                "guild_id": guild_id
            })
            data = response.json()

            embed = discord.Embed(
                title=f"🌞 Top 10 Tạo Mặt Trời Nhanh Nhất ({interaction.guild.name})",
                description="Dựa trên thời gian hoàn thành tạo ra Mặt Trời",
                color=discord.Color.orange()
            )

            top10 = data.get("top10", [])
            if not top10:
                embed.add_field(name="Không có dữ liệu", value="Chưa ai tạo ra Mặt Trời trong server này!", inline=False)
            else:
                for i, player in enumerate(top10, start=1):
                    total_sec = player["sun_time"] // 1000
                    minutes = total_sec // 60
                    seconds = total_sec % 60
                    embed.add_field(
                        name=f"#{i} {player['username']}",
                        value=f"⏱️ {minutes} phút {seconds} giây",
                        inline=False
                    )

            user_rank = data.get("user_rank")
            user_time = data.get("user_time")

            if user_rank is not None and user_time is not None:
                total_sec = user_time // 1000
                minutes = total_sec // 60
                seconds = total_sec % 60
                embed.set_footer(
                    text=f"📊 {interaction.user.name}, bạn đang xếp hạng #{user_rank} với {minutes} phút {seconds} giây."
                )
            else:
                embed.set_footer(
                    text="🤔 Bạn chưa từng tạo ra Mặt Trời trong server này. Hãy dùng /play để bắt đầu hoặc /sync để đồng bộ!"
                )

            await interaction.response.send_message(embed=embed)

        except Exception as e:
            print(f"❌ Lỗi khi gọi API /local-sun: {e}")
            await interaction.response.send_message("⚠️ Có lỗi xảy ra khi lấy bảng xếp hạng.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(LocalSun(bot))
