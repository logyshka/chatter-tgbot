from database import promocodes
from datetime import timedelta
import pickle


class Promocode:

    def __init__(self, promocode):
        self.promo = promocode
        self._s = ["promocode", promocode]

    @property
    def is_valid(self):
        max_activations = promocodes.get(["activations_max"], self._s)
        if len(max_activations) > 0:
            max_activations = max_activations[0][0]
            if len(self.activations) < max_activations:
                return True
            return False
        return False

    @property
    def max_activations(self):
        return promocodes.get(["activations_max"], self._s)[0][0]

    @property
    def subscription_bonus(self):
        return promocodes.get(["subscription_bonus"], self._s)[0][0]

    @property
    def activations(self) -> list:
        return pickle.loads(promocodes.get(["activations"], self._s)[0][0])

    def activate(self, user_id):
        if self.is_valid:
            if user_id not in self.activations:
                bonus = self.subscription_bonus
                act = self.activations.copy()
                act.append(user_id)
                promocodes.set(["activations", pickle.dumps(act)],
                               self._s)
                if not self.is_valid:
                    promocodes.delete(self._s)
                return bonus
            return None
        return None

    @classmethod
    def create(cls, promocode, bonus, max):
        if not promocodes.get(["*"], ["promocode", promocode]):
            activations = pickle.dumps([])
            promocodes.insert({
                "promocode": promocode,
                "subscription_bonus": float(bonus),
                "activations_max": int(max),
                "activations": activations
            })
            print(activations)
            return promocode
        return False

    @classmethod
    def delete(cls, promocode):
        try:
            promocodes.delete(["promocode", promocode])
            return True
        except:
            return None

    @classmethod
    def get_all(cls):
        return promocodes.get_all()
