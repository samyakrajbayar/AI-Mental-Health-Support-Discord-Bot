# 💙 AI Mental Health Support Discord Bot

A compassionate Discord bot designed to provide mental health support, mood tracking, and coping resources using Claude AI by Anthropic.

## ⚠️ Important Disclaimer

**This bot is NOT a replacement for professional mental health care.** It is designed to provide supportive conversations and resources, but should not be used as a substitute for therapy, counseling, or medical treatment. If you're experiencing a mental health crisis, please contact emergency services or a crisis hotline immediately.

## ✨ Features

- **🤖 AI-Powered Conversations**: Empathetic support conversations using Claude Sonnet 4
- **📊 Mood Tracking**: Log and track your mood over time
- **🧘 Breathing Exercises**: Guided 4-7-8 breathing technique
- **💫 Daily Affirmations**: Positive affirmations for mental wellbeing
- **🆘 Crisis Resources**: Immediate access to crisis hotlines and mental health resources
- **🔒 Privacy-Focused**: All conversations are private and ephemeral
- **📚 Conversation History**: Maintains context across conversations (stored in memory)

## 🚀 Commands

| Command | Description |
|---------|-------------|
| `/talk` | Have a supportive conversation about your feelings |
| `/mood` | Log your current mood and intensity (1-10) |
| `/moodhistory` | View your recent mood logs |
| `/breathing` | Start a guided breathing exercise |
| `/affirmation` | Receive a positive affirmation |
| `/resources` | Get crisis hotlines and mental health resources |
| `/clear` | Clear your conversation history |
| `/help` | View all available commands |

## 📋 Prerequisites

- Python 3.8 or higher
- Discord account and server
- Discord Bot Token
- Anthropic API Key (Claude AI)

## 🛠️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/mental-health-discord-bot.git
cd mental-health-discord-bot
```

### 2. Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Discord Bot

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click "New Application" and give it a name
3. Go to the "Bot" section and click "Add Bot"
4. Under "Privileged Gateway Intents", enable:
   - MESSAGE CONTENT INTENT
   - SERVER MEMBERS INTENT
5. Click "Reset Token" and copy your bot token
6. Go to "OAuth2" > "URL Generator"
7. Select scopes: `bot` and `applications.commands`
8. Select bot permissions:
   - Send Messages
   - Use Slash Commands
   - Embed Links
   - Read Message History
9. Copy the generated URL and use it to invite the bot to your server

### 5. Get Anthropic API Key

1. Go to [Anthropic Console](https://console.anthropic.com/)
2. Sign up or log in
3. Navigate to API Keys
4. Create a new API key and copy it

### 6. Configure Environment Variables

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Edit `.env` and add your tokens:

```env
DISCORD_BOT_TOKEN=your_discord_bot_token_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
```

### 7. Run the Bot

```bash
python bot.py
```

You should see: `[BotName] has connected to Discord!`

## 📁 Project Structure

```
mental-health-discord-bot/
│
├── bot.py                 # Main bot file
├── config.py             # Configuration settings
├── requirements.txt      # Python dependencies
├── .env.example         # Environment variables template
├── .env                 # Your environment variables (not tracked)
├── .gitignore          # Git ignore rules
└── README.md           # This file
```

## 🔧 Configuration

You can modify `config.py` to customize:

- Maximum conversation history length
- Maximum mood logs stored
- Crisis detection keywords
- Bot prefix (if using text commands)

## 🔒 Privacy & Security

- All conversations are ephemeral (only visible to the user)
- Conversation history is stored in memory (cleared on restart)
- No data is permanently stored without user consent
- Crisis keywords trigger automatic resource sharing
- API keys are stored securely in environment variables

## 🆘 Crisis Detection

The bot monitors for crisis keywords and automatically provides resources when detected. Current crisis resources include:

- **US**: 988 Suicide & Crisis Lifeline
- **UK**: Samaritans (116 123)
- **Canada**: Talk Suicide Canada (1-833-456-4566)
- **International**: IASP Crisis Centers

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 Future Enhancements

- [ ] Database integration for persistent storage
- [ ] Scheduled check-ins and reminders
- [ ] Integration with meditation/mindfulness APIs
- [ ] Support group channels
- [ ] Anonymous peer support matching
- [ ] Multi-language support
- [ ] Web dashboard for mood tracking visualization
- [ ] Integration with mental health professional directory

## ⚖️ License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **Anthropic** for Claude AI API
- **Discord.py** for the excellent Discord library
- Mental health organizations providing crisis resources

## ⚠️ Mental Health Resources

### United States
- **988 Suicide & Crisis Lifeline**: Call or text 988
- **Crisis Text Line**: Text HOME to 741741
- **NAMI Helpline**: 1-800-950-6264

### United Kingdom
- **Samaritans**: 116 123
- **Shout Crisis Text Line**: Text SHOUT to 85258

### Canada
- **Talk Suicide Canada**: 1-833-456-4566
- **Crisis Text Line**: Text TALK to 686868

### International
- **IASP Crisis Centers**: https://www.iasp.info/resources/Crisis_Centres/

---

**Remember**: You are not alone. Help is available 24/7. This bot is a tool to support you, but professional help is irreplaceable for serious mental health concerns.

## 🌟 Star this project if you find it helpful!

Made with 💙 for mental health awareness and support.
