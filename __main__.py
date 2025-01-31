from src import get_discord_token, quiz_bot

DISCORD_TOKEN = get_discord_token()

def main() -> None:
    """Start the Discord bot."""
    quiz_bot.run(DISCORD_TOKEN)

if __name__ == '__main__':
    main()