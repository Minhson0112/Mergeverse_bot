import discord
from discord import app_commands
from discord.ext import commands
from ..utils.channel_check import is_channel_allowed

class HelpCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="help", description="Hiển thị danh sách các lệnh có trong bot")
    async def help_command(self, interaction: discord.Interaction):
        if not await is_channel_allowed(interaction):
            await interaction.response.send_message(
                "⚠️ Bot không được phép hoạt động ở kênh này. Hãy dùng lệnh `/setchannel` để thiết lập.",
                ephemeral=True
            )
            return

        embed = discord.Embed(
            title="📖 Danh sách lệnh bot",
            description="Dưới đây là các lệnh bạn có thể sử dụng với bot:",
            color=discord.Color.blue()
        )

        embed.add_field(name="/play", value="🎮 Bắt đầu chơi game", inline=False)
        embed.add_field(name="/localrank", value="📊 Xem bảng xếp hạng hiện tại của server này", inline=False)
        embed.add_field(name="/globalrank", value="🌍 Xem bảng xếp hạng toàn cầu", inline=False)
        embed.add_field(name="/localsun", value="🌞 Xem thời gian tạo Mặt Trời nhanh nhất trong server", inline=False)
        embed.add_field(name="/globalsun", value="🌞 Xem thời gian tạo Mặt Trời nhanh nhất toàn cầu", inline=False)
        embed.add_field(name="/localrankseason season:<số>", value="🕒 Xem lịch sử xếp hạng theo mùa của server", inline=False)
        embed.add_field(name="/globalrankseason season:<số>", value="🕒 Xem lịch sử xếp hạng theo mùa toàn cầu", inline=False)
        embed.add_field(name="/sync", value="🔄 Đồng bộ điểm của bạn sang server mới", inline=False)
        embed.add_field(name="/setchannel", value="🔧 Đặt kênh hiện tại thành kênh hoạt động của bot *(cần quyền QTV)*", inline=False)
        embed.add_field(name="/developer", value="👨‍💻 Liên hệ với nhà phát triển (báo lỗi/góp ý)", inline=False)
        embed.add_field(name="/help", value="🆘 Hiển thị danh sách các lệnh", inline=False)
        embed.add_field(name="/seasonreset", value="⚠️ Reset mùa giải mới *(chỉ dành cho developer)*", inline=False)

        embed.set_footer(text="Cảm ơn bạn đã sử dụng bot ❤️")

        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(HelpCommand(bot))
