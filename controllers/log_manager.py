import json
import os
from datetime import datetime



class LogManager:


    def __init__(self):

        self.file = "data/logs.json"

        self.logs = []

        self.load()



    # ==========================
    # ADD LOG
    # ==========================


    def add_log(
        self,
        action,
        details
    ):


        log = {


            "date": datetime.now().strftime(

                "%Y-%m-%d"

            ),


            "time": datetime.now().strftime(

                "%I:%M %p"

            ),


            "action": action,


            "details": details

        }



        self.logs.append(

            log

        )


        self.save()



    # ==========================
    # SAVE
    # ==========================


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

                self.logs,

                f,

                indent=4

            )



    # ==========================
    # LOAD
    # ==========================


    def load(self):


        if os.path.exists(

            self.file

        ):


            with open(

                self.file,

                "r"

            ) as f:


                self.logs = json.load(f)



    # ==========================
    # GET LOGS
    # ==========================


    def get_logs(self):

        return self.logs



    # ==========================
    # CLEAR LOGS
    # ==========================


    def clear_logs(self):


        self.logs = []


        self.save()