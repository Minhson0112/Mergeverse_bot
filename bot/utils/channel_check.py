from bot.db import get_allowed_channel
import discord

async def is_channel_allowed(interaction: discord.Interaction) -> bool:
    """
    Kiểm tra xem bot có được phép hoạt động trong kênh gửi lệnh hay không
    """
    if not interaction.guild:
        return False  # Chỉ hoạt động trong server

    allowed_channel_id = get_allowed_channel(interaction.guild.id)
    return allowed_channel_id is not None and allowed_channel_id == interaction.channel.id
