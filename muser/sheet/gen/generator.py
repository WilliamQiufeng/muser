from .rel_input import SourceSheetInput
import logger
import warnings


def gen_init():
    warnings.warn("Relative sheets are no longer supported", DeprecationWarning)
    process = SourceSheetInput(
        "/williamye/program/pyxel_projects/muser/test/test.data")
    process.process_all()
    logger.print(vars(process))
    logger.print(process.to_abs())
    logger.print("End")
