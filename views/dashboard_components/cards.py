import tkinter as tk


class DashboardCards:

    def __init__(self, parent, manager, colors, open_page):

        self.parent = parent

        self.manager = manager

        self.open_page = open_page

        self.PRIMARY = colors["PRIMARY"]
        self.SECONDARY = colors["SECONDARY"]
        self.SUCCESS = colors["SUCCESS"]
        self.DANGER = colors["DANGER"]
        self.WARNING = colors["WARNING"]

        self.BACKGROUND = colors["BACKGROUND"]
        self.WHITE = colors["WHITE"]
        self.TEXT = colors["TEXT"]

        self.today_value = None
        self.upcoming_value = None
        self.total_value = None
        self.pending_value = None
        self.overdue_value = None
        self.calendar_value = None

    # ==========================
    # CREATE CARDS
    # ==========================

    def create(self, parent_frame):

        tk.Label(
            parent_frame,
            text="📋 Court Proceedings Overview",
            bg=self.BACKGROUND,
            fg=self.TEXT,
            font=("Segoe UI", 12, "bold"),
        ).pack(anchor="w", padx=30, pady=(20, 5))

        cards = tk.Frame(parent_frame, bg=self.BACKGROUND)

        cards.pack(fill="both", padx=30, pady=15)

        for i in range(3):

            cards.grid_columnconfigure(i, weight=1)

        self.today_value = self.create_card(
            cards, "📅 Today's", len(self.manager.get_today_cases()), self.SUCCESS
        )

        self.upcoming_value = self.create_card(
            cards, "🔔 Upcoming", len(self.manager.get_upcoming_cases()), self.SECONDARY
        )

        self.total_value = self.create_card(
            cards, "📂 Total Cases", self.manager.get_total_cases(), self.PRIMARY
        )

        self.pending_value = self.create_card(
            cards, "⏳ Pending", len(self.manager.get_pending_cases()), self.WARNING
        )

        self.overdue_value = self.create_card(
            cards, "⚠ Overdue", len(self.manager.get_overdue_cases()), self.DANGER
        )

        self.calendar_value = self.create_card(
            cards, "🗂 Records", len(self.manager.get_calendar_records()), "#6c5ce7"
        )

        return cards

    # ==========================
    # CREATE CARD
    # ==========================

    def create_card(self, parent, title, value, color):

        card = tk.Frame(
            parent, bg=self.WHITE, width=175, height=110, bd=1, relief="solid"
        )

        card.pack(side="left", padx=5)

        card.pack_propagate(False)

        card.bind("<Button-1>", lambda e: self.open_page(title))

        tk.Frame(card, bg=color, width=8).pack(side="left", fill="y")

        content = tk.Frame(card, bg=self.WHITE)

        content.pack(expand=True)

        tk.Label(
            content,
            text=title,
            bg=self.WHITE,
            fg=self.TEXT,
            font=("Segoe UI", 9, "bold"),
        ).pack(pady=(15, 5))

        label = tk.Label(
            content, text=value, bg=self.WHITE, fg=color, font=("Segoe UI", 24, "bold")
        )

        label.pack()

        label.bind("<Button-1>", lambda e: self.open_page(title))

        return label

    # ==========================
    # REFRESH CARDS
    # ==========================

    def refresh(self):

        self.today_value.config(text=len(self.manager.get_today_cases()))

        self.upcoming_value.config(text=len(self.manager.get_upcoming_cases()))

        self.total_value.config(text=self.manager.get_total_cases())

        self.pending_value.config(text=len(self.manager.get_pending_cases()))

        self.overdue_value.config(text=len(self.manager.get_overdue_cases()))

        self.calendar_value.config(text=len(self.manager.get_calendar_records()))
