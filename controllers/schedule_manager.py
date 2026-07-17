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
        



    def add(self, schedule):


        self.schedules.append(

            schedule

        )


        self.save()



        self.log_manager.add_log(

            "ADD",

            f"Added case {schedule.case_no}"

        )



    def update(
        self,
        schedule_id,
        new_data
    ):


        for schedule in self.schedules:


            if schedule.id == schedule_id:


                schedule.case_no = new_data.case_no
                schedule.complainant = new_data.complainant
                schedule.respondent = new_data.respondent
                schedule.date = new_data.date
                schedule.time = new_data.time
                schedule.proceeding = new_data.proceeding
                schedule.status = new_data.status


                self.log_manager.add_log(

                    "UPDATE",

                    f"Updated case {schedule.case_no}"

                )



        self.save()



    def delete(
        self,
        schedule_id
    ):


        deleted_case = None



        for schedule in self.schedules:


            if schedule.id == schedule_id:


                deleted_case = schedule.case_no



        self.schedules = [

            s for s in self.schedules

            if s.id != schedule_id

        ]



        self.save()



        self.log_manager.add_log(

            "DELETE",

            f"Deleted case {deleted_case}"

        )



    def search(self, keyword):

        result = []


        for s in self.schedules:

            text = (

                s.case_no +

                s.complainant +

                s.respondent +

                s.proceeding +

                s.status

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



                self.schedules = []



                for x in data:


                    # BACKWARD COMPATIBILITY
                    # Old records without status

                    if "status" not in x:

                        x["status"] = "Pending"



                    self.schedules.append(

                        Schedule.from_dict(x)

                    )





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





    # ==========================
    # STATUS FUNCTIONS
    # ==========================


    def get_pending_cases(self):

        return [

            s for s in self.schedules

            if s.status == "Pending"

        ]





    def get_completed_cases(self):

        return [

            s for s in self.schedules

            if s.status == "Completed"

        ]





    def get_cancelled_cases(self):

        return [

            s for s in self.schedules

            if s.status == "Cancelled"

        ]





    def get_status_count(self, status):

        return len(

            [

                s for s in self.schedules

                if s.status == status

            ]

        )