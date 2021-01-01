import logging
hd = logging.NullHandler()
logging.getLogger(__name__).addHandler(hd)
logger = logging
from .pokemon import *
from .enumparser import *
from .pokemondata import *

