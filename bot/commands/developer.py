import discord
from discord import app_commands
from discord.ext import commands
from ..utils.channel_check import is_channel_allowed

class DeveloperInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="developer", description="Thông tin liên hệ với nhà phát triển để báo cáo lỗi")
    async def developer(self, interaction: discord.Interaction):
        if not await is_channel_allowed(interaction):
            await interaction.response.send_message(
                "⚠️ Bot không được phép hoạt động ở kênh này. Hãy dùng lệnh `/setchannel` để thiết lập.",
                ephemeral=True
            )
            return

        embed = discord.Embed(
            title="👨‍💻 Thông tin Nhà phát triển",
            description="Nếu bạn gặp lỗi hoặc có góp ý, hãy liên hệ qua link dưới đây:",
            color=discord.Color.purple()
        )
        embed.add_field(
            name="📩 Liên hệ Facebook",
            value="[Developer](https://www.facebook.com/son.kakashi01/)",
            inline=False
        )
        embed.set_footer(text="Cảm ơn bạn đã sử dụng bot!")

        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(DeveloperInfo(bot))
