# controllers/schedule_manager.py

import json
import os
from datetime import datetime

from controllers.log_manager import LogManager

from models.schedule import Schedule


class ScheduleManager:

    def __init__(self):

        self.file = "data/schedules.json"

        self.schedules = []

        self.log_manager = LogManager()

        self.load()

    # ==========================
    # ADD SCHEDULE
    # ==========================

    def add(self, schedule):

        self.schedules.append(schedule)

        self.save()

        self.log_manager.add_log("ADD", f"Added case {schedule.case_no}")

    # ==========================
    # UPDATE SCHEDULE
    # ==========================

    def update(self, schedule_id, new_data):

        for schedule in self.schedules:

            if schedule.id == schedule_id:

                schedule.update(
                    new_data.case_no,
                    new_data.complainant,
                    new_data.respondent,
                    new_data.date,
                    new_data.time,
                    new_data.proceeding,
                    new_data.status,
                )

                self.log_manager.add_log("UPDATE", f"Updated case {schedule.case_no}")

        self.save()

    # ==========================
    # DELETE SCHEDULE
    # ==========================

    def delete(self, schedule_id):

        deleted_case = None

        for schedule in self.schedules:

            if schedule.id == schedule_id:

                deleted_case = schedule.case_no

        self.schedules = [s for s in self.schedules if s.id != schedule_id]

        self.save()

        self.log_manager.add_log("DELETE", f"Deleted case {deleted_case}")

    # ==========================
    # SEARCH
    # ==========================

    def search(self, keyword):

        result = []

        for s in self.schedules:

            text = (
                s.case_no + s.complainant + s.respondent + s.proceeding + s.status
            ).lower()

            if keyword.lower() in text:

                result.append(s)

        return result

    # ==========================
    # GENERATE ID
    # ==========================

    def generate_id(self):

        if not self.schedules:

            return 1

        return max(s.id for s in self.schedules) + 1

    # ==========================
    # SAVE
    # ==========================

    def save(self):

        os.makedirs("data", exist_ok=True)

        with open(self.file, "w") as f:

            json.dump([s.to_dict() for s in self.schedules], f, indent=4)

    # ==========================
    # LOAD
    # ==========================

    def load(self):

        if os.path.exists(self.file):

            with open(self.file, "r") as f:

                data = json.load(f)

                self.schedules = []

                for x in data:

                    if "status" not in x:

                        x["status"] = "Pending"

                    if "queue_position" not in x:

                        x["queue_position"] = 0

                    self.schedules.append(Schedule.from_dict(x))

    # ==========================
    # DASHBOARD FUNCTIONS
    # ==========================

    def get_total_cases(self):

        return len(self.schedules)

    def get_today_cases(self):

        today = datetime.now().strftime("%Y-%m-%d")

        return [
            s
            for s in self.schedules
            if s.date == today and s.status not in ["Completed", "Not Attended"]
        ]

    def get_upcoming_cases(self):

        today = datetime.now().strftime("%Y-%m-%d")

        return [s for s in self.schedules if s.date > today]

    def get_recent_cases(self, limit=5):

        return self.schedules[-limit:]

    # ==========================
    # STATUS FUNCTIONS
    # ==========================

    def get_pending_cases(self):

        return [s for s in self.schedules if s.status == "Pending"]

    def get_completed_cases(self):

        return [s for s in self.schedules if s.status == "Completed"]

    def get_cancelled_cases(self):

        return [s for s in self.schedules if s.status == "Cancelled"]

    def get_status_count(self, status):

        return len([s for s in self.schedules if s.status == status])

    # ==========================
    # ADVANCED DASHBOARD FUNCTIONS
    # ==========================

    def get_overdue_cases(self):

        now = datetime.now()

        overdue = []

        for s in self.schedules:

            if s.status in ["Completed", "Not Attended"]:

                continue

            try:

                schedule_date = datetime.strptime(s.date, "%Y-%m-%d")

                # ==========================
                # DATE ALREADY PASSED
                # ==========================

                if schedule_date.date() < now.date():

                    overdue.append(s)

                    continue

                # ==========================
                # SAME DAY TIME CHECK
                # ==========================

                if schedule_date.date() == now.date() and s.time:

                    try:

                        schedule_datetime = datetime.strptime(
                            f"{s.date} {s.time}", "%Y-%m-%d %I:%M %p"
                        )

                        if schedule_datetime < now:

                            overdue.append(s)

                    except ValueError:

                        continue

            except ValueError:

                continue

        return overdue

    def get_calendar_records(self):

        return [
            s
            for s in self.schedules
            if s.status in ["Completed", "Not Attended"]
        ]

    # ==========================
    # TODAY QUEUE
    # ==========================

    def get_today_queue(self):

        today = datetime.now().strftime("%Y-%m-%d")

        queue = [
            s
            for s in self.schedules
            if s.date == today
            and s.status not in ["Completed", "Not Attended"]
        ]

        queue.sort(
            key=lambda s: (
                s.queue_position if s.queue_position > 0 else 999999,
                s.time or "",
                s.id,
            )
        )

        return queue

    # ==========================
    # SKIP TODAY CASE
    # ==========================

    def skip_today_case(self, schedule_id):

        queue = self.get_today_queue()

        if not queue:

            return

        selected = None

        for s in queue:

            if s.id == schedule_id:

                selected = s

                break

        if not selected:

            return

        queue = [s for s in queue if s.id != schedule_id]

        queue.append(selected)

        for position, schedule in enumerate(queue, start=1):

            schedule.set_queue_position(position)

        self.save()

        self.log_manager.add_log(
            "QUEUE",
            f"{selected.case_no} moved to the back of today's queue",
        )

    # ==========================
    # UPDATE STATUS
    # ==========================

    def update_status(self, schedule_id, status):

        for s in self.schedules:

            if s.id == schedule_id:

                s.set_status(status)

                self.log_manager.add_log(
                    "STATUS",
                    f"{s.case_no} marked {status}",
                )

        self.save()