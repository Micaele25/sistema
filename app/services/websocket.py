from fastapi import WebSocket, WebSocketDisconnect, Depends
from sqlalchemy.orm import Session
import json
from app.database.db import get_db
from app.models.curso import Curso

active_connections = []

async def websocket_endpoint(websocket: WebSocket, db: Session = Depends(get_db)):
    await websocket.accept()
    active_connections.append(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        pass
    finally:
        if websocket in active_connections:
            active_connections.remove(websocket)
        await websocket.close()

async def notify_users(db: Session):
    cursos = db.query(Curso).all()
    message = json.dumps({"cursos": [{"id": c.id, "nome": c.nome, "descricao": c.descricao} for c in cursos]})
    for connection in active_connections:
        await connection.send_text(message)