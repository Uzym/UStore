import logging

from odata import ODataService

import generated.taskmgr
from config import config
from src.services import TaskMgrApiService


class MyODataService(TaskMgrApiService):
    instance = None

    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super().__new__(cls)

        return cls.instance

    def __init__(self, api_key: str = None, logger: logging.Logger = None):
        super().__init__(api_key=api_key)
        self.logger = logger
        self.controller = "/OData/"
        logger.error(self.api_key)
        logger.error(self.controller)
        self.service = ODataService(
            url=self.api_key + self.controller,
            base=generated.taskmgr.ReflectionBase
        )
