"""Static path information should be defined here"""
import pathlib


ROOT_DIR = pathlib.Path(__file__).parent.resolve()
LOGGING_PATH = str(ROOT_DIR.joinpath('logging.json'))
