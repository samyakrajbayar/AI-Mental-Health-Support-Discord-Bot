import discord
from discord.ext import commands
from discord import app_commands
import anthropic
import os
from datetime import datetime
import json
import asyncio

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)
client = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

# Store user conversations (in production, use a database)
user_conversations = {}
user_mood_logs = {}

SYSTEM_PROMPT = """You are a compassionate mental health support assistant. Your role is to:
- Provide empathetic, supportive responses
- Help users work through difficult emotions
- Suggest evidence-based coping strategies
- Encourage professional help when needed
- Never diagnose or replace professional treatment
- Be warm, understanding, and non-judgmental
- Use active listening and validation techniques
- Suggest breathing exercises, mindfulness, or grounding techniques when appropriate

IMPORTANT: If someone expresses thoughts of self-harm or suicide, immediately provide crisis resources:
- National Suicide Prevention Lifeline: 988 (US)
- Crisis Text Line: Text HOME to 741741
- International Association for Suicide Prevention: https://www.iasp.info/resources/Crisis_Centres/"""

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    try:
        synced = await bot.tree.sync()
        print(f'Synced {len(synced)} command(s)')
    except Exception as e:
        print(f'Error syncing commands: {e}')

@bot.tree.command(name="talk", description="Have a supportive conversation about how you're feeling")
@app_commands.describe(message="What's on your mind?")
async def talk(interaction: discord.Interaction, message: str):
    await interaction.response.defer(ephemeral=True)
    
    user_id = str(interaction.user.id)
    
    # Initialize conversation history
    if user_id not in user_conversations:
        user_conversations[user_id] = []
    
    # Add user message to history
    user_conversations[user_id].append({
        "role": "user",
        "content": message
    })
    
    # Keep only last 10 messages to manage context
    if len(user_conversations[user_id]) > 10:
        user_conversations[user_id] = user_conversations[user_id][-10:]
    
    try:
        # Call Claude API
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1024,
            system=SYSTEM_PROMPT,
            messages=user_conversations[user_id]
        )
        
        assistant_message = response.content[0].text
        
        # Add assistant response to history
        user_conversations[user_id].append({
            "role": "assistant",
            "content": assistant_message
        })
        
        # Create embed for response
        embed = discord.Embed(
            title="💙 Mental Health Support",
            description=assistant_message,
            color=discord.Color.blue(),
            timestamp=datetime.now()
        )
        embed.set_footer(text="Remember: This is not a replacement for professional help")
        
        await interaction.followup.send(embed=embed, ephemeral=True)
        
    except Exception as e:
        await interaction.followup.send(
            f"I'm sorry, I encountered an error. Please try again later.\nError: {str(e)}", 
            ephemeral=True
        )

@bot.tree.command(name="mood", description="Log your current mood")
@app_commands.describe(
    mood="How are you feeling?",
    intensity="Intensity from 1-10"
)
@app_commands.choices(mood=[
    app_commands.Choice(name="😊 Happy", value="happy"),
    app_commands.Choice(name="😔 Sad", value="sad"),
    app_commands.Choice(name="😰 Anxious", value="anxious"),
    app_commands.Choice(name="😡 Angry", value="angry"),
    app_commands.Choice(name="😐 Neutral", value="neutral"),
    app_commands.Choice(name="😫 Overwhelmed", value="overwhelmed"),
])
async def mood(interaction: discord.Interaction, mood: str, intensity: int):
    if intensity < 1 or intensity > 10:
        await interaction.response.send_message("Intensity must be between 1 and 10", ephemeral=True)
        return
    
    user_id = str(interaction.user.id)
    
    if user_id not in user_mood_logs:
        user_mood_logs[user_id] = []
    
    mood_entry = {
        "mood": mood,
        "intensity": intensity,
        "timestamp": datetime.now().isoformat()
    }
    
    user_mood_logs[user_id].append(mood_entry)
    
    mood_emoji = {
        "happy": "😊",
        "sad": "😔",
        "anxious": "😰",
        "angry": "😡",
        "neutral": "😐",
        "overwhelmed": "😫"
    }
    
    embed = discord.Embed(
        title="Mood Logged Successfully",
        description=f"Mood: {mood_emoji.get(mood, '💭')} {mood.capitalize()}\nIntensity: {intensity}/10",
        color=discord.Color.green(),
        timestamp=datetime.now()
    )
    
    await interaction.response.send_message(embed=embed, ephemeral=True)

@bot.tree.command(name="moodhistory", description="View your mood history")
async def moodhistory(interaction: discord.Interaction):
    user_id = str(interaction.user.id)
    
    if user_id not in user_mood_logs or not user_mood_logs[user_id]:
        await interaction.response.send_message("You haven't logged any moods yet! Use `/mood` to start tracking.", ephemeral=True)
        return
    
    mood_emoji = {
        "happy": "😊",
        "sad": "😔",
        "anxious": "😰",
        "angry": "😡",
        "neutral": "😐",
        "overwhelmed": "😫"
    }
    
    recent_moods = user_mood_logs[user_id][-7:]  # Last 7 entries
    
    history_text = ""
    for entry in recent_moods:
        timestamp = datetime.fromisoformat(entry['timestamp'])
        formatted_time = timestamp.strftime("%b %d, %I:%M %p")
        history_text += f"{mood_emoji.get(entry['mood'], '💭')} {entry['mood'].capitalize()} ({entry['intensity']}/10) - {formatted_time}\n"
    
    embed = discord.Embed(
        title="📊 Your Recent Mood History",
        description=history_text,
        color=discord.Color.purple(),
        timestamp=datetime.now()
    )
    embed.set_footer(text=f"Showing last {len(recent_moods)} mood logs")
    
    await interaction.response.send_message(embed=embed, ephemeral=True)

@bot.tree.command(name="breathing", description="Guided breathing exercise")
async def breathing(interaction: discord.Interaction):
    await interaction.response.send_message("Starting a 4-7-8 breathing exercise... 🧘", ephemeral=True)
    
    exercises = [
        ("Breathe in through your nose...", 4),
        ("Hold your breath...", 7),
        ("Exhale slowly through your mouth...", 8),
    ]
    
    for i in range(3):  # 3 cycles
        for instruction, duration in exercises:
            await interaction.followup.send(f"**Cycle {i+1}/3:** {instruction}", ephemeral=True)
            await asyncio.sleep(duration)
    
    embed = discord.Embed(
        title="✅ Exercise Complete",
        description="Great job! How are you feeling now?",
        color=discord.Color.green()
    )
    await interaction.followup.send(embed=embed, ephemeral=True)

@bot.tree.command(name="resources", description="Get mental health resources and crisis support")
async def resources(interaction: discord.Interaction):
    embed = discord.Embed(
        title="🆘 Mental Health Resources",
        description="If you're in crisis, please reach out to these resources:",
        color=discord.Color.red()
    )
    
    embed.add_field(
        name="🇺🇸 United States",
        value="**988 Suicide & Crisis Lifeline**: Call or text 988\n**Crisis Text Line**: Text HOME to 741741",
        inline=False
    )
    
    embed.add_field(
        name="🇬🇧 United Kingdom",
        value="**Samaritans**: 116 123\n**Shout Crisis Text Line**: Text SHOUT to 85258",
        inline=False
    )
    
    embed.add_field(
        name="🇨🇦 Canada",
        value="**Talk Suicide Canada**: 1-833-456-4566\n**Crisis Text Line**: Text TALK to 686868",
        inline=False
    )
    
    embed.add_field(
        name="🌍 International",
        value="**IASP Crisis Centers**: https://www.iasp.info/resources/Crisis_Centres/",
        inline=False
    )
    
    embed.add_field(
        name="📚 Additional Resources",
        value="**NAMI (National Alliance on Mental Illness)**: https://www.nami.org\n**Mental Health America**: https://www.mhanational.org\n**BetterHelp**: https://www.betterhelp.com",
        inline=False
    )
    
    embed.set_footer(text="You are not alone. Help is available 24/7.")
    
    await interaction.response.send_message(embed=embed, ephemeral=True)

@bot.tree.command(name="affirmation", description="Get a positive affirmation")
async def affirmation(interaction: discord.Interaction):
    affirmations = [
        "You are worthy of love and respect.",
        "Your feelings are valid, and it's okay to feel them.",
        "You are stronger than you think.",
        "Every day is a new opportunity for growth.",
        "You deserve to be happy and at peace.",
        "Your presence makes a difference in the world.",
        "It's okay to take things one step at a time.",
        "You are doing the best you can, and that's enough.",
        "Your mental health matters.",
        "You have overcome challenges before, and you can do it again.",
        "You are not defined by your struggles.",
        "It's brave to ask for help when you need it.",
        "You deserve compassion, especially from yourself.",
        "Progress, not perfection, is what matters.",
        "You are capable of amazing things."
    ]
    
    import random
    affirmation = random.choice(affirmations)
    
    embed = discord.Embed(
        title="💫 Daily Affirmation",
        description=affirmation,
        color=discord.Color.gold()
    )
    
    await interaction.response.send_message(embed=embed, ephemeral=True)

@bot.tree.command(name="clear", description="Clear your conversation history")
async def clear(interaction: discord.Interaction):
    user_id = str(interaction.user.id)
    
    if user_id in user_conversations:
        user_conversations[user_id] = []
    
    await interaction.response.send_message("✅ Your conversation history has been cleared.", ephemeral=True)

@bot.tree.command(name="help", description="Learn how to use the mental health bot")
async def help_command(interaction: discord.Interaction):
    embed = discord.Embed(
        title="🤖 Mental Health Support Bot - Help",
        description="I'm here to provide support and help you manage your mental wellbeing.",
        color=discord.Color.blue()
    )
    
    embed.add_field(
        name="/talk",
        value="Have a supportive conversation about your feelings",
        inline=False
    )
    
    embed.add_field(
        name="/mood",
        value="Log your current mood and intensity",
        inline=False
    )
    
    embed.add_field(
        name="/moodhistory",
        value="View your recent mood logs",
        inline=False
    )
    
    embed.add_field(
        name="/breathing",
        value="Guided breathing exercise (4-7-8 technique)",
        inline=False
    )
    
    embed.add_field(
        name="/affirmation",
        value="Receive a positive affirmation",
        inline=False
    )
    
    embed.add_field(
        name="/resources",
        value="Get crisis hotlines and mental health resources",
        inline=False
    )
    
    embed.add_field(
        name="/clear",
        value="Clear your conversation history",
        inline=False
    )
    
    embed.set_footer(text="All conversations are private and ephemeral")
    
    await interaction.response.send_message(embed=embed, ephemeral=True)

# Run the bot
if __name__ == "__main__":
    bot.run(os.getenv('DISCORD_BOT_TOKEN'))