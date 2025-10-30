import state
from datetime import datetime, timedelta
from fastapi import FastAPI
from pydantic import BaseModel
import ipaddress 

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
        "healthy": mcHealth,
        "lastUpdated": currentState.lastUpdated.strftime("%d %B, %Y %H:%M:%S") if currentState.lastUpdated != None else None
    }

@app.patch("/update/")
async def update_info(newInfo: InfoPacket):
    def check_info():
        assert ipaddress.ip_address(newInfo.ip)

    check_info()
    currentState.currentIP = newInfo.ip
    currentState.lastUpdated = datetime.now()