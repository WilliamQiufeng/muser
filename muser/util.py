def grid(sw, sh, gw, gh, x, y):
    gridw = sw / gw
    gridh = sh / gh
    return (gridw * x, gridh * y)