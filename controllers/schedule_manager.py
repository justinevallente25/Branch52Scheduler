import json
import os
from datetime import datetime

from models.schedule import Schedule



class ScheduleManager:


    def __init__(self):

        self.file = "data/schedules.json"
        self.schedules = []

        self.load()



    def add(self, schedule):

        self.schedules.append(schedule)

        self.save()



    def update(self, schedule_id, new_data):

        for schedule in self.schedules:

            if schedule.id == schedule_id:

                schedule.case_no = new_data.case_no
                schedule.complainant = new_data.complainant
                schedule.respondent = new_data.respondent
                schedule.date = new_data.date
                schedule.time = new_data.time
                schedule.proceeding = new_data.proceeding


        self.save()



    def delete(self, schedule_id):

        self.schedules = [

            s for s in self.schedules
            if s.id != schedule_id

        ]

        self.save()



    def search(self, keyword):

        result = []


        for s in self.schedules:

            text = (
                s.case_no +
                s.complainant +
                s.respondent +
                s.proceeding
            ).lower()


            if keyword.lower() in text:

                result.append(s)


        return result



    def generate_id(self):

        if not self.schedules:

            return 1


        return max(
            s.id for s in self.schedules
        ) + 1



    def save(self):

        os.makedirs(
            "data",
            exist_ok=True
        )


        with open(
            self.file,
            "w"
        ) as f:


            json.dump(

                [
                    s.to_dict()
                    for s in self.schedules
                ],

                f,

                indent=4
            )



    def load(self):

        if os.path.exists(self.file):

            with open(
                self.file,
                "r"
            ) as f:


                data = json.load(f)


                self.schedules = [

                    Schedule.from_dict(x)

                    for x in data

                ]



    # ==========================
    # DASHBOARD FUNCTIONS
    # ==========================


    def get_total_cases(self):

        return len(
            self.schedules
        )



    def get_today_cases(self):

        today = datetime.now().strftime(
            "%Y-%m-%d"
        )


        return [

            s for s in self.schedules

            if s.date == today

        ]



    def get_upcoming_cases(self):

        today = datetime.now().strftime(
            "%Y-%m-%d"
        )


        return [

            s for s in self.schedules

            if s.date > today

        ]



    def get_recent_cases(
        self,
        limit=5
    ):

        return self.schedules[-limit:]