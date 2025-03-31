import discord
from discord import app_commands
from discord.ext import commands
from ..db import save_guild_channel
from bot.config import ADMIN_OVERRIDE_ID

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="setchannel", description="Đặt kênh hiện tại để bot hoạt động")
    async def set_channel(self, interaction: discord.Interaction):
        # Kiểm tra quyền admin
        if not interaction.user.guild_permissions.administrator and interaction.user.id != ADMIN_OVERRIDE_ID:
            await interaction.response.send_message(
                "❌ Bạn không có quyền quản trị.", ephemeral=True
            )
            return

        guild_id = interaction.guild.id
        channel_id = interaction.channel.id

        # Lưu vào DB
        save_guild_channel(guild_id, channel_id)
        print(f"✅ Đã set kênh {channel_id} cho guild {guild_id}.")

        await interaction.response.send_message(
            f"✅ {interaction.user.mention} đã đặt kênh này làm nơi bot hoạt động."
        )

async def setup(bot):
    await bot.add_cog(Admin(bot))
