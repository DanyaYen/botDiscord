import discord
from discord.ext import commands
import json
from datetime import datetime
from utils import create_embed, load_json, save_json
from config import NOTE_FILE, REMINDER_FILE, OWNER_ID

class Personal(commands.Cog, name="Personal Commands"):
    def __init__(self, bot):
        self.bot = bot
        self.notes = load_json(NOTE_FILE)
        self.reminders = load_json(REMINDER_FILE)

    async def get_user_safe(self, ctx, user_input=None):
        """Safely get user from mention, id, or name"""
        if user_input is None:
            return ctx.author
        
        try:
            # Check for user mention
            if ctx.message.mentions:
                return ctx.message.mentions[0]
            
            # Check for user ID
            if user_input.isdigit():
                try:
                    user = await self.bot.fetch_user(int(user_input))
                    return user
                except discord.NotFound:
                    return None
            
            # Search by name
            if ctx.guild:
                member = discord.utils.get(ctx.guild.members, name=user_input)
                if member:
                    return member
            
            return None
        except Exception as e:
            print(f"Debug: Error in get_user_safe: {e}")
            return None

    @commands.command()
    async def userinfo(self, ctx, *, user_input=None):
        try:
            user = await self.get_user_safe(ctx, user_input)

            if user is None:
                await ctx.send(embed=create_embed(
                    "Error",
                    "User not found or invalid input.",
                    discord.Color.red()
                ))
                return

            embed = discord.Embed(title="User Info", color=discord.Color.blue())
            embed.add_field(name="Name", value=str(user), inline=True)
            embed.add_field(name="ID", value=str(user.id), inline=True)
            embed.add_field(name="Created at", value=user.created_at.strftime("%Y-%m-%d %H:%M:%S"), inline=True)

            if isinstance(user, discord.Member):
                embed.add_field(name="Display Name", value=user.display_name, inline=True)
                if user.joined_at:
                    embed.add_field(name="Joined Server", value=user.joined_at.strftime("%Y-%m-%d %H:%M:%S"), inline=True)
                embed.add_field(name="Top Role", value=user.top_role.name, inline=True)
                
                embed.add_field(name="Status", value=str(user.status).title(), inline=True)
                
                if user.activity:
                    activity = f"{user.activity.type.name.title()} {user.activity.name}"
                    embed.add_field(name="Activity", value=activity, inline=True)
            
            if user.avatar:
                embed.set_thumbnail(url=user.avatar.url)
            
            await ctx.send(embed=embed)
            
        except Exception as e:
            await ctx.send(embed=create_embed(
                "Error",
                f"An error occurred: {str(e)}",
                discord.Color.red()
            ))

    @commands.group(invoke_without_command=True)
    async def note(self, ctx):
        """Note management commands"""
        await ctx.send(embed=create_embed(
            "Notes Help",
            "Available commands:\n"
            "!note add <name> | <content>  (use | to separate name and content)\n"
            "!note list\n"
            "!note show <name>\n"
            "!note delete <name>"
        ))

    @note.command(name="add")
    async def add_note(self, ctx, *, content: str):
        """Adds a new note. Format: !note add name | content"""
        try:
            name, note_content = content.split('|', 1)
            name = name.strip()
            note_content = note_content.strip()
            
            if not name or not note_content:
                raise ValueError
                
            self.notes[name] = {
                'content': note_content,
                'created_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            save_json(NOTE_FILE, self.notes)
            await ctx.send(embed=create_embed(
                "Success", 
                f"Note '{name}' has been saved with content:\n{note_content}"
            ))
        except ValueError:
            await ctx.send(embed=create_embed(
                "Error",
                "Incorrect format! Use: !note add name | your note content",
                discord.Color.red()
            ))

    @note.command(name="list")
    async def list_notes(self, ctx):
        """Shows list of all notes"""
        if not self.notes:
            await ctx.send(embed=create_embed("Notes", "You don't have any notes"))
            return
        
        notes_list = "\n".join([f"📝 {name} ({note['created_at']})" 
                            for name, note in self.notes.items()])
        await ctx.send(embed=create_embed("Your Notes", notes_list))

    @note.command(name="show")
    async def show_note(self, ctx, name: str):
        """Shows note content"""
        if name not in self.notes:
            await ctx.send(embed=create_embed(
                "Error", 
                "Note not found",
                discord.Color.red()
            ))
            return
        
        note = self.notes[name]
        await ctx.send(embed=create_embed(
            f"Note: {name}",
            note['content']
        ))

    @note.command(name="delete")
    async def delete_note(self, ctx, name: str):
        """Deletes a note"""
        if name not in self.notes:
            await ctx.send(embed=create_embed(
                "Error",
                "Note not found",
                discord.Color.red()
            ))
            return
        
        del self.notes[name]
        save_json(NOTE_FILE, self.notes)
        await ctx.send(embed=create_embed(
            "Success",
            f"Note '{name}' has been deleted"
        ))

    @commands.command()
    async def search(self, ctx, *, query: str):
        """Search through notes"""
        results = []
        for name, note in self.notes.items():
            if query.lower() in name.lower() or query.lower() in note['content'].lower():
                results.append(f"📌 {name}: {note['content'][:100]}...")
        
        if results:
            await ctx.send(embed=create_embed(
                f"Search results for '{query}'",
                "\n\n".join(results)
            ))
        else:
            await ctx.send(embed=create_embed("Search", "No results found"))

    @commands.command()
    async def calc(self, ctx, *, expression: str):
        """Simple calculator"""
        try:
            result = eval(expression)
            await ctx.send(embed=create_embed(
                "Calculator",
                f"{expression} = {result}"
            ))
        except Exception as e:
            await ctx.send(embed=create_embed(
                "Error",
                f"Failed to evaluate expression: {str(e)}",
                discord.Color.red()
            ))

    @commands.command()
    async def clear(self, ctx, amount: int):
        """Clear specified number of messages"""
        await ctx.channel.purge(limit=amount + 1)
        msg = await ctx.send(embed=create_embed(
            "Clear Messages",
            f"Deleted {amount} messages!"
        ))
        await msg.delete(delay=5)

async def setup(bot):
    await bot.add_cog(Personal(bot))

async def cog_check(self, ctx):
    return ctx.author.id == OWNER_ID
