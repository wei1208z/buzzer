from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from datetime import datetime

app = FastAPI()

class BuzzerManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []
        self.host_connection: WebSocket | None = None
        self.is_open = False
        self.winners = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        await self.send_state(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
        if self.host_connection == websocket:
            self.host_connection = None

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

@app.get("/")
async def get_user_page():
    with open("index.html", "r", encoding="utf-8") as f:
        return HTMLResponse(f.read())

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
            
            if action == "host_login":
                today_password = datetime.now().strftime("%Y%m%d")
                pwd = data.get("password")
                
                if pwd != today_password:
                    await websocket.send_json({"type": "login_result", "success": False, "msg": f"密碼錯誤！"})
                elif manager.host_connection is not None and manager.host_connection != websocket:
                    await websocket.send_json({"type": "login_result", "success": False, "msg": "登入失敗：目前已經有另一位主持人登入中！"})
                else:
                    manager.host_connection = websocket
                    await websocket.send_json({"type": "login_result", "success": True})
                    await manager.send_state(websocket)

            elif action == "buzz":
                user_name = data.get("user", "匿名參賽者")
                user_answer = data.get("answer", "未填寫答案")
                
                has_buzzed = any(w["name"] == user_name for w in manager.winners)
                
                if manager.is_open and not has_buzzed:
                    manager.winners.append({"name": user_name, "answer": user_answer})
                    await manager.broadcast_state()
            
            elif action in ["reset", "close"]:
                if manager.host_connection == websocket:
                    if action == "reset":
                        manager.is_open = True
                        manager.winners = []
                    elif action == "close":
                        manager.is_open = False
                    await manager.broadcast_state()

    except WebSocketDisconnect:
        manager.disconnect(websocket)