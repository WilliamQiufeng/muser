if __name__ == '__main__':
    import pyxel
    import game_config as game_config
    pyxel.init(256, 256,
               caption="Muser", scale=48)
    print("Window loaded")
    pyxel.load(f"{game_config.GLOB_CONFIG.assets.root}/resources.pyxres")
    print("Res loaded")
    from game import *
    from game import muser

