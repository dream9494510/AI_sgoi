from fastapi import FastAPI
from api.routers import user, diary, ai, social

app = FastAPI(title="飲食紀錄應用 API")

# 註冊路由
app.include_router(user.router, prefix="/api/users", tags=["users"])
app.include_router(diary.router, prefix="/api/diary", tags=["diary"])
app.include_router(ai.router, prefix="/api/ai", tags=["ai"])
app.include_router(social.router, prefix="/api/social", tags=["social"])

@app.get("/")
async def root():
    return {"message": "歡迎使用飲食紀錄應用 API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
