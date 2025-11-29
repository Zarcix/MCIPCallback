from typing import Annotated
import state
import os
from datetime import datetime, timedelta
from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordBearer

from models import (
    PlayerListPacket,
    ServerTPSPacket
)

currentState = state.MinecraftState()
secretKey = os.environ.get("SECRET_KEY", "1234")

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.get("/")
def read_root():
    player_list = currentState.player_list
    mcHealth = currentState.lastUpdated != None and (datetime.now() - currentState.lastUpdated) <= timedelta(minutes=1)
    return {
        "player_list": player_list,
        "healthy": mcHealth,
        "lastUpdated": currentState.lastUpdated.strftime("%d %B, %Y %H:%M:%S") if currentState.lastUpdated != None else None
    }

@app.patch("/update/player_list", status_code=200)
async def update_player_info(token: Annotated[str, Depends(oauth2_scheme)], newInfo: PlayerListPacket):
    if token != secretKey:
        raise HTTPException(
            status_code=401
        )

    # Prereq Checks
    if not "Connected players:" in newInfo.player_list: raise HTTPException(status_code=400, detail="Invalid Payload. Not a list of players.")

    raw_player_string = newInfo.player_list
    player_string = raw_player_string.split("Connected players:")[1]
    player_list = list(filter(lambda n: n != "", [player.strip() for player in player_string.split(", ")]))
    print(f"Got Player List - '{player_list}'")

    currentState.player_list = player_list
    currentState.lastUpdated = datetime.now()
    return currentState.player_list

@app.patch("/update/tps_list", status_code=200)
async def update_server_tps(token: Annotated[str, Depends(oauth2_scheme)], newInfo: ServerTPSPacket):
    if token != secretKey:
        raise HTTPException(
            status_code=401
        )

    print(f"Got TPS List - '{newInfo.tps_list}'")
    tps_list = list(filter(lambda n: n != "", newInfo.tps_list.split(" ")))
    if not tps_list:
        raise HTTPException(status_code=400, detail="Invalid TPS List. No TPS found in data.")

    currentState.tps.clear()
    for tps in tps_list:
        tps_interval, tps_value = tps.split(":")
        currentState.tps.update({tps_interval: tps_value})

    return currentState.tps
