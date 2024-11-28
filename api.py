from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import json

# 創建 FastAPI 應用實例
app = FastAPI()

# 配置允許的來源
origins = [
    # "http://localhost:3000",  # 本地開發的前端
    # "http://127.0.0.1:3000",  # 本地開發的另一種形式
    # "https://your-frontend-domain.com",  # 部署後的前端域名
    "*",
]

# 添加 CORS 中間件
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # 允許的來源
    allow_credentials=True,  # 是否允許攜帶憑據（如 Cookie）
    allow_methods=["*"],  # 允許的 HTTP 方法，如 GET、POST 等，"*" 表示全部允許
    allow_headers=["*"],  # 允許的 HTTP 請求頭，"*" 表示全部允許
)


@app.get("/")
def read_root():
    return {"message": "Hello, World!"}



if __name__ == "__main__":
    print("啟動API服務器中...")
    # 記得允許防火墻開放端口：sudo ufw allow 8000
    import uvicorn

    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=False)