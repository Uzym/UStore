from aiohttp import ClientSession

class TaskMgrApiService:
    def __init__(self, api_key):
        self.session = ClientSession()
        self.api_key = api_key
        pass

    async def test(self):
        async with self.session.get(self.api_key + "/user") as res:
            result = await res.json()
            if res.status == 200:
                return result
            else:
                return {"ans": 0}


