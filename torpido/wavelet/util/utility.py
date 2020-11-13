"""Utility functions"""

from math import log, pow

import numpy as np

from torpido.wavelet.exceptions import WaveletException


def getExponent(value):
    """Returns the exponent for the data Ex: 8 -> 3 [2 ^ 3]"""
    return int(log(value) / log(2.))


def scalb(f, scaleFactor):
    """Return the scale for the factor"""
    return f * pow(2., scaleFactor)


def isPowerOf2(number):
    """Checks if the length is equal to the power of 2"""
    power = getExponent(number)
    result = scalb(1., power)

    return result == number


def decomposeArbitraryLength(number):
    """
    Returns decomposition for the numbers

    Examples
    --------
    number 42 : 32 + 8 + 2
    powers : 5, 3, 1
    """
    if number < 1:
        raise WaveletException("Number should be greater than 1")

    tempArray = list()
    current = number
    position = 0

    while current >= 1.:
        power = getExponent(current)
        tempArray.append(power)
        current = current - scalb(1., power)
        position += 1

    return tempArray[:position]


def threshold(data, value, substitute=0):
    """Soft thresholding"""

    magnitude = np.absolute(data)

    with np.errstate(divide='ignore'):
        # divide by zero okay as np.inf values get clipped, so ignore warning.
        thresholded = (1 - value / magnitude)
        thresholded.clip(min=0, max=None, out=thresholded)
        thresholded = data * thresholded

    if substitute == 0:
        return thresholded
    else:
        cond = np.less(magnitude, value)
        return np.where(cond, substitute, thresholded)


def mad(data):
    """
    Median Absolute Deviation: a "Robust" version of standard deviation.
    Indices variability of the sample.
    https://en.wikipedia.org/wiki/Median_absolute_deviation
    """
    data = np.ma.array(data).compressed()
    med = np.median(data)
    return np.median(np.abs(data - med))


def snr(data, axis=0, ddof=0):
    """
    Signal to Noise ratio
    Simply given by mean / standard deviation
    """
    with np.errstate(divide='ignore'):
        a = np.asanyarray(data)
        a = amp_to_db(a)
        m = a.mean(axis)
        sd = a.std(axis=axis, ddof=ddof)
        return np.where(sd == 0, 0, m / sd)


def amp_to_db(S, ref=1.0, min_value=1e-5, top_db=80.0):
    """
    Convert an amplitude spectrogram to dB-scaled spectrogram.

    This is equivalent to ``power_to_db(S**2)``

    Parameters
    ----------
    S : array_like
        input amplitude

    ref : scalar
        If scalar, the amplitude `abs(S)` is scaled relative to `ref`:
        `20 * log10(S / ref)`.
        Zeros in the output correspond to positions where `S == ref`.

    min_value : float > 0 [scalar]
        minimum threshold for `S` and `ref`

    top_db : float >= 0 [scalar]
        threshold the output at `top_db` below the peak:
        ``max(20 * log10(S)) - top_db``


    Returns
    -------
    S_db : np.ndarray
        ``S`` measured in dB
    """

    S = np.asarray(S)

    magnitude = np.abs(S)
    ref_value = np.abs(ref)

    power = np.square(magnitude, out=magnitude)

    return power_to_db(power, ref=ref_value ** 2, min_value=min_value ** 2,
                       top_db=top_db)


def power_to_db(S, ref=1.0, min_value=1e-10, top_db=80.0):
    """
    Convert a power spectrogram (amplitude squared) to decibel (dB) units

    This computes the scaling ``10 * log10(S / ref)`` in a numerically
    stable way.

    Parameters
    ----------
    S : np.ndarray
        input power

    ref : scalar
        If scalar, the amplitude `abs(S)` is scaled relative to `ref`:
        `10 * log10(S / ref)`.
        Zeros in the output correspond to positions where `S == ref`.

    min_value : float > 0 [scalar]
        minimum threshold for `abs(S)` and `ref`

    top_db : float >= 0 [scalar]
        threshold the output at `top_db` below the peak:
        ``max(10 * log10(S)) - top_db``

    Returns
    -------
    S_db   : np.ndarray
        ``S_db ~= 10 * log10(S) - 10 * log10(ref)``
    """

    S = np.asarray(S)

    if min_value <= 0:
        raise Exception('min must be strictly positive')

    if np.issubdtype(S.dtype, np.complexfloating):
        magnitude = np.abs(S)
    else:
        magnitude = S

    ref_value = np.abs(ref)

    log_spec = 10.0 * np.log10(np.maximum(min_value, magnitude))
    log_spec -= 10.0 * np.log10(np.maximum(min_value, ref_value))

    # scaling based on the top db
    if top_db is not None:
        if top_db < 0:
            raise Exception('top_db must be non-negative')
        log_spec = np.maximum(log_spec, log_spec.max() - top_db)

    return log_spec
