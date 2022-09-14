import datetime
from database.creation import conversations
from entities.status import ConversationStatus, UserStatus

class Conversation:

    def __init__(self, conversation_id):
        self.id = float(conversation_id)
        self._s = ["conversation_id", self.id]

    @property
    def user_id1(self):
        return conversations.get(["user_id1"], self._s)[0][0]

    @property
    def user_id2(self):
        return conversations.get(["user_id2"], self._s)[0][0]

    @property
    def status(self):
        if self.user_id2 == 0:
            return ConversationStatus.WAITING
        elif not self.end_time:
            return ConversationStatus.STARTED
        return ConversationStatus.ENDED

    @property
    def start_time(self):
        return datetime.datetime.fromisoformat(conversations.get(["start_time"], self._s)[0][0])

    @property
    def end_time(self):
        _time = conversations.get(["end_time"], self._s)[0][0]
        return None if _time == 0 else datetime.datetime.fromisoformat(_time)

    @property
    def user_gender1(self):
        return conversations.get(["user_gender1"], self._s)[0][0]

    @property
    def gender_expected(self):
        return conversations.get(["gender_expected"], self._s)[0][0]

    @classmethod
    def create(cls, user_id1: int, user_gender1: str, gender_expected="none"):
        start_time = datetime.datetime.now()
        conversation_id = start_time.timestamp()
        conversations.insert({
                "conversation_id": conversation_id,
                "user_id1": user_id1,
                "user_id2": 0,
                "start_time": start_time,
                "end_time": 0,
                "user_gender1": user_gender1,
                "gender_expected": gender_expected
        })
        return Conversation(conversation_id)


    def delete(self):
        conversations.delete(self._s)
        del self


    def set_user_id2(self, user_id2):
        if self.user_id1 != user_id2:
            conversations.set(["user_id2", user_id2], self._s)

    def set_end_time(self):
        conversations.set(["end_time", datetime.datetime.now()], self._s)

    @classmethod
    def get_free(cls, seeker_gender) -> float:
        result = conversations.get(["*"], ["end_time", 0], ["gender_expected", seeker_gender], ["user_id2", 0])
        if len(result) != 0:
            return result[0][0]
        result = conversations.get(["*"], ["end_time", 0], ["gender_expected", "none"], ["user_id2", 0])
        if len(result) != 0:
            return result[0][0]
        return None

    @classmethod
    def get_free_donate(cls, seeker_gender, excepted_gender):
        result = conversations.get(["*"], ["end_time", 0], ["gender_expected", seeker_gender], ["user_id2", 0], ["user_gender1", excepted_gender])
        if len(result) != 0:
            return result[0][0]
        result = conversations.get(["*"], ["end_time", 0], ["gender_expected", "none"], ["user_id2", 0],
                                   ["user_gender1", excepted_gender])
        if len(result) != 0:
            return result[0][0]
        return None

    @classmethod
    def get_all(cls):
        return conversations.get_all()

