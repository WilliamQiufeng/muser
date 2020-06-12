import game_config as game_config
import copy
class Config:
   SHEET_PATHS          = [game_config.GLOB_CONFIG.assets.get("sheets/")]
   TOUCHED              = [False] * 12
   ARROW_COLORS_DEFAULT = [5] * 12
   ARROW_COLORS         = copy.copy(ARROW_COLORS_DEFAULT)
   
   @staticmethod
   def set_all_arrow_colors(color: int):
      Config.ARROW_COLORS = [color] * 12
   @staticmethod
   def set_arrow_color(index: int, color: int):
      Config.ARROW_COLORS[index] = color
