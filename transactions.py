import argparse
import asyncio
import os

import dotenv

from pbl import PayByLinkAsync

dotenv.load_dotenv()

PBL_API_KEY = os.getenv("PBL_API_KEY")
PBL_DIVISION = os.getenv("PBL_DIVISION")

async def main() -> None:
    async with PayByLinkAsync(PBL_API_KEY) as pblapi:
        resp = await pblapi.get_transactions(PBL_DIVISION)
        for r in resp['transactions']:
            txid = r['id']
            txresp = await pblapi.get_transaction(PBL_DIVISION, txid)
            txstatus = txresp['transactions']['paymentRequest']['status']
            print(f"{txid} : {txstatus}")
        

if __name__ == "__main__":
    asyncio.run(main())