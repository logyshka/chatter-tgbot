import datetime
from database import users
from entities.conversation import Conversation, ConversationStatus, UserStatus
from entities.promocode import Promocode

class User:

    @classmethod
    def create(cls, user_id):
        users.insert({
            "user_id": user_id,
            "reg_date": datetime.date.today(),
            "conversation_id": 0,
            "banned_for": datetime.datetime.now(),
            "warnings": 1,
            "gender": "unknown",
            "reports": 0,
            "report_reason": "unknown",
            "likes": 0,
            "dislikes": 0,
            "subscription": datetime.datetime.now(),
            "refer": 0
        })

    def __init__(self, user_id):
        self.id = int(user_id)
        self._s = ["user_id", self.id]
        if self.is_new(user_id=self.id): self.create(user_id=self.id)

    @classmethod
    def is_new(cls, user_id):
        if users.get(["*"], ["user_id", user_id]):
            return False
        return True

    @property
    def refer(self):
        return users.get(["refer"], self._s)[0][0]

    @property
    def subscription(self):
        _subscription = datetime.datetime.fromisoformat(users.get(["subscription"], self._s)[0][0])
        if _subscription > datetime.datetime.now():
            return _subscription.replace(microsecond=0)
        return False

    @property
    def gender(self):
        return users.get(["gender"], self._s)[0][0]

    @property
    def reg_date(self):
        return datetime.date.fromisoformat(users.get(["reg_date"], self._s)[0][0])

    @property
    def interlocutor(self):
        if self.status == UserStatus.BUSY:
            conversation = Conversation(self.conversation_id)
            if conversation.user_id1 == self.id:
                return conversation.user_id2
            return conversation.user_id1
        return 0

    @property
    def banned_for(self):
        return datetime.datetime.fromisoformat(users.get(["banned_for"], self._s)[0][0])

    @property
    def conversation_id(self):
        return users.get(["conversation_id"], self._s)[0][0]

    @property
    def status(self):
        if self.conversation_id == 0:
            return UserStatus.FREE
        return UserStatus.BUSY

    @property
    def warnings(self):
        return users.get(["warnings"], self._s)[0][0]

    @property
    def reports(self):
        return users.get(["reports"], self._s)[0][0]

    @property
    def report_reason(self):
        return users.get(["report_reason"], self._s)[0][0]

    @property
    def likes(self):
        return users.get(["likes"], self._s)[0][0]

    @property
    def dislikes(self):
        return users.get(["dislikes"], self._s)[0][0]

    def set_refer(self, refer):
        users.set(["refer", refer], self._s)

    def get_subscription(self, during):
        users.set(["subscription", datetime.datetime.now() + datetime.timedelta(days=during)], self._s)

    def get_like(self):
        users.set(["likes", self.likes+1], self._s)

    def get_dislike(self):
        users.set(["dislikes", self.likes + 1], self._s)

    def get_report(self, report_reason):
        if self.report_reason == report_reason:
            users.set(["reports", self.reports + 1], self._s)
            if self.reports > 5:
                self.admin_get_warn(1 * self.reports)
        else:
            users.set(["reports", 1], self._s)
            users.set(["report_reason", report_reason], self._s)

    def set_gender(self, gender):
        users.set(["gender", gender], self._s)

    def admin_get_warn(self, during: float):
        users.set(["banned_for", datetime.datetime.now() + datetime.timedelta(hours=during)], self._s)

    def get_warn(self, during: float):
        during = during*self.warnings
        users.set(["banned_for", datetime.datetime.now() + datetime.timedelta(hours=during)], self._s)
        users.set(["warnings", self.warnings + 1], self._s)
        return during

    def get_ban(self):
        users.set(["banned_for", datetime.datetime.now() + datetime.timedelta(days=9999)], self._s)

    def get_unban(self):
        users.set(["banned_for", datetime.datetime.now()], self._s)

    def set_conversation(self, conversation_id):
        users.set(["conversation_id", conversation_id], self._s)

    def end_conversation(self):
        if self.status == UserStatus.BUSY:
            conversation = Conversation(self.conversation_id)
            if conversation.status == ConversationStatus.STARTED:
                conversation.set_end_time()
                User(self.interlocutor).set_conversation(0)
                self.set_conversation(0)
            elif conversation.status == ConversationStatus.WAITING:
                self.set_conversation(0)
                conversation.delete()


    def start_conversation(self, excepted_gender=False):
        if excepted_gender:
            conversation_id = Conversation.get_free_donate(self.gender, excepted_gender)
            if conversation_id:
                conversation: Conversation = Conversation(conversation_id)
                conversation.set_user_id2(self.id)
                self.set_conversation(conversation.id)
                return ConversationStatus.STARTED
            else:
                conversation: Conversation = Conversation.create(self.id, self.gender, excepted_gender)
                self.set_conversation(conversation.id)
                return ConversationStatus.WAITING
        else:
            conversation_id = Conversation.get_free(self.gender)
            if conversation_id:
                conversation: Conversation = Conversation(conversation_id)
                conversation.set_user_id2(self.id)
                self.set_conversation(conversation.id)
                return ConversationStatus.STARTED
            else:
                conversation: Conversation = Conversation.create(self.id, self.gender)
                self.set_conversation(conversation.id)
                return ConversationStatus.WAITING

    def activate_promocode(self, promocode):
        result = Promocode(promocode=promocode).activate(self.id)
        if result:
            self.get_subscription(round(result/24, 2))
            return result
        return None


    @classmethod
    def get_all(cls):
        return [i[0] for i in users.get_all()]