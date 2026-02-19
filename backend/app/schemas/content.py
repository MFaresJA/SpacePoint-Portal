from pydantic import BaseModel


class ContentItemOut(BaseModel):
    title: str
    url: str

    class Config:
        from_attributes = True


class ContentResponse(BaseModel):
    key: str
    items: list[ContentItemOut]
