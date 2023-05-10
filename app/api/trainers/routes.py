from fastapi import APIRouter



router = APIRouter(tags=["plans"])


@router.get("/plans")
def create_user():
    return {"funciona": "bien"}



