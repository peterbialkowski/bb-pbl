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

async def main(transactionid: str) -> None:
    async with PayByLinkAsync(PBL_API_KEY) as pblapi:
        while True:
            resp = await pblapi.get_transaction(PBL_DIVISION, transactionid)
            status = resp['transactions']['paymentRequest']['status']
            print(f"Transaction {transactionid}: {status}")
            if status == PaymentStatus.RECEIVED or status == PaymentStatus.CANCELLED:
                # Notify some external API and stop checking for this UUID
                await postback_update(resp)
                break
            elif status == PaymentStatus.FAILED:
                # Do something else
                pass
                
            await asyncio.sleep(30)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("transactionid", type=str)
    args = parser.parse_args()
    asyncio.run(main(args.transactionid))