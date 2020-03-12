from .common import *
from .dcinside import *

try:
    common.check_and_make_data_directories()
except:
    common.print_error(inspect.currentframe())

if __name__ == "__main__":
    pass