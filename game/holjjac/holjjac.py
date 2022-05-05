import discord
import random
from discord.ext import commands
from utils.commands import slash_command
from discord.commands import ApplicationContext, Option
import logging
from typing import List

logger = logging.getLogger(__name__)


class holjjac(commands.Cog):
    @slash_command(description="홀짝 게임을 시작합니다.")
    async def 홀짝(self, ctx: ApplicationContext):
        dice = random.randint(1, 6)
        embed = discord.Embed(
            title="홀짝 게임",
            description="1부터 6까지 나오는 주사위의 수가 짝수일지, 홀수일지 아래의 반응을 눌러 예측해보세요!",
            color=0xFFFFFF,
        )
        embed.add_field(name="> 주사위의 눈", value="?", inline=False)
        embed.add_field(name="> 선택지", value="홀수: 🔴\n짝수: 🔵", inline=True)
        interaction = await ctx.interaction.response.send_message(embed=embed)
        msg = await interaction.original_message()
        await msg.add_reaction("🔴")
        await msg.add_reaction("🔵")
        try:

            def check(reaction, user):
                return (
                    str(reaction) in ["🔴", "🔵"]
                    and user == ctx.author
                    and reaction.message.id == msg.id
                )

            reaction, user = await ctx.bot.wait_for("reaction_add", check=check)
            if (str(reaction) == "🔴" and dice % 2 == 1) or (
                str(reaction) == "🔵" and dice % 2 == 0
            ):
                embed = discord.Embed(
                    title="홀짝 게임", description="정답입니다!", color=0xFFFFFF
                )
                embed.add_field(name="> 주사위의 눈", value=f"{dice}")
                embed.add_field(name="> 당신의 선택", value=f"{str(reaction)}", inline=False)
            else:
                embed = discord.Embed(
                    title="홀짝 게임", description="틀렸습니다..", color=0xFFFFFF
                )
                embed.add_field(name="> 주사위의 눈", value=f"{dice}")
                embed.add_field(name="> 당신의 선택", value=f"{str(reaction)}", inline=False)
            await msg.edit(embed=embed)
        except Exception:
            logger.exception("Unexpected exception from holjjac")
            embed = discord.Embed(
                title="오류가 발생했어요", description="잠시 후에 다시 시도해주세요", color=0xFF0000
            )
            await msg.edit(embed=embed)


def setup(bot):
    bot.add_cog(holjjac())
