from .rel_input import SourceSheetInput
import logger


def gen_init():
    process = SourceSheetInput(
        "/williamye/program/pyxel_projects/muser/test/test.data")
    process.process_all()
    logger.print(vars(process))
    logger.print(process.to_abs())
    logger.print("End")
