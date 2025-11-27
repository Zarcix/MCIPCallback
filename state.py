from datetime import datetime

class MinecraftState():
    player_list: list[str] = []
    tps: str = ""
    lastUpdated: datetime | None = None
