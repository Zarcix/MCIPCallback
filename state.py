from datetime import datetime

class MinecraftState():
    player_list: list[str] = []
    tps: dict[str, str] = {}
    lastUpdated: datetime | None = None
