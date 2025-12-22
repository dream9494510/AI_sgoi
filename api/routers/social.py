from fastapi import APIRouter

router = APIRouter()

@router.get("/posts")
async def get_posts():
    """取得社群貼文"""
    return {"posts": []}

@router.post("/posts")
async def create_post(user_id: int, content: str):
    """建立新貼文"""
    return {"user_id": user_id, "content": content}

@router.get("/posts/{post_id}")
async def get_post(post_id: int):
    """取得特定貼文"""
    return {"post_id": post_id}
