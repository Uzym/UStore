import logging

from .store_api import StoreApiService
from src.models import s3
from pydantic.v1 import parse_raw_as
from typing import BinaryIO
from aiohttp import FormData
from aiogram.types import InputFile


class S3Service(StoreApiService):

    def __init__(self, api_key: str, logger: logging.Logger):
        super().__init__(api_key=api_key)
        self.logger = logger

    async def upload_file(self, file_path: str, file: BinaryIO) -> s3.ResponseUploadFile:
        url = self.api_key + "/upload"
        file_name = file_path.split('/')[-1].split('.')[0]
        extension = file_path.split('/')[-1].split('.')[-1]
        if extension == ".jpg" or extension == ".jpeg":
            content_type = "image/jpeg"
        elif extension == ".png":
            content_type = "image/png"
        else:
            content_type = "application/octet-stream"
        form_data = FormData()
        form_data.add_field(
            name="file",
            value=file,
            filename=f"{file_name}.{extension}",
            content_type=content_type,
        )
        async with self.session.post(url, data=form_data) as response:
            self.logger.info(response)
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
                return await response.read()

    async def delete_file(self, file_name: str) -> bool:
        url = self.api_key + "/remove"
        params = {
            "fileName": file_name
        }
        async with self.session.delete(url, params=params) as response:
            if response.status == 200:
                data = await response.read()
                return parse_raw_as(bool, data)
