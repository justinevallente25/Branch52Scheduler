import json
import os



class SettingsManager:


    def __init__(self):

        self.file = "data/settings.json"

        self.settings = {}

        self.load()



    # ==========================
    # LOAD SETTINGS
    # ==========================


    def load(self):


        if os.path.exists(

            self.file

        ):


            with open(

                self.file,

                "r"

            ) as f:


                self.settings = json.load(f)



        else:


            self.settings = {


                "branch_name": "Branch 52",

                "office_name": "National Labor Relations Commission",

                "system_name": "Branch 52 Scheduler",

                "version": "1.0",

                "theme": "light",

                "backup_enabled": True

            }


            self.save()



    # ==========================
    # SAVE SETTINGS
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

                self.settings,

                f,

                indent=4

            )



    # ==========================
    # GET VALUE
    # ==========================


    def get(

        self,

        key

    ):


        return self.settings.get(

            key,

            ""

        )



    # ==========================
    # UPDATE VALUE
    # ==========================


    def update(

        self,

        key,

        value

    ):


        self.settings[key] = value


        self.save()