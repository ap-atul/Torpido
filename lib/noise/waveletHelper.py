import pywt


def waveletLeafData(waveletPacket: pywt.WaveletPacket):
    """
    Extract wavelet coefficients from the signal

    Parameters
    ----------
    waveletPacket : object
        pywt wavelte bject

    Returns
    -------
    object
        output data
    """
    leafData = list()
    leafNodes = [node.path for node in waveletPacket.get_level(
        waveletPacket.maxlevel, 'freq')]

    for node in leafNodes:
        bandData = waveletPacket[node].data
        leafData.extend(bandData)

    return leafData
