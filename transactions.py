import asyncio
import os

import dotenv

from pbl import PayByLinkAsync, PaymentStatus

dotenv.load_dotenv()

PBL_API_KEY = os.getenv("PBL_API_KEY")
PBL_DIVISION = os.getenv("PBL_DIVISION")

async def main() -> None:
    async with PayByLinkAsync(PBL_API_KEY) as pblapi:
        resp = await pblapi.paymentrequests(PBL_DIVISION, da="2021-09-16", st=PaymentStatus.RECEIVED)
        for req in resp['paymentRequests']:
            reqid = req['id']
            reqresp = await pblapi.paymentrequest(PBL_DIVISION, reqid)
            txstatus = reqresp['status']
            print(f"{reqid} {txstatus}")
        

if __name__ == "__main__":
    asyncio.run(main())