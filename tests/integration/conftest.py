import pathlib
import sys

PATH = pathlib.Path(__file__).parent.parent.parent.resolve()
sys.path.insert(0, str(PATH))
