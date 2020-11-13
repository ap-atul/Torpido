""" Symlet 11 wavelet """


class Symlet11:
    """
    Properties
    ----------
     near symmetric, orthogonal, biorthogonal

    All values are from http://wavelets.pybytes.com/wavelet/sym11/
    """
    __name__ = "Symlet Wavelet 11"
    __motherWaveletLength__ = 22  # length of the mother wavelet
    __transformWaveletLength__ = 2  # minimum wavelength of input signal

    # decomposition filter
    # low-pass
    decompositionLowFilter = [
        0.00017172195069934854,
        -3.8795655736158566e-05,
        -0.0017343662672978692,
        0.0005883527353969915,
        0.00651249567477145,
        -0.009857934828789794,
        -0.024080841595864003,
        0.0370374159788594,
        0.06997679961073414,
        -0.022832651022562687,
        0.09719839445890947,
        0.5720229780100871,
        0.7303435490883957,
        0.23768990904924897,
        -0.2046547944958006,
        -0.1446023437053156,
        0.03526675956446655,
        0.04300019068155228,
        -0.0020034719001093887,
        -0.006389603666454892,
        0.00011053509764272153,
        0.0004892636102619239,
    ]

    # high-pass
    decompositionHighFilter = [
        -0.0004892636102619239,
        0.00011053509764272153,
        0.006389603666454892,
        -0.0020034719001093887,
        -0.04300019068155228,
        0.03526675956446655,
        0.1446023437053156,
        -0.2046547944958006,
        -0.23768990904924897,
        0.7303435490883957,
        -0.5720229780100871,
        0.09719839445890947,
        0.022832651022562687,
        0.06997679961073414,
        -0.0370374159788594,
        -0.024080841595864003,
        0.009857934828789794,
        0.00651249567477145,
        -0.0005883527353969915,
        -0.0017343662672978692,
        3.8795655736158566e-05,
        0.00017172195069934854,
    ]

    # reconstruction filters
    # low pass
    reconstructionLowFilter = [
        0.0004892636102619239,
        0.00011053509764272153,
        -0.006389603666454892,
        -0.0020034719001093887,
        0.04300019068155228,
        0.03526675956446655,
        -0.1446023437053156,
        -0.2046547944958006,
        0.23768990904924897,
        0.7303435490883957,
        0.5720229780100871,
        0.09719839445890947,
        -0.022832651022562687,
        0.06997679961073414,
        0.0370374159788594,
        -0.024080841595864003,
        -0.009857934828789794,
        0.00651249567477145,
        0.0005883527353969915,
        -0.0017343662672978692,
        -3.8795655736158566e-05,
        0.00017172195069934854,
    ]

    # high-pass
    reconstructionHighFilter = [
        0.00017172195069934854,
        3.8795655736158566e-05,
        -0.0017343662672978692,
        -0.0005883527353969915,
        0.00651249567477145,
        0.009857934828789794,
        -0.024080841595864003,
        -0.0370374159788594,
        0.06997679961073414,
        0.022832651022562687,
        0.09719839445890947,
        -0.5720229780100871,
        0.7303435490883957,
        -0.23768990904924897,
        -0.2046547944958006,
        0.1446023437053156,
        0.03526675956446655,
        -0.04300019068155228,
        -0.0020034719001093887,
        0.006389603666454892,
        0.00011053509764272153,
        -0.0004892636102619239,
    ]