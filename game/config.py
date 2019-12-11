import game_config
class Config:
   SHEET_PATHS = [game_config.GLOB_CONFIG.assets.get("sheets/")]
   TOUCHED = [False for _ in range(4)]
