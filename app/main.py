from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
import uuid

app = FastAPI()

class BuzzerManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []
        self.is_open = False
        self.winners = []  # 改為陣列，儲存前五名

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        await self.send_state(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast_state(self):
        state = {
            "type": "state",
            "is_open": self.is_open,
            "winners": self.winners
        }
        for connection in self.active_connections:
            try:
                await connection.send_json(state)
            except:
                pass

    async def send_state(self, websocket: WebSocket):
        try:
            await websocket.send_json({
                "type": "state",
                "is_open": self.is_open,
                "winners": self.winners
            })
        except:
            pass

manager = BuzzerManager()

# 參賽者畫面
@app.get("/")
async def get_user_page():
    with open("index.html", "r", encoding="utf-8") as f:
        return HTMLResponse(f.read())

# 主持人畫面
@app.get("/host")
async def get_host_page():
    with open("host.html", "r", encoding="utf-8") as f:
        return HTMLResponse(f.read())

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_json()
            action = data.get("action")
            
            if action == "buzz":
                user_name = data.get("user", "匿名參賽者")
                # 判斷：系統有開放 且 名額未滿5人 且 該使用者還沒搶過
                if manager.is_open and len(manager.winners) < 5 and user_name not in manager.winners:
                    manager.winners.append(user_name)
                    # 如果滿5人了，自動關閉搶答
                    if len(manager.winners) == 5:
                        manager.is_open = False
                    await manager.broadcast_state()
            
            elif action == "reset":
                manager.is_open = True
                manager.winners = []
                await manager.broadcast_state()
                
            elif action == "close":
                manager.is_open = False
                await manager.broadcast_state()

    except WebSocketDisconnect:
        manager.disconnect(websocket)