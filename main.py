import os

from calendar_app.calendar import Calendar
from calendar_app.chatbot import ChatBot


def main():
    # store DB in local file in project folder
    db_path = os.path.join(os.path.dirname(__file__), "calendar.db")
    cal = Calendar(db_path)
    bot = ChatBot(cal)

    print("Calendar Chatbot — type 'help' for commands. Type 'quit' or 'exit' to stop.")
    while True:
        try:
            text = input("You: ")
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye")
            break
        if not text:
            continue
        if text.strip().lower() in ("quit", "exit"):
            print("Goodbye")
            break
        resp = bot.respond(text)
        print("Bot:", resp)


if __name__ == "__main__":
    main()
