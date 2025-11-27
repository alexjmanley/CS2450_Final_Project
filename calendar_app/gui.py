import tkinter as tk
from tkinter import scrolledtext
from typing import Optional
import calendar as pycalendar
from datetime import date


class ChatGUI:
    """Simple Tkinter GUI wrapper for a chatbot object with .respond(text)->str method."""

    def __init__(self, bot, title: Optional[str] = "Calendar Chatbot"):
        self.bot = bot
        self.root = tk.Tk()
        self.root.title(title)
        self._build_ui()

    def _build_ui(self):
        # conversation area
        self.txt = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, state=tk.DISABLED, width=80, height=20)
        self.txt.grid(row=0, column=0, columnspan=2, padx=8, pady=8, sticky="nsew")

        # input field
        self.entry_var = tk.StringVar()
        self.entry = tk.Entry(self.root, textvariable=self.entry_var, width=70)
        self.entry.grid(row=1, column=0, padx=8, pady=(0,8), sticky="ew")
        self.entry.bind('<Return>', self._on_enter)

        # send button
        self.send_btn = tk.Button(self.root, text="Send", command=self._on_send)
        self.send_btn.grid(row=1, column=1, padx=8, pady=(0,8), sticky="e")

        # calendar view button
        self.cal_btn = tk.Button(self.root, text="Calendar", command=self._open_calendar)
        self.cal_btn.grid(row=2, column=1, padx=8, pady=(0,8), sticky="e")

        # configure resizing
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # welcome message
        self._append_bot("Hello — I'm your calendar assistant.")
        self.entry.focus()

    def _append(self, who: str, text: str):
        self.txt.configure(state=tk.NORMAL)
        self.txt.insert(tk.END, f"{who}: {text}\n")
        self.txt.see(tk.END)
        self.txt.configure(state=tk.DISABLED)

    def _append_user(self, text: str):
        self._append("You", text)

    def _append_bot(self, text: str):
        self._append("Bot", text)

    def _on_enter(self, event=None):
        self._on_send()
        return 'break'

    def _on_send(self):
        text = self.entry_var.get().strip()
        if not text:
            return
        self._append_user(text)
        try:
            resp = self.bot.respond(text)
        except Exception as e:
            resp = f"Error: {e}"
        self._append_bot(resp)
        self.entry_var.set("")

    def run(self):
        self.root.mainloop()

    def _open_calendar(self):
        # Open a Toplevel window with a month calendar view
        top = tk.Toplevel(self.root)
        top.title("Calendar View")
        # Create the CalendarView and pack it
        view = CalendarView(top, self.bot.calendar)
        view.frame.pack(fill=tk.BOTH, expand=True)


class CalendarView:
    """A simple month-grid calendar view that shows events per day.

    calendar_obj must implement list_events(date: Optional[str]) -> List[Dict]
    where date is an ISO YYYY-MM-DD prefix.
    """
    _instance = None 

    def __new__(cls, parent, calendar_obj):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, parent, calendar_obj):
        if getattr(self, "_initialized", False):
            return
        self._initialized = True

        self.parent = parent
        self.calendar = calendar_obj
        today = date.today()
        self.year = today.year
        self.month = today.month

        self.frame = tk.Frame(parent)
        self._build_ui()
        self._draw_month()

    def _build_ui(self):
        header = tk.Frame(self.frame)
        header.pack(fill=tk.X, padx=6, pady=6)

        self.prev_btn = tk.Button(header, text="◀", width=3, command=self._prev_month)
        self.prev_btn.pack(side=tk.LEFT)

        self.title_lbl = tk.Label(header, text="", font=(None, 14))
        self.title_lbl.pack(side=tk.LEFT, padx=8)

        self.next_btn = tk.Button(header, text="▶", width=3, command=self._next_month)
        self.next_btn.pack(side=tk.LEFT)

        body = tk.Frame(self.frame)
        body.pack(fill=tk.BOTH, expand=True, padx=6, pady=6)

        self.grid_frame = tk.Frame(body)
        self.grid_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # sidebar for events list
        self.side = scrolledtext.ScrolledText(body, width=40, state=tk.DISABLED)
        self.side.pack(side=tk.RIGHT, fill=tk.Y)

    def _draw_month(self):
        # Clear grid
        for w in self.grid_frame.winfo_children():
            w.destroy()

        self.title_lbl.config(text=f"{pycalendar.month_name[self.month]} {self.year}")

        # Weekday headers
        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        for c, d in enumerate(days):
            lbl = tk.Label(self.grid_frame, text=d, borderwidth=1, relief=tk.FLAT)
            lbl.grid(row=0, column=c, padx=2, pady=2, sticky="nsew")

        month_matrix = pycalendar.monthcalendar(self.year, self.month)
        for r, week in enumerate(month_matrix, start=1):
            for c, day in enumerate(week):
                if day == 0:
                    cell = tk.Label(self.grid_frame, text="", borderwidth=1, relief=tk.RIDGE, width=12, height=4)
                    cell.grid(row=r, column=c, padx=2, pady=2, sticky="nsew")
                else:
                    frm = tk.Frame(self.grid_frame, borderwidth=1, relief=tk.RIDGE, width=12, height=4)
                    frm.grid_propagate(False)
                    frm.grid(row=r, column=c, padx=2, pady=2, sticky="nsew")
                    lbl = tk.Label(frm, text=str(day), anchor="nw")
                    lbl.pack(fill=tk.X)

                    # check events for this day
                    iso = f"{self.year}-{self.month:02d}-{day:02d}"
                    try:
                        events = self.calendar.list_events(iso)
                    except Exception:
                        events = []

                    if events:
                        btn = tk.Button(frm, text=f"{len(events)} event(s)", command=lambda d=day: self._show_day(d))
                        btn.pack(side=tk.BOTTOM, pady=2)
                    else:
                        # make the whole cell clickable to show empty day
                        frm.bind("<Button-1>", lambda e, d=day: self._show_day(d))

        # Make grid cells expand evenly
        for i in range(7):
            self.grid_frame.grid_columnconfigure(i, weight=1)

    def _show_day(self, day: int):
        iso = f"{self.year}-{self.month:02d}-{day:02d}"
        try:
            events = self.calendar.list_events(iso)
        except Exception as e:
            events = []

        self.side.configure(state=tk.NORMAL)
        self.side.delete("1.0", tk.END)
        self.side.insert(tk.END, f"Events for {iso}:\n\n")
        if not events:
            self.side.insert(tk.END, "No events.\n")
        else:
            for e in events:
                self.side.insert(tk.END, f"#{e['id']} {e['start']} - {e['title']}\n")
        self.side.configure(state=tk.DISABLED)

    def _prev_month(self):
        if self.month == 1:
            self.month = 12
            self.year -= 1
        else:
            self.month -= 1
        self._draw_month()

    def _next_month(self):
        if self.month == 12:
            self.month = 1
            self.year += 1
        else:
            self.month += 1
        self._draw_month()
