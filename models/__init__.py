"""Pydantic 資料模型定義"""

from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    """使用者基礎模型"""
    name: str
    email: str

class UserCreate(UserBase):
    """建立使用者模型"""
    password: str

class User(UserBase):
    """使用者模型"""
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class DiaryEntry(BaseModel):
    """飲食紀錄模型"""
    id: int
    user_id: int
    food: str
    calories: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class DiaryCreate(BaseModel):
    """建立飲食紀錄模型"""
    food: str
    calories: int

class Post(BaseModel):
    """社群貼文模型"""
    id: int
    user_id: int
    content: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class PostCreate(BaseModel):
    """建立貼文模型"""
    content: str
