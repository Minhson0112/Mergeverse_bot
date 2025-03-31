import discord
from discord import app_commands
from discord.ext import commands
from ..utils.channel_check import is_channel_allowed
from bot.config import BACKEND_HOST

class PlayCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="play", description="Gửi link chơi game qua tin nhắn riêng")
    async def play(self, interaction: discord.Interaction):
        if not await is_channel_allowed(interaction):
            await interaction.response.send_message(
                "⚠️ Bot không được phép hoạt động ở kênh này. Hãy dùng lệnh `/setchannel` để thiết lập.",
                ephemeral=True
            )
            return

        user = interaction.user
        guild_id = interaction.guild.id  #Thêm guild_id
        game_url = (
            f"{BACKEND_HOST}/start-game"
            f"?discord_id={user.id}"
            f"&username={user.name}"
            f"&guild_id={guild_id}"
        )

        try:
            await user.send(f"🎮 Ấn để bắt đầu chơi: {game_url}")
            await interaction.response.send_message(
                f"📩 {user.mention} tôi đã gửi link chơi game cho bạn qua tin nhắn riêng!")
        except:
            await interaction.response.send_message(
                "❌ Tôi không thể gửi tin nhắn riêng cho bạn. Vui lòng kiểm tra cài đặt quyền riêng tư.",
                ephemeral=True
            )

async def setup(bot):
    await bot.add_cog(PlayCommand(bot))
