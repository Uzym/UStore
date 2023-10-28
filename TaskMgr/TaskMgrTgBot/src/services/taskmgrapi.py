from aiohttp import ClientSession


class TaskMgrApiService:
    def __init__(self, api_key):
        self.session = ClientSession()
        self.api_key = api_key
