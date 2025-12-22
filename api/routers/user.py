from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def get_users():
    """取得所有使用者"""
    return {"users": []}

@router.post("/")
async def create_user(name: str, email: str):
    """建立新使用者"""
    return {"name": name, "email": email}

@router.get("/{user_id}")
async def get_user(user_id: int):
    """取得特定使用者資訊"""
    return {"user_id": user_id}
