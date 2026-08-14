from datetime import datetime


class DashboardClock:

    def __init__(self, frame, clock_label):

        self.frame = frame

        self.clock_label = clock_label

    # ==========================
    # UPDATE CLOCK
    # ==========================

    def update(self):

        if not self.frame.winfo_exists():

            return

        now = datetime.now()

        self.clock_label.config(text=now.strftime("%A, %B %d, %Y | %I:%M:%S %p"))

        self.frame.after(1000, self.update)
