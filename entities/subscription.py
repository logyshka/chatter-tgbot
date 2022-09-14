from database import subscriptions


class Subscription:

    def __create__(self, cost):
        if not subscriptions.get(["subscription_during"], self._s):
            subscriptions.insert({
                "subscription_name": self.name,
                "subscription_cost": cost,
                "subscription_during": self.during
            })

    def __init__(self, name, cost, during):
        self.name = name
        self.during = during
        self._s = ["subscription_name", self.name]
        self.__create__(cost=cost)

    def edit_subscription(self, cost):
        subscriptions.set(["subscription_cost", cost], self._s)

    @property
    def cost(self):
        return subscriptions.get(["subscription_cost"], self._s)[0][0]

DaySubscription = Subscription(name="day",
                               cost=15,
                               during=1)

WeekSubscription = Subscription(name="week",
                                cost=90,
                                during=7)

MonthSubscription = Subscription(name="month",
                                cost=300,
                                during=30)

ContainerSubscriptions = {
    "day": DaySubscription,
    "week": WeekSubscription,
    "month": MonthSubscription
}
