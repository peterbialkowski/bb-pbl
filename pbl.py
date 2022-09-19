from enum import Enum

import aiohttp

class PaymentStatus(str, Enum):
    NEWREQUEST = "newRequest"
    CANCELLED = "cancelled"
    RECEIVED = "received"
    FAILED = "failed"
    AUTHORIZED = "authorized"
    PARTIALLYRECEIVED = "partiallyReceived"
    VOIDED = "voided"
    PENDING = "pending"

    def __str__(self):
        return str(self.value)

class PayByLinkAsync:

    def __init__(self, token: str, prod: bool = True, limit: int = 100):
        """Pay By Link API Wrapper Class

        Args:
            token (str): PBL API Key
            prod (bool, optional): Target production or sandbox environment. Defaults to True.
            limit (int, optional): Maximum number of concurrent connections to API host. Defaults to 100.
        """
        self._conn = aiohttp.TCPConnector(limit_per_host=limit)
        self._headers = {
                "Content-Type": "application/json; charset=utf-8",
                "authorization": f"Token {token}"
            }
        if prod:
            self.BASEURL = "https://api-gateway.tillpayments.com/paybylink" 
        else:
            self.BASEURL = "https://gateway.tillvision.show/paybylink"
        self.session = aiohttp.ClientSession(connector=self._conn, headers=self._headers)

    async def __aenter__(self):
        if not hasattr(self, 'session'):
            self.session = aiohttp.ClientSession(connector=self._conn, headers=self._headers)
        return self

    async def __aexit__(self, *err):
        await self.close()
        # self.session = None
    
    async def close(self):
        await self.session.close()

    async def paymentrequests(self, divisionid: str, **kwargs) -> list[dict]:
        """Endpoint to get paginated list of payment requests

        Required Args:
            divisionid (str): PBL Division ID

        Optional Args:
            ci (str): Customer ID
            da (str): Date created after `yyyy-mm-dd`
            db (str): Date created before `yyyy-mm-dd`
            aa (int): Amount above
            ab (int): Amount below
            rn (str): Reference number
            st (str | PaymentStatus): Status
            pt (str): Payment type
            pl (str): Page length
            pn (str): Page number

        Returns:
            list[dict]: List of all payment requests-paginated
        """
        url = self.BASEURL + f"/divisions/{divisionid}/paymentRequests/query"
        params = kwargs
        if kwargs.get('st'):
            params['st'] = str(kwargs['st'])
        response = await self.session.get(url=url, params=params)
        resp_json = await response.json()
        return resp_json

    async def get_transactions(self, divisionid: str, **kwargs) -> list[dict]:
        """Endpoint to get paginated list of transactions

        Required Args:
            divisionid (str): PBL Division ID

        Optional Args:
            ci (str): Customer ID
            cr (str): Currency
            da (str): Date created after `yyyy-mm-dd`
            db (str): Date created before `yyyy-mm-dd`
            aa (int): Amount above
            ab (int): Amount below
            rn (str): Reference number
            st (str | PaymentStatus): Status
            pt (str): Payment type
            pl (str): Page length
            pn (str): Page number

        Returns:
            list[dict]: List of all transactions-paginated
        """
        url = self.BASEURL + f"/divisions/{divisionid}/transactions/query"
        params = kwargs
        if kwargs.get('st'):
            params['st'] = str(kwargs['st'])
        response = await self.session.get(url=url, params=params)
        resp_json = await response.json()
        return resp_json
    
    async def paymentrequest(self, divisionid: str, paymentrequestid: str) -> dict:
        url = self.BASEURL + f"/divisions/{divisionid}/paymentRequests/{paymentrequestid}"
        params = {"includeRelations": "true"}
        response = await self.session.get(url=url, params=params)
        resp_json = await response.json()
        return resp_json

    async def get_transaction(self, divisionid: str, transactionid: str) -> dict:
        """Endpoint to get a transaction

        Args:
            divisionid (str): Division UUID
            transactionid (str): Transaction UUID

        Returns:
            dict: Details of the transaction requested
        """
        url = self.BASEURL + f"/divisions/{divisionid}/transactions/{transactionid}"
        response = await self.session.get(url=url)
        resp_json = await response.json()
        return resp_json