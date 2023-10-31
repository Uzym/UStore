import logging

from .store_api import StoreApiService
from src.models import s3
from pydantic import parse_raw_as


class S3Service(StoreApiService):

    def __init__(self, api_key: str, logger: logging.Logger):
        super().__init__(api_key=api_key)
        self.logger = logger

    async def upload_file(self, key: str, raw: bytes) -> s3.ResponseUploadFile:
        url = self.api_key + "/upload"
        body = {
            key: raw
        }
        async with self.session.post(url, data=body) as response:
            if response.status == 200:
                data = await response.json()
                return s3.ResponseUploadFile.parse_obj(data)

    async def download_file(self, file_name: str) -> bytes:
        url = self.api_key + "/download"
        params = {
            "fileName": file_name
        }
        async with self.session.post(url, params=params) as response:
            if response.status == 200:
                data = await response.read()
                return data

    async def delete_file(self, file_name: str) -> bool:
        url = self.api_key + "/remove"
        params = {
            "fileName": file_name
        }
        async with self.session.delete(url, params=params) as response:
            if response.status == 200:
                data = await response.read()
                return parse_raw_as(bool, data)
