import argparse
import asyncio
import os

import dotenv

from pbl import PayByLinkAsync

dotenv.load_dotenv()

PBL_API_KEY = os.getenv("PBL_API_KEY")
PBL_DIVISION = os.getenv("PBL_DIVISION")

async def main(transactionid: str) -> None:
    async with PayByLinkAsync(PBL_API_KEY) as pblapi:
        while True:
            resp = await pblapi.get_transaction(PBL_DIVISION, transactionid)
            status = resp['transactions']['paymentRequest']['status']
            print(f"Transaction {transactionid}: {status}")
            if status == "received" or status == "cancelled":
                # Notify some external API
                break
            else:
                await asyncio.sleep(30)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("transactionid", type=str)
    args = parser.parse_args()
    asyncio.run(main(args.transactionid))