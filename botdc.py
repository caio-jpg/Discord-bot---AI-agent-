import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
from google import genai
from google.genai import types

load_dotenv()
discord_bot_token = os.getenv("DISCORD_BOT_TOKEN")
gemini_api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=gemini_api_key)

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

def ask_gpt(conteudo):
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=conteudo,
            config=types.GenerateContentConfig(
                safety_settings=[
                    types.SafetySetting(
                        category="HARM_CATEGORY_HARASSMENT",
                        threshold="BLOCK_NONE"
                    ),
                    types.SafetySetting(
                        category="HARM_CATEGORY_HATE_SPEECH",
                        threshold="BLOCK_NONE"
                    ),
                    types.SafetySetting(
                        category="HARM_CATEGORY_SEXUALLY_EXPLICIT",
                        threshold="BLOCK_NONE"
                    ),
                    types.SafetySetting(
                        category="HARM_CATEGORY_DANGEROUS_CONTENT",
                        threshold="BLOCK_NONE"
                    )
                ]
            )
        )
        return response.text
    except Exception as e:
        return f"Erro na API: {e}"

@bot.event
async def on_ready():
    print(f"O {bot.user.name} está online!")

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    
    if bot.user.mentioned_in(message):
       
        async with message.channel.typing():
            prompt = message.clean_content
            resposta = ask_gpt(prompt)
            
            if len(resposta) > 2000:
                await message.reply(resposta[:2000])
            else:
                await message.reply(resposta)
        
    await bot.process_commands(message)

bot.run(discord_bot_token)