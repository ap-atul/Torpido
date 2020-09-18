import pywt


def waveletLeafData(waveletPacket: pywt.WaveletPacket):
    leafData = list()
    leafNodes = [node.path for node in waveletPacket.get_level(
        waveletPacket.maxlevel, 'freq')]

    for node in leafNodes:
        bandData = waveletPacket[node].data
        leafData.extend(bandData)

    return leafData
