from database import users, conversations
import datetime


class Statistic:

    @classmethod
    def users_amount(cls):
        free_users = 0
        banned_users = 0
        _time = datetime.datetime.now()
        for i in users.get_all():
            if datetime.datetime.fromisoformat(i[3]) < _time:
                free_users += 1
            else:
                banned_users += 1
        all_users = free_users + banned_users
        return {
            "free_users": free_users,
            "banned_users": banned_users,
            "all_users": all_users
        }

    @classmethod
    def conversations_amount(cls):
        amount = 0
        total_during = 0
        for i in conversations.get_all():
            if i[4] != 0:
                amount += 1
                total_during += (datetime.datetime.fromisoformat(i[4]) - datetime.datetime.fromisoformat(i[3])).total_seconds()
        average_during = str(datetime.timedelta(seconds=round(total_during/amount, 2)))
        total_during = str(datetime.timedelta(seconds=round(total_during, 2)))
        return {
            "amount": amount,
            "average_during": average_during,
            "total_during": total_during
        }

