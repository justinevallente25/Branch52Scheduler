# models/schedule.py


class Schedule:

    def __init__(
        self,
        schedule_id,
        case_no,
        complainant,
        respondent,
        date,
        time,
        proceeding,
        status="Pending",
        queue_position=0,
    ):

        self.id = schedule_id

        self.case_no = case_no

        self.complainant = complainant

        self.respondent = respondent

        self.date = date

        self.time = time

        self.proceeding = proceeding

        self.status = status

        self.queue_position = queue_position

    # ==========================
    # GET PARTIES
    # ==========================

    def get_parties(self):

        return f"{self.complainant} vs {self.respondent}"

    # ==========================
    # UPDATE DATA
    # ==========================

    def update(
        self, case_no, complainant, respondent, date, time, proceeding, status="Pending"
    ):

        self.case_no = case_no

        self.complainant = complainant

        self.respondent = respondent

        self.date = date

        self.time = time

        self.proceeding = proceeding

        self.status = status

    # ==========================
    # SET STATUS
    # ==========================

    def set_status(self, status):

        self.status = status

    # ==========================
    # SET QUEUE POSITION
    # ==========================

    def set_queue_position(self, queue_position):

        self.queue_position = queue_position

    # ==========================
    # CONVERT TO DICT
    # ==========================

    def to_dict(self):

        return {
            "id": self.id,
            "case_no": self.case_no,
            "complainant": self.complainant,
            "respondent": self.respondent,
            "date": self.date,
            "time": self.time,
            "proceeding": self.proceeding,
            "status": self.status,
            "queue_position": self.queue_position,
        }

    # ==========================
    # CREATE FROM DICT
    # ==========================

    @staticmethod
    def from_dict(data):

        return Schedule(
            data["id"],
            data["case_no"],
            data["complainant"],
            data["respondent"],
            data["date"],
            data["time"],
            data["proceeding"],
            data.get("status", "Pending"),
            data.get("queue_position", 0),
        )