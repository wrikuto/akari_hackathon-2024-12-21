from fastapi import FastAPI, WebSocket
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from starlette.responses import HTMLResponse
from user_data import engine, UserData, UserInfo
from sqlmodel import Session, select
import asyncio
import time
from finc_chatbot import chatbot

app = FastAPI()
user_data = UserData(user_id=4232, user_name="きよ")


# 静的ファイルをマウント
app.mount("/workspace/src/app/static", StaticFiles(directory="/workspace/src/app/static"), name="static")

# テンプレートの設定
templates = Jinja2Templates(directory="/workspace/src/app/templates")


@app.get("/")
async def get(request: Request):
    # テンプレートにリクエストを渡す
    return templates.TemplateResponse("index.html", {"request": request})



@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    await chatbot(websocket)

    # await websocket.accept()
    # await websocket.send_text("はじめまして。よろしくね!")


