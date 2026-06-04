import subprocess
import time
import os

def run_auto_poster():
    print("Running auto-poster...")
    try:
        subprocess.run(["python3", "/home/ubuntu/it-link-ai-bot/auto_poster.py"], check=True)
    except Exception as e:
        print(f"Auto-poster failed: {e}")

def run_bot_service():
    print("Starting IT Link AI Bot service...")
    # This will run the Flask app
    try:
        subprocess.run(["python3", "/home/ubuntu/it-link-ai-bot/it_link_bot.py"])
    except Exception as e:
        print(f"Bot service failed: {e}")

if __name__ == "__main__":
    # In a real scenario, the auto-poster would be scheduled.
    # For this task, we've already run it once and set up the project context.
    # The scheduled task will re-trigger this session.
    
    # Run auto-poster once at start
    run_auto_poster()
    
    # Then start the bot service to handle messages
    run_bot_service()
