import argparse
import asyncio
import os

from aiohttp import ClientSession, ClientConnectionError
import dotenv

from pbl import PayByLinkAsync, PaymentStatus

dotenv.load_dotenv()

PBL_API_KEY = os.getenv("PBL_API_KEY")
PBL_DIVISION = os.getenv("PBL_DIVISION")
POSTBACK_URL = os.getenv("POSTBACK_URL")

async def postback_update(transaction_resp: dict) -> None:
    async with ClientSession() as s:
        try:
            _ = await s.post(url=POSTBACK_URL, json=transaction_resp)
        except ClientConnectionError as err:
            print(err)

async def monitor_multiple_payments() -> None:
    with open("paymentrequests.txt", "r") as file:
        payment_requests = file.read().splitlines()

    tasks = []
    for req in payment_requests:
        tasks.append(
            asyncio.ensure_future(
                monitor_payment_request(req, 10)
            )
        )

    return [await task for task in tasks]


async def monitor_payment_request(transactionid: str, refresh_time: int) -> None:
    async with PayByLinkAsync(PBL_API_KEY) as pblapi:
        while True:
            resp = await pblapi.paymentrequest(PBL_DIVISION, transactionid)
            status = resp['status']
            print(f"Transaction {transactionid}: {status}")
            if status == PaymentStatus.RECEIVED or status == PaymentStatus.CANCELLED:
                # Notify some external API and stop checking for this UUID
                await postback_update({"paymentReceived": True, "status": "ok"})
                break
            elif status == PaymentStatus.FAILED:
                # Do something else
                pass
                
            await asyncio.sleep(refresh_time)

if __name__ == "__main__":
    # asyncio.run(monitor_multiple_payments())
    parser = argparse.ArgumentParser()
    parser.add_argument("transactionid", type=str)
    parser.add_argument("-r", "--refresh", type=int, default=30, required=False)
    args = parser.parse_args()
    asyncio.run(monitor_payment_request(args.transactionid, args.refresh))