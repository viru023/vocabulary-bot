# Vocabulary Bot

This project is a Telegram bot that sends daily vocabulary from a specific website to a Telegram channel or chat. It fetches vocabulary, synonyms, and antonyms from the site, formats the data, and sends it through Telegram.

## Features

- Scrapes vocabulary data from WordPandit daily
- Sends vocabulary to a specified Telegram chat
- Schedules messages daily at a specified time

## Installation

### Prerequisites

- Python 3.x
- A Telegram bot token and chat ID (for sending messages)

### Steps

1. Clone the repository.

   ```bash
   git clone https://github.com/viru023/vocabulary-bot.git
   cd vocabulary-bot
   ```

2. Install required packages.

    ```bash
    pip install -r requirements.txt
    ```

3. Create a .env file with your Telegram bot token and chat ID.

    ```bash
    TELEGRAM_TOKEN=your_bot_token
    TELEGRAM_CHAT_ID=your_chat_id
    ````

4. Run the script to start the bot.

    ```bash
    python bot_script.py
    ```

## Usage

The bot is set up to run daily and fetch the latest vocabulary. You can modify the fetch URL or schedule by editing the bot_script.py file.

## Dependencies

See requirements.txt for a list of dependencies.

```bash
python bot_script.py
```
