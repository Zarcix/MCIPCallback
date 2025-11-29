from datetime import datetime

class MinecraftState():
    player_list: list[str] = []
    tps: dict[str, str] = {}
    lastUpdated: datetime | None = None

    def asdict(self):
        return {
            "player_list": self.player_list,
            "tps": self.tps,
            "last_updated": self.lastUpdated
        }
