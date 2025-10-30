import stat
from typing import Annotated
import state
import os
from datetime import datetime, timedelta
from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
import ipaddress 

currentState = state.MinecraftState()
secretKey = os.environ.get("SECRET_KEY", "1234")

class InfoPacket(BaseModel):
    ip: str

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

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
async def update_info(token: Annotated[str, Depends(oauth2_scheme)], newInfo: InfoPacket):
    if token != secretKey:
        raise HTTPException(
            status_code=401
        )
    def check_info():
        assert ipaddress.ip_address(newInfo.ip)

    check_info()
    currentState.currentIP = newInfo.ip
    currentState.lastUpdated = datetime.now()