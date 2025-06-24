# bot developer @mr_jisshu
import os
from flask import Flask, request
from bot import Bot

# Load environment variables
BOT_TOKEN = os.environ["BOT_TOKEN"]
WEBHOOK_URL = os.environ["WEBHOOK_URL"]

# Initialize Flask and your bot class
flask_app = Flask(__name__)
bot = Bot()

@flask_app.route("/")
def index():
    return "Forward Bot is Running!"

@flask_app.route(f"/{BOT_TOKEN}", methods=["POST"])
def webhook():
    if request.headers.get("content-type") == "application/json":
        update = request.get_json()
        bot.process_update(update)  # This should be defined in your Bot class
        return "ok"
    return "Invalid request"

@flask_app.before_first_request
def set_webhook():
    bot.set_webhook(f"{WEBHOOK_URL}/{BOT_TOKEN}")  # Should be defined in Bot class

if __name__ == "__main__":
    bot.start()  # Optional: If your Bot class requires setup
    flask_app.run(host="0.0.0.0", port=8080)
