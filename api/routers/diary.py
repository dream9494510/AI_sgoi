from fastapi import APIRouter
from typing import List

router = APIRouter()

@router.get("/")
async def get_diaries():
    """取得所有飲食紀錄"""
    return {"diaries": []}

@router.post("/")
async def create_diary(user_id: int, food: str, calories: int):
    """新增飲食紀錄"""
    return {"user_id": user_id, "food": food, "calories": calories}

@router.get("/{diary_id}")
async def get_diary(diary_id: int):
    """取得特定飲食紀錄"""
    return {"diary_id": diary_id}

@router.delete("/{diary_id}")
async def delete_diary(diary_id: int):
    """刪除飲食紀錄"""
    return {"deleted": diary_id}
