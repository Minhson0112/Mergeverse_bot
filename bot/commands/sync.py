import discord
from discord import app_commands
from discord.ext import commands
import requests
from ..utils.channel_check import is_channel_allowed
from bot.config import BACKEND_HOST

url = f"{BACKEND_HOST}/api/sync"

class SyncCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="sync", description="Đồng bộ điểm của bạn 1 lần duy nhất với server hiện tại")
    async def sync(self, interaction: discord.Interaction):
        if not await is_channel_allowed(interaction):
            await interaction.response.send_message(
                "⚠️ Bot không được phép hoạt động ở kênh này. Hãy dùng lệnh `/setchannel` để thiết lập.",
                ephemeral=True
            )
            return

        discord_id = interaction.user.id
        guild_id = interaction.guild.id

        try:
            response = requests.post(url, json={
                "discord_id": discord_id,
                "guild_id": guild_id
            })

            if response.status_code == 200:
                await interaction.response.send_message("✅ Đã đồng bộ điểm với server này!", ephemeral=True)
            else:
                await interaction.response.send_message(
                    "❌ Đã xảy ra lỗi khi đồng bộ. Vui lòng thử lại sau.", ephemeral=True
                )
        except Exception as e:
            print(f"Lỗi khi gỏi API sync: {e}")
            await interaction.response.send_message(
                "⚠️ Lỗi kết nối tới server.", ephemeral=True
            )

async def setup(bot):
    await bot.add_cog(SyncCommand(bot))
