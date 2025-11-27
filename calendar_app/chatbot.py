import re
import requests
import json 

from typing import Tuple

from .calendar import Calendar


class ChatBot:
    def __init__(self, calendar: Calendar):
        self.calendar = calendar
    '''
    def respond(self, text: str) -> str:
        text = text.strip()
        if not text:
            return "I didn't get that. Type 'help' for commands."

        low = text.lower()
        if low.startswith("help"):
            return self._help_text()
        if low.startswith("add "):
            return self._handle_add(text[4:].strip())
        if low.startswith("list"):
            return self._handle_list(text[4:].strip())
        if low.startswith("remove") or low.startswith("delete"):
            return self._handle_remove(text)

        return "Sorry, I didn't understand. Type 'help' for examples."
    '''
    def ask_llm(self, prompt: str) -> str:
        url = "http://localhost:11434/api/generate"
        headers = {"Content-Type": "application/json"}
        data = {"model": "llama3.2:1b", "prompt": prompt, "stream": True}

        response = requests.post(url, headers=headers, json=data, stream=True)

        output = ""
        for line in response.iter_lines():
            if line:
                try:
                    obj = json.loads(line.decode("utf-8"))
                    output += obj.get("response", "")
                except json.JSONDecodeError:
                    continue

        print(output)
        return output

    def respond(self, text: str) -> str:
        text = text.strip()
        reply = self.ask_llm(text)

        return reply 

    def _help_text(self) -> str:
        return (
            "Commands:\n"
            "- add <title> on YYYY-MM-DD [at HH:MM]\n"
            "  e.g. add Team meeting on 2025-11-20 at 14:00\n"
            "- list\n"
            "- list on YYYY-MM-DD\n"
            "- remove <id>\n"
            "- help\n"
        )

    def _handle_add(self, body: str) -> str:
        # Try to parse patterns: "<title> on <date> at <time>"
        m = re.match(r"(?P<title>.+) on (?P<date>\S+)(?: at (?P<time>\S+))?", body, re.IGNORECASE)
        if m:
            title = m.group("title").strip()
            date = m.group("date")
            time = m.group("time")
            when = f"{date} {time}".strip() if time else date
            try:
                eid = self.calendar.add_event(title, when)
                return f"Added event #{eid}: {title} at {when}"
            except Exception as e:
                return f"Failed to add event: {e}"

        # Fallback: if body starts with a date first
        m2 = re.match(r"(?P<date>\S+) (?P<title>.+)", body)
        if m2:
            date = m2.group("date")
            title = m2.group("title")
            try:
                eid = self.calendar.add_event(title, date)
                return f"Added event #{eid}: {title} at {date}"
            except Exception as e:
                return f"Failed to add event: {e}"

        return "Could not parse add command. Try: add Meeting on 2025-11-20 at 14:00"

    def _handle_list(self, body: str) -> str:
        body = body.strip()
        if body.startswith("on "):
            date = body[3:].strip()
            events = self.calendar.list_events(date)
        elif body == "":
            events = self.calendar.list_events()
        else:
            # maybe body is a date
            events = self.calendar.list_events(body)

        if not events:
            return "No events found."

        lines = []
        for e in events:
            lines.append(f"#{e['id']} {e['start']} - {e['title']}")
        return "\n".join(lines)

    def _handle_remove(self, text: str) -> str:
        m = re.search(r"(remove|delete)\s+(?P<id>\d+)", text, re.IGNORECASE)
        if not m:
            return "Usage: remove <id>\nUse 'list' to see ids."
        eid = int(m.group("id"))
        ok = self.calendar.remove_event(eid)
        return "Removed." if ok else "Event not found."
