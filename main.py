import discord
from discord.ext import commands
from config import TOKEN, PREFIX
import os
import asyncio
from utils import create_embed

class Bot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        
        super().__init__(
            command_prefix=PREFIX,
            intents=intents,
            help_command=None
        )

    async def setup_hook(self):
        """Setup cogs on startup"""
        try:
            # Load all cogs from the cogs folder
            for filename in os.listdir("cogs"):
                if filename.endswith(".py"):
                    await self.load_extension(f"cogs.{filename[:-3]}")
            print("✅ Cogs loaded successfully")
            
            # Register the help command after loading cogs
            self.remove_command('help')  # Remove the old help command if it exists
            
            @self.command(name='help')
            async def help(ctx, command_name=None):
                """Shows help message"""
                if command_name is None:
                    embed = create_embed(
                        "Commands List",
                        f"Use {PREFIX}help <command> for more info about a command",
                        discord.Color.purple()
                    )

                    # Personal Commands
                    personal_commands = [
                        f"`{PREFIX}calc` - Simple calculator",
                        f"`{PREFIX}clear` - Clear specified number of messages",
                        f"`{PREFIX}note` - Note management commands",
                        f"`{PREFIX}search` - Search through notes",
                        f"`{PREFIX}userinfo` - Get info about a user"
                    ]
                    embed.add_field(
                        name="Personal Commands",
                        value="\n".join(personal_commands),
                        inline=False
                    )

                    # Greetings
                    greeting_commands = [
                        f"`{PREFIX}about` - Shows information about the bot",
                        f"`{PREFIX}hello` - Says hello to the user",
                        f"`{PREFIX}ping` - Check bot's latency"
                    ]
                    embed.add_field(
                        name="Greetings",
                        value="\n".join(greeting_commands),
                        inline=False
                    )

                    # Main Commands
                    main_commands = [
                        f"`{PREFIX}help` - Shows this message"
                    ]
                    embed.add_field(
                        name="Main Commands",
                        value="\n".join(main_commands),
                        inline=False
                    )

                else:
                    cmd = self.get_command(command_name)
                    if cmd is None:
                        embed = create_embed(
                            "Error",
                            f"Command '{command_name}' not found.",
                            discord.Color.red()
                        )
                    else:
                        embed = create_embed(
                            f"Help: {cmd.name}",
                            cmd.help or "No description available"
                        )

                await ctx.send(embed=embed)
            
        except Exception as e:
            print(f"❌ Error loading cogs: {e}")

    async def on_ready(self):
        """Actions when bot is ready"""
        print(f"🤖 Bot {self.user} is ready!")
        print(f"🎮 Current prefix: {PREFIX}")
        print(f"💡 Use {PREFIX}help to see available commands")
        
        await self.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.listening,
                name=f"{PREFIX}help"
            )
        )

async def main():
    async with bot:
        try:
            await bot.start(TOKEN)
        except KeyboardInterrupt:
            print("Bot interrupted by user.")
        except Exception as e:
            print(f"Error starting the bot: {str(e)}")

if __name__ == "__main__":
    bot = Bot()
    asyncio.run(main())