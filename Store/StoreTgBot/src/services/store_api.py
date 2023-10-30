from aiohttp import ClientSession


class StoreApiService:
    def __init__(self, api_key):
        self.session = ClientSession()
        self.api_key = api_key