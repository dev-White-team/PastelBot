import discord
import random
from discord.ext import commands
from utils.commands import slash_command
from discord.commands import ApplicationContext, Option
import logging
from typing import List

logger = logging.getLogger(__name__)


class rsp(commands.Cog):
    @slash_command(description="봇과 가위바위보 게임을 합니다.")
    async def 가위바위보(
        self,
        ctx: ApplicationContext,
        user: Option(str, "낼 것을 선택하세요", choices=["가위", "바위", "보"]),
    ):
        rsp_table = ["가위", "바위", "보"]
        if user not in rsp_table:
            embed = discord.Embed(
                title="PastelBot 오류", description="가위바위보 기능", color=0xFF0000
            )
            embed.add_field(
                name="오류 내용:", value="`가위, 바위, 보` 중에 하나를 입력해주세요.", inline=False
            )
            await ctx.respond(embed=embed)
        else:
            bot = random.choice(rsp_table)
            result = rsp_table.index(user) - rsp_table.index(bot)
            if result == 0:
                forsend = f"{user} vs {bot}\n비겼네요!"
            elif result == 1 or result == -2:
                forsend = f"{user} vs {bot}\n{ctx.author.display_name}님이 이겼어요!"
            else:
                forsend = f"{user} vs {bot}\n봇이 이겼습니다!"
            embed = discord.Embed(
                title="가위바위보",
                description=f"{ctx.author.display_name} vs 봇",
                color=0xFFFFFF,
            )
            embed.add_field(name="**결과:**", value=f"{forsend}", inline=False)
            await ctx.respond(embed=embed)


def setup(bot):
    bot.add_cog(rsp())
