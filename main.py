import state
from datetime import datetime, timedelta
from fastapi import FastAPI
from pydantic import BaseModel  

currentState = state.MinecraftState()

class InfoPacket(BaseModel):
    ip: str

app = FastAPI()

@app.get("/")
def read_root():
    mcIP = currentState.currentIP
    mcHealth = currentState.lastUpdated != None and (datetime.now() - currentState.lastUpdated) <= timedelta(minutes=5)
    return {
        "ip": mcIP,
        "healthy": mcHealth
    }

@app.patch("/update/")
async def update_info(newInfo: InfoPacket):
    currentState.currentIP = newInfo.ip
    currentState.lastUpdated = datetime.now()