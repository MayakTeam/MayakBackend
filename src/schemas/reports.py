from pydantic import BaseModel


class ReportCreateSchema(BaseModel):
    title: str
    author: str


class ReportGetSchema(BaseModel):
    id: int
    title: str
    author: str