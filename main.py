from typing import Annotated
import state
import os
from datetime import datetime, timedelta
from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

currentState = state.MinecraftState()
secretKey = os.environ.get("SECRET_KEY", "1234")

class InfoPacket(BaseModel):
    player_list: str

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

@app.patch("/update/", status_code=200)
async def update_info(token: Annotated[str, Depends(oauth2_scheme)], newInfo: InfoPacket):
    if token != secretKey:
        raise HTTPException(
            status_code=401
        )

    # Prereq Checks
    assert type(newInfo.player_list) is str

    raw_player_string = newInfo.player_list
    player_string = raw_player_string.split("Connected players:")[1]
    player_list = list(filter(lambda n: n != "", [player.strip() for player in player_string.split(", ")]))
    print(f"Got Player List - '{player_list}'")

    currentState.player_list = player_list
    currentState.lastUpdated = datetime.now()
    return currentState