import discord
from discord.ext import commands
import requests
from bot.config import BACKEND_HOST, ADMIN_OVERRIDE_ID

BACKEND_URL = f"{BACKEND_HOST}/api/season/reset"

class SeasonReset(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        # Bỏ qua tin nhắn từ bot
        if message.author.bot:
            return

        # Chỉ cho phép DM
        if not isinstance(message.channel, discord.DMChannel):
            return

        # Kiểm tra ID admin
        if str(message.author.id) != str(ADMIN_OVERRIDE_ID):
            await message.channel.send("❌ Bạn không có quyền sử dụng chức năng này.")
            return

        # Kiểm tra nội dung lệnh reset
        if message.content.strip().lower() == "reset season":
            try:
                response = requests.post(BACKEND_URL)
                if response.status_code == 200:
                    await message.channel.send("✅ Đã reset mùa thành công!")
                else:
                    await message.channel.send(f"⚠️ Gửi yêu cầu thất bại. Mã lỗi: {response.status_code}")
            except Exception as e:
                print(f"❌ Lỗi khi gọi API resetSeason: {e}")
                await message.channel.send("❌ Có lỗi xảy ra khi reset mùa.")
        else:
            await message.channel.send("❗ Gõ đúng lệnh `reset season` để thực hiện reset.")

async def setup(bot):
    await bot.add_cog(SeasonReset(bot))
