from pathlib import Path
import json


class GameState:
    def __init__(self,ai_game):
        self.settings = ai_game.settings
        #path = Path("highest.json")
        #contents = json.loads(path.read_text())
        #self.high_score = contents["highest"]
        self.high_score = 0
        self.reset_states()

    def reset_states(self):
        self.ship_left = self.settings.ship_limit
        self.score = 0