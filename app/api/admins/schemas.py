from app.api.users.schemas import UserBase


class AdminRequest(UserBase):
    class Config:
        orm_mode = True


class AdminResponse(UserBase):
    uid: str

    class Config:
        orm_mode = True


class AdminCreate(AdminResponse):
    class Config:
        schema_extra = {
            "example": {
                "uid": "123",
                "email": "a@mail.com",
                "username": "admin10",
            }
        }
