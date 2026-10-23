
import discord
from discord import app_commands
import os

TOKEN = os.environ.get("DISCORD_TOKEN")

class ImageBot(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        await self.tree.sync()

bot = ImageBot()

@bot.tree.command(name="image", description="Generate an AI image from a prompt")
@app_commands.describe(prompt="Describe the image you want")
async def image(interaction: discord.Interaction, prompt: str):
    await interaction.response.send_message(
        f"Your image prompt: {prompt}\n"
        "Image generation will be connected in the next step."
    )

@bot.event
async def on_ready():
    print(f"Bot online: {bot.user}")

if not TOKEN:
    raise RuntimeError("Missing DISCORD_TOKEN environment variable")

bot.run(TOKEN)
