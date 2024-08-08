import streamlit as st
import threading
import time
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def run_bot():
    import telegram_bot
    telegram_bot.main()

def main():
    st.title("Streamlit App with Telegram Bot")
    bot_thread = threading.Thread(target=run_bot)
    bot_thread.start()
   
if __name__ == "__main__":
    main()