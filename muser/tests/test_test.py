import util


def test_util_grid():
    pos = util.grid(256, 256, 16, 16, 3, 3)
    assert pos == (48.0, 48.0)
    print(1)
