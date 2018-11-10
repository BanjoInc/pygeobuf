from .encode import Encoder
from .decode import Decoder


def encode(*args):
    return Encoder().encode(*args)


def decode(*args):
    return Decoder().decode(*args)
