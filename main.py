import discord
from discord.ext import commands
import dotenv
import time
import logging
import utils.logging
import os

dotenv.load_dotenv()
bot = commands.Bot(command_prefix="-", help_command=None)
utils.logging.setup_logging()
logger = logging.getLogger("main")
bot.start_time = time.time()


@bot.event
async def on_ready():
    guild_count = len(bot.guilds)

    logger.info(f"Logged in as {bot.user.name}")
    logger.info(f"Be used in {guild_count} guilds.")

    await bot.change_presence(
        status=discord.Status.online,
        activity=discord.Game(f"개발중 - {guild_count}개의 서버에서 작동 중"),
    )

    log_channel = await bot.fetch_channel(951047371645669376)
    await log_channel.send(f"<t:{int(bot.start_time)}:T>({bot.start_time})")

bot.run(os.getenv("BOT_TOKEN"))
