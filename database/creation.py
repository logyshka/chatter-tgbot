from database.main import Database

users = Database(table="users", _db_path=__file__.replace("creation.py", "db/users.db")).create_table({
    "user_id": "INT",
    "reg_date": "DATE",
    "conversation_id": "REAL",
    "banned_for": "TIME",
    "warnings": "INT",
    "gender": "TEXT",
    "reports": "INT",
    "report_reason": "TEXT",
    "likes": "INT",
    "dislikes": "INT",
    "subscription": "TIME",
    "refer": "INT"
})

conversations = Database(table="conversations", _db_path=__file__.replace("creation.py", "db/conversations.db")).create_table({
    "conversation_id": "REAL",
    "user_id1": "INT",
    "user_id2": "INT",
    "start_time": "TIME",
    "end_time": "TIME",
    "user_gender1": "TEXT",
    "gender_expected": "TEXT"
})

bills = Database(table="bills", _db_path=__file__.replace("creation.py", "db/bills.db")).create_table({
    "user_id": "INT",
    "bill_id": "TEXT",
    "bill_amount": "INT",
    "bill_status": "TEXT",
    "sub_during": "INT"
})

subscriptions = Database(table="subscriptions", _db_path=__file__.replace("creation.py", "db/subs.db")).create_table({
    "subscription_name": "TEXT",
    "subscription_cost": "INT",
    "subscription_during": "INT"
})

promocodes = Database(table="promocodes", _db_path=__file__.replace("creation.py", "db/promocodes.db")).create_table({
    "promocode": "TEXT",
    "subscription_bonus": "INT",
    "activations_max": "INT",
    "activations": "LIST"
})