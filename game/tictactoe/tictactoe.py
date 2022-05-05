import discord
import random
from discord.ext import commands
from utils.commands import slash_command
from discord.commands import ApplicationContext, Option
import logging
from typing import List

logger = logging.getLogger(__name__)


class tictactoe(commands.Cog):
    @slash_command(description="틱택토(삼목) 게임을 진행합니다.")
    async def 틱택토(
        self,
        ctx: ApplicationContext,
        rival: Option(discord.User, description="같이 게임을 할 유저를 선택하세요"),
    ):
        if rival.bot:
            embed = discord.Embed(
                title="PastelBot 오류", description="틱택토 기능", color=0xFF0000
            )
            embed.add_field(name="오류 내용:", value="봇과는 대결할 수 없습니다.", inline=False)
            await ctx.respond(embed=embed)
        else:
            await ctx.respond(
                f"틱택토(삼목) 게임을 시작합니다. {ctx.user.mention}(X) vs {rival.mention}(O) - X부터 시작합니다.",
                view=TicTacToe(ctx.user.id, rival.id),
            )


class TicTacToeButton(discord.ui.Button["TicTacToe"]):
    def __init__(self, x: int, y: int):
        super().__init__(style=discord.ButtonStyle.secondary, label="\u200b", row=y)
        self.x = x
        self.y = y

    styles_by_player = (discord.ButtonStyle.danger, discord.ButtonStyle.success)
    labels_by_player = ("X", "O")

    async def callback(self, interaction: discord.Interaction):
        assert self.view is not None
        view: TicTacToe = self.view
        cp = view.current_player

        assert view.board[self.y][self.x] == -1
        if interaction.user.id != view.player_ids[cp]:
            return

        view.board[self.y][self.x] = cp

        self.style = self.styles_by_player[cp]
        self.label = self.labels_by_player[cp]
        self.disabled = True

        view.current_player = cp = 1 - cp
        content = f"<@{view.player_ids[cp]}>({self.labels_by_player[cp]})의 차례입니다!"

        logger.debug("Board %s", str(view.board))

        winner = view.check_board_winner()
        if winner is not None:
            if winner == -1:
                content = "비겼습니다."
            else:
                content = (
                    f"<@{view.player_ids[winner]}>({self.labels_by_player[winner]}) 승리!"
                )

            for child in view.children:
                child.disabled = True
            view.stop()

        await interaction.response.edit_message(content=content, view=view)


class TicTacToe(discord.ui.View):
    children: List[TicTacToeButton]

    def __init__(self, player_id: discord.Member, rival_id: discord.Member):
        super().__init__()

        self.player_ids = (player_id, rival_id)

        self.current_player = 0
        self.board = [
            [-1, -1, -1],
            [-1, -1, -1],
            [-1, -1, -1],
        ]

        logger.debug("Board %s", str(self.board))

        for x in range(3):
            for y in range(3):
                self.add_item(TicTacToeButton(x, y))

    def check_board_winner(self):
        for line in range(3):
            if self.board[line][0] == self.board[line][1] == self.board[line][2] != -1:
                logger.debug("[Game Set] Horizontal(line %d)", line)
                return self.board[line][0]

        for line in range(3):
            if self.board[0][line] == self.board[1][line] == self.board[2][line] != -1:
                logger.debug("[Game Set] Vertical(line %d)", line)
                return self.board[0][line]

        if self.board[0][2] == self.board[1][1] == self.board[2][0] != -1:
            logger.debug("[Game Set] Diagonal ↙")
            return self.board[0][2]

        if self.board[0][0] == self.board[1][1] == self.board[2][2] != -1:
            logger.debug("[Game Set] Diagonal ↘")
            return self.board[0][0]

        if all(i != -1 for row in self.board for i in row):
            logger.debug("[Game Set] Draw")
            return -1

        return None


def setup(bot):
    bot.add_cog(tictactoe())
