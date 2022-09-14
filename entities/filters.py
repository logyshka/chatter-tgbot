import datetime

from entities import User
from database import admins

class IsUnbanned:

    def __init__(self, message):
        self.access = False
        if not message.from_user.username:
            self.access = False
        elif User.is_new(message.from_user.id) or message.from_user.id in admins:
            self.access = True
        else:
            user = User(message.from_user.id)
            try:
                if message.from_user.id == message.chat.id:
                    if user.banned_for < datetime.datetime.now():
                        self.access = True
            except:
                if message.from_user.id == message.message.chat.id:
                    if user.banned_for < datetime.datetime.now():
                        self.access = True

    def __call__(self, *args, **kwargs):
        return self.access

class IsAdmin:

    def __init__(self, message):
        self.access = False
        if message.from_user.id in admins:
            self.access = True

    def __call__(self, *args, **kwargs):
        return self.access
