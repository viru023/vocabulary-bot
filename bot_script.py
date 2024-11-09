import os
import requests
from bs4 import BeautifulSoup
from apscheduler.schedulers.blocking import BlockingScheduler
from telegram import Bot
from dotenv import load_dotenv
import logging
from datetime import datetime

# Load environment variables from a .env file
load_dotenv()
TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Function to fetch and parse the vocabulary data
def fetch_vocabulary():
    # Generate the URL with the current date
    today_date = datetime.now().strftime("%B-%d-%Y").lower()  # e.g., "november-1-2024"
    url = f"https://wordpandit.com/daily-vocabulary-from-indian-newspapers-and-publications-{today_date}/"
    
    try:
        # Fetch the page content
        response = requests.get(url)
        response.raise_for_status()  # Check for request errors
        soup = BeautifulSoup(response.text, "html.parser")

        message = ""

        # Loop through row1 to row5
        for i in range(1, 6):  # From row1 to row5
            class_name = f"et_pb_row et_pb_row_{i}"
            word_divs = soup.find_all("div", class_=class_name)

            for word_div in word_divs:
                # Extract word title
                word_title = word_div.find("h2").get_text(strip=True) if word_div.find("h2") else "Title not found"

                # Extract synonyms and antonyms
                synonyms_antonyms = word_div.find("div", class_="synonyms-antonyms")
                if synonyms_antonyms:
                    synonyms = synonyms_antonyms.find("p").get_text(strip=True).replace("Synonyms:", "").strip() if synonyms_antonyms.find("p") else "Synonyms not found"
                    antonyms = synonyms_antonyms.find_all("p")[1].get_text(strip=True).replace("Antonyms:", "").strip() if len(synonyms_antonyms.find_all("p")) > 1 else "Antonyms not found"
                else:
                    synonyms = "Synonyms not found"
                    antonyms = "Antonyms not found"

                # Add to message
                message += f"Word Title: {word_title}\n"
                message += f"Synonyms: {synonyms}\n"
                message += f"Antonyms: {antonyms}\n"
                message += "-" * 30 + "\n"

                # Send message if it approaches Telegram's message length limit
                if len(message) > 3500:
                    send_telegram_message(message)
                    message = ""

        # Send remaining message content, if any
        if message:
            send_telegram_message(message)

    except requests.RequestException as e:
        logging.error(f"Failed to fetch data: {e}")
    except Exception as e:
        logging.error(f"An error occurred: {e}")

# Function to send message to Telegram
def send_telegram_message(message):
    try:
        bot = Bot(token=TOKEN)
        bot.send_message(chat_id=CHAT_ID, text=message)
        logging.info("Message sent to Telegram successfully.")
    except Exception as e:
        logging.error(f"Failed to send message: {e}")

# Function to set up the scheduler
def setup_scheduler():
    scheduler = BlockingScheduler()
    # Schedule the job to run daily at a specific time (e.g., 8:00 AM)
    scheduler.add_job(fetch_vocabulary, 'interval', days=1, start_date='2024-11-09 08:00:00')
    logging.info("Scheduled task set for daily vocabulary posting.")
    scheduler.start()

if __name__ == '__main__':
    setup_scheduler()
