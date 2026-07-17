import json
import os
import holidays



class HolidayManager:


    def __init__(self):

        self.file = "data/holidays.json"

        self.custom_holidays = {}

        self.load()



    # ==========================
    # LOAD CUSTOM HOLIDAYS
    # ==========================


    def load(self):


        if os.path.exists(

            self.file

        ):


            with open(

                self.file,

                "r"

            ) as f:


                self.custom_holidays = json.load(f)



    # ==========================
    # SAVE CUSTOM HOLIDAYS
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

                self.custom_holidays,

                f,

                indent=4

            )



    # ==========================
    # CHECK HOLIDAY
    # ==========================


    def is_holiday(

        self,

        date

    ):


        year = int(

            date.split("-")[0]

        )


        # Philippine Holidays

        ph = holidays.PH(

            years=year

        )


        if date in ph:

            return True



        # Branch 52 Custom Holidays

        if date in self.custom_holidays:

            return True



        return False



    # ==========================
    # GET HOLIDAY NAME
    # ==========================


    def get_holiday_name(

        self,

        date

    ):


        year = int(

            date.split("-")[0]

        )


        ph = holidays.PH(

            years=year

        )



        if date in ph:


            return ph.get(

                date

            )



        if date in self.custom_holidays:


            return self.custom_holidays[date]



        return None



    # ==========================
    # ADD CUSTOM HOLIDAY
    # ==========================


    def add_holiday(

        self,

        date,

        name

    ):


        self.custom_holidays[date] = name


        self.save()



    # ==========================
    # REMOVE CUSTOM HOLIDAY


    def remove_holiday(

        self,

        date

    ):


        if date in self.custom_holidays:


            del self.custom_holidays[date]


            self.save()



    # ==========================
    # GET ALL HOLIDAYS
    # ==========================


    def get_all_holidays(

        self,

        year

    ):


        result = []



        ph = holidays.PH(

            years=year

        )


        for date, name in ph.items():


            result.append(

                {

                    "date": str(date),

                    "name": name

                }

            )



        for date, name in self.custom_holidays.items():


            result.append(

                {

                    "date": date,

                    "name": name

                }

            )



        return sorted(

            result,

            key=lambda x:x["date"]

        )