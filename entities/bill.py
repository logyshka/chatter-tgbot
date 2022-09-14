from pyqiwip2p.AioQiwip2p import AioQiwiP2P
from database import qiwi_secret_key, bills


class Bill:

    @classmethod
    async def create_bill(cls, amount, user_id, sub_name):
        async with AioQiwiP2P(qiwi_secret_key) as aio_qiwi:
            bill = await aio_qiwi.bill(amount=amount, comment="Покупка подписки", lifetime=7)
            s = bills.get(["bill_status"], ["user_id", int(user_id)])
            if s:
                for i in s:
                    if i[0] == "WAIT":
                        return False
            bills.insert({
                "user_id": user_id,
                "bill_id": bill.bill_id,
                "bill_amount": amount,
                "bill_status": "WAIT",
                "sub_during": sub_name
            })
            return bill

    @classmethod
    async def close_bill(cls, bill_id):
        async with AioQiwiP2P(qiwi_secret_key) as aio_qiwi:
            await aio_qiwi.reject(bill_id=bill_id)
            bills.delete(["bill_id", bill_id])

    @classmethod
    async def check_bill(cls, bill_id):
        async with AioQiwiP2P(qiwi_secret_key) as aio_qiwi:
            if (await aio_qiwi.check(bill_id)).status == "PAID":
                bills.set(["bill_status", "PAID"], ["bill_id", bill_id])
                return bills.get(["sub_during"], ["bill_id", bill_id])[0][0]
            return False

    @classmethod
    async def admin_complete(cls, bill_id):
        bills.set(["bill_status", "PAID"], ["bill_id", bill_id])
        return bills.get(["sub_during"], ["bill_id", bill_id])[0][0]