from pydantic import BaseModel


class TrainingType(BaseModel):
    name: str
    descr: str

    class Config:
        orm_mode = True
