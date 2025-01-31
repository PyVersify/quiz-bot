import discord
from discord.ext import commands
from src.quiz import QuizSelectView

intents = discord.Intents.default()
intents.message_content = True

quiz_bot = commands.Bot(command_prefix='!', intents=intents)

@quiz_bot.command()
async def quiz(ctx) -> None:
    view = QuizSelectView()
    await ctx.send('Select a quiz:', view=view)
