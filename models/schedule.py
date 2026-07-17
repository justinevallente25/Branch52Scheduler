class Schedule:

    def __init__(
        self,
        schedule_id,
        case_no,
        complainant,
        respondent,
        date,
        time,
        proceeding
    ):

        self.id = schedule_id
        self.case_no = case_no
        self.complainant = complainant
        self.respondent = respondent
        self.date = date
        self.time = time
        self.proceeding = proceeding


    def get_parties(self):

        return f"{self.complainant} vs {self.respondent}"


    def to_dict(self):

        return {

            "id": self.id,
            "case_no": self.case_no,
            "complainant": self.complainant,
            "respondent": self.respondent,
            "date": self.date,
            "time": self.time,
            "proceeding": self.proceeding

        }


    @staticmethod
    def from_dict(data):

        return Schedule(

            data["id"],
            data["case_no"],
            data["complainant"],
            data["respondent"],
            data["date"],
            data["time"],
            data["proceeding"]

        )