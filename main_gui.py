import os
import sys

from calendar_app.calendar import Calendar
from calendar_app.chatbot import ChatBot
from calendar_app.gui import ChatGUI


def main():
    db_path = os.path.join(os.path.dirname(__file__), "calendar.db")
    cal = Calendar(db_path)
    bot = ChatBot(cal)
    gui = ChatGUI(bot, title="Calendar Chatbot GUI")
    gui.run()


if __name__ == '__main__':
    main()
