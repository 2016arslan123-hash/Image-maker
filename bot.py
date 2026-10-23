
import os
import io
import base64
import asyncio
import discord
from discord import app_commands
from openai import OpenAI

ai = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

class ImageBot(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        await self.tree.sync()

bot = ImageBot()

@bot.tree.command(name="image", description="Generate an AI image")
@app_commands.describe(prompt="Describe the image you want")
async def image(interaction: discord.Interaction, prompt: str):
    await interaction.response.defer(thinking=True)
    try:
        result = await asyncio.to_thread(
            ai.images.generate,
            model="gpt-image-1",
            prompt=prompt,
            size="1024x1024",
            n=1
        )
        data = base64.b64decode(result.data[0].b64_json)
        image_file = discord.File(io.BytesIO(data), filename="image.png")
        await interaction.followup.send(file=image_file)
    except Exception as error:
        print(f"Image error: {error}")
        await interaction.followup.send(
            "Image generation failed. Check API billing and model access."
        )

@bot.event
async def on_ready():
    print(f"Bot online: {bot.user}")

bot.run(os.environ["DISCORD_TOKEN"])
