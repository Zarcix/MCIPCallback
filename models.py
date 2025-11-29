from pydantic import BaseModel

class PlayerListPacket(BaseModel):
    ### Packet Structure ###
    # "HH:MM:SS [INFO] Connected players: Player1, Player2, Player3"
    ### Example ###
    # "08:07:39 [INFO] Connected players: Notch, Herobrine"
    player_list: str

class ServerTPSPacket(BaseModel):
    ### Packet Structure ###
    # "TIME:VAL TIME:VAL TIME:VAL"
    ### Example ###
    # "5s:20 30s:20 1m:20 5m:20 10m:20 15m:20"
    tps_list: str