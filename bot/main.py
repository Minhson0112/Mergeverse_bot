import discord
from discord.ext import commands
from bot.config import DISCORD_TOKEN

intents = discord.Intents.default()
intents.message_content = True  # Cho phép đọc nội dung tin nhắn nếu cần

bot = commands.Bot(command_prefix="/", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Bot is ready as {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"🔧 Synced {len(synced)} slash commands.")
    except Exception as e:
        print(f"❌ Failed to sync commands: {e}")

async def main():
    # Load các module slash command
    await bot.load_extension("bot.commands.play")
    await bot.load_extension("bot.commands.setChannel")
    await bot.load_extension("bot.commands.globalRank")
    await bot.load_extension("bot.commands.localRank")
    await bot.load_extension("bot.commands.globalSun")
    await bot.load_extension("bot.commands.localSun")
    await bot.load_extension("bot.commands.sync")
    await bot.load_extension("bot.commands.developer")
    await bot.load_extension("bot.commands.seasonReset")
    await bot.load_extension("bot.commands.localRankSeason")
    await bot.load_extension("bot.commands.globalRankSeason")
    await bot.load_extension("bot.commands.help")
    await bot.start(DISCORD_TOKEN)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
