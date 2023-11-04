from pydantic import BaseModel


class ResponseUploadFile(BaseModel):
    fileName: str

    def __str__(self):
        return f"fileName: {self.fileName}"
