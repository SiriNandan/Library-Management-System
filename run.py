# run.py
import os
from pyngrok import ngrok
from app import app

PORT = 3000

def start():
    print("🔄 Starting Flask server with ngrok tunnel...")

    # Start ngrok tunnel
    public_url = ngrok.connect(PORT, "http").public_url
    print(f"🌍 PUBLIC URL: {public_url}")
    print(f"➡️  FULL WEBHOOK URL: {public_url}/webhook")

    print("\n📌 Copy the above URL into your GitHub App's Webhook URL.\n")

    # Start Flask
    app.run(host="0.0.0.0", port=PORT)

if __name__ == "__main__":
    start()
