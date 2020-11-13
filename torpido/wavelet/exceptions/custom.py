"""All custom exceptions"""


class WaveletImplementationMissing(Exception):
    """
    This exception will be raised when unknown wavelet name is provided for
    transform object. When the wavelet implementation is missing
    """
    __cause__ = "The implementation for the requested wavelet is missing!"


class WaveletException(Exception):
    """
    This exception will be raised when something goes wrong with calculations
    or validations with message added at the runtime
    """
    pass


class WrongLengthsOfData(Exception):
    """
    This exception will be raised when any dimension length of data is not a
    power of 2, the solution to use the Ancient Egyptian with flatten will be
    indicated
    """
    __cause__ = "The length of the dimensions of data is not power of 2, use np.array(data).flatten()." \
                "Store the shape and reshape at the end"
