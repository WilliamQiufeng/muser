import game_config as game_config
import copy
from pyglet import media


class Config:
    SHEET_PATHS = [game_config.GLOB_CONFIG.assets.get("sheets")]
    TOUCHED = [False] * 16
    ARROW_COLORS_DEFAULT = [5] * 16
    ARROW_COLORS = copy.copy(ARROW_COLORS_DEFAULT)
    PLAYER: media.Player = media.Player()
    MOD_AUTO: bool = False

    @staticmethod
    def release_player():
        Config.PLAYER.pause()
        Config.PLAYER.delete()

    @staticmethod
    def set_all_arrow_colors(color: int):
        Config.ARROW_COLORS = [color] * 12

    @staticmethod
    def set_arrow_color(index: int, color: int):
        Config.ARROW_COLORS[index] = color
