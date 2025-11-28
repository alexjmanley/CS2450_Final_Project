import tkinter as tk
from tkinter import scrolledtext, font
from typing import Optional
import calendar as pycalendar
from datetime import date


class ChatGUI:
    """Simple Tkinter GUI wrapper for a chatbot object with .respond(text)->str method."""

    def __init__(self, bot, title: Optional[str] = "Calendar Chatbot"):
        self.bot = bot
        self.root = tk.Tk()
        self.root.title(title)
        
        # Modern color scheme - warm cream/yellow professional palette
        self.bg_color = "#FFFCF5"  # Warm white background
        self.primary_color = "#F4D03F"  # Soft golden yellow
        self.secondary_color = "#FFF2CC"  # Light cream
        self.accent_color = "#E8B923"  # Rich golden
        self.text_color = "#2C3E50"  # Dark blue-grey
        self.bot_bg = "#FFF9E6"  # Very light cream for bot messages
        self.user_bg = "#FFF2CC"  # Slightly darker cream for user messages
        
        self.root.configure(bg=self.bg_color)
        self._build_ui()

    def _build_ui(self):
        # Main container frame with two columns (chat + calendar)
        main_frame = tk.Frame(self.root, bg=self.bg_color)
        main_frame.grid(row=0, column=0, sticky="nsew", padx=15, pady=15)
        
        # Configure main grid
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(2, weight=1)  # Chat area row
        main_frame.grid_columnconfigure(0, weight=2)  # Chat column
        main_frame.grid_columnconfigure(1, weight=3)  # Calendar column
        
        # Title label
        title_font = font.Font(family="Segoe UI", size=16, weight="bold")
        title_label = tk.Label(main_frame, text="📅 Calendar Assistant", 
                               font=title_font, bg=self.bg_color, fg=self.text_color)
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 10), sticky="w")
        
        # Toggle calendar button
        toggle_font = font.Font(family="Segoe UI", size=10, weight="bold")
        self.toggle_cal_btn = tk.Button(
            main_frame, text="◀ Hide Calendar", command=self._toggle_calendar,
            font=toggle_font, bg=self.primary_color, fg=self.text_color,
            relief=tk.FLAT, bd=0, padx=15, pady=6,
            cursor="hand2", activebackground=self.accent_color
        )
        self.toggle_cal_btn.grid(row=1, column=1, sticky="e", pady=(0, 5))
        self.calendar_visible = True
        
        # conversation area with modern styling
        chat_frame = tk.Frame(main_frame, bg=self.secondary_color, relief=tk.FLAT, bd=0)
        chat_frame.grid(row=2, column=0, sticky="nsew", pady=(0, 12), padx=(0, 10))
        
        self.txt = scrolledtext.ScrolledText(
            chat_frame, wrap=tk.WORD, state=tk.DISABLED, 
            width=50, height=25,
            bg=self.bg_color, fg=self.text_color,
            font=("Segoe UI", 10),
            relief=tk.FLAT, bd=0,
            padx=10, pady=10
        )
        self.txt.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        
        # Configure text tags for styled messages
        self.txt.tag_configure("user", foreground="#2C5F8D", font=("Segoe UI", 10, "bold"))
        self.txt.tag_configure("bot", foreground="#7D6608", font=("Segoe UI", 10, "bold"))
        self.txt.tag_configure("user_msg", background=self.user_bg, lmargin1=10, lmargin2=10, 
                              rmargin=10, spacing1=5, spacing3=5)
        self.txt.tag_configure("bot_msg", background=self.bot_bg, lmargin1=10, lmargin2=10, 
                              rmargin=10, spacing1=5, spacing3=5)

        # Calendar view embedded on the right side
        self.calendar_frame = tk.Frame(main_frame, bg=self.bg_color)
        self.calendar_frame.grid(row=2, column=1, rowspan=2, sticky="nsew", pady=(0, 12))
        
        # Create embedded calendar
        self.calendar_view = CalendarView(self.calendar_frame, self.bot.calendar)
        self.calendar_view.frame.pack(fill=tk.BOTH, expand=True)
        
        # Input frame
        input_frame = tk.Frame(main_frame, bg=self.bg_color)
        input_frame.grid(row=3, column=0, sticky="ew", pady=(0, 8))
        
        # input field with modern styling
        self.entry_var = tk.StringVar()
        entry_font = font.Font(family="Segoe UI", size=10)
        self.entry = tk.Entry(
            input_frame, textvariable=self.entry_var,
            font=entry_font, bg="white", fg=self.text_color,
            relief=tk.SOLID, bd=1,
            insertbackground=self.text_color
        )
        self.entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, ipady=8, ipadx=8)
        self.entry.bind('<Return>', self._on_enter)

        # Button frame
        btn_frame = tk.Frame(main_frame, bg=self.bg_color)
        btn_frame.grid(row=4, column=0, sticky="e")
        
        # Modern styled buttons
        btn_font = font.Font(family="Segoe UI", size=10, weight="bold")
        
        self.send_btn = tk.Button(
            btn_frame, text="Send", command=self._on_send,
            font=btn_font, bg=self.accent_color, fg="white",
            relief=tk.FLAT, bd=0, padx=20, pady=8,
            cursor="hand2", activebackground="#D4A017"
        )
        self.send_btn.pack(side=tk.RIGHT, padx=(8, 0))

        # Set minimum window size for side-by-side layout
        self.root.minsize(1200, 600)
        
        # welcome message
        self._append_bot("Hello! 👋 I'm your calendar assistant. Type 'help' for commands.")

        self.entry.focus()

    def _append(self, who: str, text: str, is_bot: bool = False):
        self.txt.configure(state=tk.NORMAL)
        
        # Add sender label with styling
        tag = "bot" if is_bot else "user"
        msg_tag = "bot_msg" if is_bot else "user_msg"
        
        self.txt.insert(tk.END, f"{who}: ", tag)
        self.txt.insert(tk.END, f"{text}\n\n", msg_tag)
        self.txt.see(tk.END)
        self.txt.configure(state=tk.DISABLED)

    def _append_user(self, text: str):
        self._append("You", text, is_bot=False)

    def _append_bot(self, text: str):
        self._append("Bot", text, is_bot=True)

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
    
    def _toggle_calendar(self):
        """Toggle calendar visibility"""
        if self.calendar_visible:
            # Hide calendar
            self.calendar_frame.grid_remove()
            self.toggle_cal_btn.config(text="▶ Show Calendar")
            self.calendar_visible = False
            # Adjust window for chat-only mode
            self.root.minsize(700, 600)
        else:
            # Show calendar
            self.calendar_frame.grid()
            self.toggle_cal_btn.config(text="◀ Hide Calendar")
            self.calendar_visible = True
            # Adjust window for side-by-side mode
            self.root.minsize(1200, 600)


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
        self.day = today.day
        self.current_view = "month"  # "day", "month", or "year"
        
        # Professional color scheme matching main window
        self.bg_color = "#FFFCF5"
        self.header_bg = "#FFF2CC"
        self.cell_bg = "#FFFAEE"
        self.cell_header_bg = "#FFE5A3"
        self.event_bg = "#F4D03F"
        self.text_color = "#2C3E50"
        self.accent_color = "#E8B923"

        self.frame = tk.Frame(parent, bg=self.bg_color)
        self._build_ui()
        self._refresh_view()

    def _build_ui(self):
        # Header with navigation
        header = tk.Frame(self.frame, bg=self.header_bg, relief=tk.FLAT, bd=0)
        header.pack(fill=tk.X, padx=0, pady=(0, 12))
        
        # Navigation buttons with modern styling
        btn_font = font.Font(family="Segoe UI", size=11, weight="bold")
        
        self.prev_btn = tk.Button(
            header, text="◀", command=self._prev_period,
            font=btn_font, bg=self.accent_color, fg="white",
            relief=tk.FLAT, bd=0, padx=15, pady=8,
            cursor="hand2", activebackground="#D4A017"
        )
        self.prev_btn.pack(side=tk.LEFT, padx=10, pady=10)

        title_font = font.Font(family="Segoe UI", size=18, weight="bold")
        self.title_lbl = tk.Label(
            header, text="", font=title_font,
            bg=self.header_bg, fg=self.text_color
        )
        self.title_lbl.pack(side=tk.LEFT, padx=15)

        self.next_btn = tk.Button(
            header, text="▶", command=self._next_period,
            font=btn_font, bg=self.accent_color, fg="white",
            relief=tk.FLAT, bd=0, padx=15, pady=8,
            cursor="hand2", activebackground="#D4A017"
        )
        self.next_btn.pack(side=tk.LEFT)
        
        # View switcher buttons
        view_frame = tk.Frame(header, bg=self.header_bg)
        view_frame.pack(side=tk.RIGHT, padx=10)
        
        view_btn_font = font.Font(family="Segoe UI", size=10, weight="bold")
        
        self.day_view_btn = tk.Button(
            view_frame, text="Day", command=lambda: self._switch_view("day"),
            font=view_btn_font, bg=self.cell_bg, fg=self.text_color,
            relief=tk.FLAT, bd=0, padx=12, pady=6,
            cursor="hand2", activebackground=self.event_bg
        )
        self.day_view_btn.pack(side=tk.LEFT, padx=2)
        
        self.month_view_btn = tk.Button(
            view_frame, text="Month", command=lambda: self._switch_view("month"),
            font=view_btn_font, bg=self.event_bg, fg=self.text_color,
            relief=tk.FLAT, bd=0, padx=12, pady=6,
            cursor="hand2", activebackground=self.event_bg
        )
        self.month_view_btn.pack(side=tk.LEFT, padx=2)
        
        self.year_view_btn = tk.Button(
            view_frame, text="Year", command=lambda: self._switch_view("year"),
            font=view_btn_font, bg=self.cell_bg, fg=self.text_color,
            relief=tk.FLAT, bd=0, padx=12, pady=6,
            cursor="hand2", activebackground=self.event_bg
        )
        self.year_view_btn.pack(side=tk.LEFT, padx=2)

        # Body container
        body = tk.Frame(self.frame, bg=self.bg_color)
        body.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)

        # Calendar grid frame
        self.grid_frame = tk.Frame(body, bg=self.bg_color)
        self.grid_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        # Sidebar for events list with modern styling
        sidebar_frame = tk.Frame(body, bg=self.header_bg, relief=tk.FLAT, bd=0)
        sidebar_frame.pack(side=tk.RIGHT, fill=tk.Y)
        
        sidebar_title = tk.Label(
            sidebar_frame, text="📋 Event Details",
            font=font.Font(family="Segoe UI", size=12, weight="bold"),
            bg=self.header_bg, fg=self.text_color, pady=10
        )
        sidebar_title.pack(fill=tk.X, padx=10)
        
        self.side = scrolledtext.ScrolledText(
            sidebar_frame, width=35, state=tk.DISABLED,
            bg=self.cell_bg, fg=self.text_color,
            font=("Segoe UI", 10),
            relief=tk.FLAT, bd=0, padx=10, pady=10
        )
        self.side.pack(fill=tk.BOTH, expand=True, padx=2, pady=(0, 2))

    def _draw_month(self):
        # Clear grid
        for w in self.grid_frame.winfo_children():
            w.destroy()

        self.title_lbl.config(text=f"{pycalendar.month_name[self.month]} {self.year}")

        # Weekday headers with professional styling
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        header_font = font.Font(family="Segoe UI", size=10, weight="bold")
        
        for c, d in enumerate(days):
            lbl = tk.Label(
                self.grid_frame, text=d,
                font=header_font, bg=self.cell_header_bg, fg=self.text_color,
                relief=tk.FLAT, bd=0, pady=8
            )
            lbl.grid(row=0, column=c, padx=1, pady=(0, 2), sticky="nsew")

        # Get today's date for highlighting
        today = date.today()
        is_current_month = (today.year == self.year and today.month == self.month)
        
        month_matrix = pycalendar.monthcalendar(self.year, self.month)
        day_font = font.Font(family="Segoe UI", size=11, weight="bold")
        event_font = font.Font(family="Segoe UI", size=9)
        
        for r, week in enumerate(month_matrix, start=1):
            for c, day in enumerate(week):
                if day == 0:
                    # Empty cell for days from other months
                    cell = tk.Frame(self.grid_frame, bg=self.bg_color, relief=tk.FLAT, bd=0)
                    cell.grid(row=r, column=c, padx=1, pady=1, sticky="nsew")
                else:
                    # Determine if this is today
                    is_today = is_current_month and day == today.day
                    cell_bg = "#FFD700" if is_today else self.cell_bg
                    
                    frm = tk.Frame(
                        self.grid_frame, bg=cell_bg,
                        relief=tk.SOLID, bd=1,
                        highlightthickness=2 if is_today else 0,
                        highlightbackground=self.accent_color if is_today else cell_bg
                    )
                    frm.grid(row=r, column=c, padx=1, pady=1, sticky="nsew")
                    
                    # Day number
                    day_label = tk.Label(
                        frm, text=str(day), anchor="nw",
                        font=day_font, bg=cell_bg, fg=self.text_color,
                        padx=8, pady=5
                    )
                    day_label.pack(fill=tk.X, anchor="n")

                    # Check events for this day
                    iso = f"{self.year}-{self.month:02d}-{day:02d}"
                    try:
                        events = self.calendar.list_events(iso)
                    except Exception:
                        events = []

                    if events:
                        # Event indicator button
                        event_btn = tk.Button(
                            frm, text=f"📌 {len(events)} event{'s' if len(events) > 1 else ''}",
                            command=lambda d=day: self._show_day(d),
                            font=event_font, bg=self.event_bg, fg=self.text_color,
                            relief=tk.FLAT, bd=0, cursor="hand2",
                            activebackground=self.accent_color, pady=4
                        )
                        event_btn.pack(side=tk.BOTTOM, fill=tk.X, padx=5, pady=5)
                    else:
                        # Make the whole cell clickable to show empty day
                        frm.bind("<Button-1>", lambda e, d=day: self._show_day(d))
                        frm.config(cursor="hand2")
                        day_label.config(cursor="hand2")
                        day_label.bind("<Button-1>", lambda e, d=day: self._show_day(d))

        # Make grid cells expand evenly
        for i in range(7):
            self.grid_frame.grid_columnconfigure(i, weight=1)
        
        # Make rows expand
        for i in range(1, len(month_matrix) + 1):
            self.grid_frame.grid_rowconfigure(i, weight=1)

    def _show_day(self, day: int):
        iso = f"{self.year}-{self.month:02d}-{day:02d}"
        try:
            events = self.calendar.list_events(iso)
        except Exception as e:
            events = []

        self.side.configure(state=tk.NORMAL)
        self.side.delete("1.0", tk.END)
        
        # Format date nicely
        date_obj = date(self.year, self.month, day)
        formatted_date = date_obj.strftime("%A, %B %d, %Y")
        
        self.side.insert(tk.END, f"{formatted_date}\n", "date_header")
        self.side.insert(tk.END, "─" * 35 + "\n\n", "separator")
        
        if not events:
            self.side.insert(tk.END, "No events scheduled for this day.\n", "no_events")
        else:
            for i, e in enumerate(events, 1):
                self.side.insert(tk.END, f"Event #{e['id']}\n", "event_id")
                self.side.insert(tk.END, f"🕐 {e['start']}\n", "event_time")
                self.side.insert(tk.END, f"📝 {e['title']}\n\n", "event_title")
        
        # Configure text tags for styled output
        self.side.tag_configure("date_header", font=("Segoe UI", 11, "bold"), 
                               foreground=self.text_color, spacing1=5)
        self.side.tag_configure("separator", foreground="#BDB76B")
        self.side.tag_configure("no_events", font=("Segoe UI", 10, "italic"), 
                               foreground="#888888", spacing1=10)
        self.side.tag_configure("event_id", font=("Segoe UI", 9, "bold"), 
                               foreground=self.accent_color)
        self.side.tag_configure("event_time", font=("Segoe UI", 10), 
                               foreground="#2C5F8D", lmargin1=15)
        self.side.tag_configure("event_title", font=("Segoe UI", 10), 
                               foreground=self.text_color, lmargin1=15)
        
        self.side.configure(state=tk.DISABLED)
    
    def _draw_day(self):
        """Draw a detailed day view with hourly time slots"""
        # Clear grid
        for w in self.grid_frame.winfo_children():
            w.destroy()
        
        # Update title
        date_obj = date(self.year, self.month, self.day)
        self.title_lbl.config(text=date_obj.strftime("%A, %B %d, %Y"))
        
        # Get events for this day
        iso = f"{self.year}-{self.month:02d}-{self.day:02d}"
        try:
            events = self.calendar.list_events(iso)
        except Exception:
            events = []
        
        # Create a scrollable canvas for the day view
        canvas = tk.Canvas(self.grid_frame, bg=self.bg_color, highlightthickness=0)
        scrollbar = tk.Scrollbar(self.grid_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.bg_color)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Create hourly time slots (6 AM to 11 PM)
        hour_font = font.Font(family="Segoe UI", size=10, weight="bold")
        event_font = font.Font(family="Segoe UI", size=9)
        
        for hour in range(6, 24):
            hour_frame = tk.Frame(scrollable_frame, bg=self.cell_bg, relief=tk.SOLID, bd=1)
            hour_frame.pack(fill=tk.X, padx=5, pady=2)
            
            # Time label
            time_str = f"{hour:02d}:00"
            if hour < 12:
                display_time = f"{hour}:00 AM" if hour != 0 else "12:00 AM"
            else:
                display_time = f"{hour-12 if hour != 12 else 12}:00 PM"
            
            time_label = tk.Label(
                hour_frame, text=display_time,
                font=hour_font, bg=self.cell_bg, fg=self.text_color,
                width=12, anchor="w", padx=10, pady=8
            )
            time_label.pack(side=tk.LEFT, fill=tk.Y)
            
            # Event container for this hour
            event_container = tk.Frame(hour_frame, bg=self.cell_bg)
            event_container.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)
            
            # Check if any events fall in this hour
            hour_events = []
            for e in events:
                event_time = e['start']
                # Parse time from event (format: YYYY-MM-DD HH:MM)
                if len(event_time) >= 16:
                    event_hour = int(event_time[11:13])
                    if event_hour == hour:
                        hour_events.append(e)
            
            if hour_events:
                for e in hour_events:
                    event_label = tk.Label(
                        event_container, text=f"📌 {e['title']}",
                        font=event_font, bg=self.event_bg, fg=self.text_color,
                        anchor="w", padx=10, pady=5, cursor="hand2"
                    )
                    event_label.pack(fill=tk.X, pady=2)
                    # Make clickable to show details
                    event_label.bind("<Button-1>", lambda e, d=self.day: self._show_day(d))
        
        # Show events in sidebar
        self._show_day(self.day)
    
    def _draw_year(self):
        """Draw a year overview with 12 months in a grid"""
        # Clear grid
        for w in self.grid_frame.winfo_children():
            w.destroy()
        
        # Update title
        self.title_lbl.config(text=str(self.year))
        
        # Create 12-month grid (3 rows x 4 columns)
        mini_month_font = font.Font(family="Segoe UI", size=9, weight="bold")
        day_font = font.Font(family="Segoe UI", size=7)
        
        for month_idx in range(1, 13):
            row = (month_idx - 1) // 4
            col = (month_idx - 1) % 4
            
            # Month container
            month_frame = tk.Frame(
                self.grid_frame, bg=self.cell_bg,
                relief=tk.SOLID, bd=1
            )
            month_frame.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
            
            # Month name header
            month_name = pycalendar.month_name[month_idx]
            month_label = tk.Label(
                month_frame, text=month_name,
                font=mini_month_font, bg=self.cell_header_bg, fg=self.text_color,
                pady=5
            )
            month_label.pack(fill=tk.X)
            
            # Mini calendar grid
            mini_grid = tk.Frame(month_frame, bg=self.cell_bg)
            mini_grid.pack(fill=tk.BOTH, expand=True, padx=3, pady=3)
            
            # Day headers (abbreviated)
            days_abbrev = ["M", "T", "W", "T", "F", "S", "S"]
            for c, d in enumerate(days_abbrev):
                lbl = tk.Label(
                    mini_grid, text=d, font=day_font,
                    bg=self.cell_bg, fg=self.text_color, width=3
                )
                lbl.grid(row=0, column=c, sticky="nsew")
            
            # Days of month
            month_matrix = pycalendar.monthcalendar(self.year, month_idx)
            today = date.today()
            
            for r, week in enumerate(month_matrix, start=1):
                for c, day in enumerate(week):
                    if day == 0:
                        lbl = tk.Label(mini_grid, text="", bg=self.cell_bg, width=3, height=1)
                    else:
                        # Check if this is today
                        is_today = (today.year == self.year and 
                                   today.month == month_idx and 
                                   today.day == day)
                        
                        # Check if day has events
                        iso = f"{self.year}-{month_idx:02d}-{day:02d}"
                        try:
                            day_events = self.calendar.list_events(iso)
                            has_events = len(day_events) > 0
                        except Exception:
                            has_events = False
                        
                        bg = "#FFD700" if is_today else (self.event_bg if has_events else self.cell_bg)
                        fg = self.text_color
                        
                        lbl = tk.Label(
                            mini_grid, text=str(day), font=day_font,
                            bg=bg, fg=fg, width=3, height=1, cursor="hand2"
                        )
                        # Make clickable to navigate to that month
                        lbl.bind("<Button-1>", 
                                lambda e, m=month_idx, d=day: self._goto_month(m, d))
                    
                    lbl.grid(row=r, column=c, sticky="nsew", padx=1, pady=1)
        
        # Configure grid weights
        for i in range(4):
            self.grid_frame.grid_columnconfigure(i, weight=1)
        for i in range(3):
            self.grid_frame.grid_rowconfigure(i, weight=1)
    
    def _goto_month(self, month, day):
        """Navigate to a specific month and day"""
        self.month = month
        self.day = day
        self.current_view = "month"
        self._switch_view("month")

    def _switch_view(self, view_type):
        """Switch between day, month, and year views"""
        self.current_view = view_type
        
        # Update button styling to show active view
        if view_type == "day":
            self.day_view_btn.config(bg=self.event_bg)
            self.month_view_btn.config(bg=self.cell_bg)
            self.year_view_btn.config(bg=self.cell_bg)
        elif view_type == "month":
            self.day_view_btn.config(bg=self.cell_bg)
            self.month_view_btn.config(bg=self.event_bg)
            self.year_view_btn.config(bg=self.cell_bg)
        else:  # year
            self.day_view_btn.config(bg=self.cell_bg)
            self.month_view_btn.config(bg=self.cell_bg)
            self.year_view_btn.config(bg=self.event_bg)
        
        self._refresh_view()
    
    def _refresh_view(self):
        """Refresh the current view"""
        if self.current_view == "day":
            self._draw_day()
        elif self.current_view == "month":
            self._draw_month()
        else:  # year
            self._draw_year()
    
    def _prev_period(self):
        """Navigate to previous period based on current view"""
        if self.current_view == "day":
            # Previous day
            current_date = date(self.year, self.month, self.day)
            from datetime import timedelta
            prev_date = current_date - timedelta(days=1)
            self.year = prev_date.year
            self.month = prev_date.month
            self.day = prev_date.day
        elif self.current_view == "month":
            # Previous month
            if self.month == 1:
                self.month = 12
                self.year -= 1
            else:
                self.month -= 1
        else:  # year
            # Previous year
            self.year -= 1
        self._refresh_view()

    def _next_period(self):
        """Navigate to next period based on current view"""
        if self.current_view == "day":
            # Next day
            current_date = date(self.year, self.month, self.day)
            from datetime import timedelta
            next_date = current_date + timedelta(days=1)
            self.year = next_date.year
            self.month = next_date.month
            self.day = next_date.day
        elif self.current_view == "month":
            # Next month
            if self.month == 12:
                self.month = 1
                self.year += 1
            else:
                self.month += 1
        else:  # year
            # Next year
            self.year += 1
        self._refresh_view()
