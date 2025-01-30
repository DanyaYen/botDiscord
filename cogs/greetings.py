import discord
from discord.ext import commands
from utils import create_embed

class Greetings(commands.Cog, name="Greetings"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def hello(self, ctx):
        """Says hello to the user"""
        await ctx.send(embed=create_embed(
            "Hello! 👋",
            f"Hello, {ctx.author.name}! Nice to meet you!"
        ))

    @commands.command()
    async def ping(self, ctx):
        """Check bot's latency"""
        latency = round(self.bot.latency * 1000)
        await ctx.send(embed=create_embed(
            "Pong! 🏓",
            f"Bot latency: {latency}ms"
        ))

    @commands.command()
    async def about(self, ctx):
        """Shows information about the bot"""
        await ctx.send(embed=create_embed(
            "About Bot ℹ️",
            "This is a personal assistant bot with note-taking and utility features.\n"
            f"Use {ctx.prefix}help to see available commands!"
        ))

async def setup(bot):
    await bot.add_cog(Greetings(bot))