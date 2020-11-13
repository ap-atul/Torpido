"""Maps the wavelet name to the Wavelet Class object"""

from torpido.wavelet.exceptions import WaveletImplementationMissing
from torpido.wavelet.wavelets import (db2, db3, db4, db5, db6, db7, db8, db9, db10,
                                      db11, db12, db13, db14, db15, db16, db17, db18, db19, db20,
                                      sym2, sym3, sym4, sym5, sym6, sym7, sym8, sym9, sym10,
                                      sym11, sym12, sym13, sym14, sym15, sym16, sym17, sym18, sym19, sym20,
                                      bior1_1, bior1_3, bior1_5, bior2_2, bior2_4,
                                      bior2_6, bior2_8, bior3_1, bior3_3, bior3_5,
                                      bior3_7, bior3_9, bior4_4, bior5_5, bior6_8,
                                      coif1, coif2, coif3, coif4, coif5,
                                      dmey, haar)

# all wavelets go here
wavelet = {
    "db2": db2.Daubechies2,
    "db3": db3.Daubechies3,
    "db4": db4.Daubechies4,
    "db5": db5.Daubechies5,
    "db6": db6.Daubechies6,
    "db7": db7.Daubechies7,
    "db8": db8.Daubechies8,
    "db9": db9.Daubechies9,
    "db10": db10.Daubechies10,
    "db11": db11.Daubechies11,
    "db12": db12.Daubechies12,
    "db13": db13.Daubechies13,
    "db14": db14.Daubechies14,
    "db15": db15.Daubechies15,
    "db16": db16.Daubechies16,
    "db17": db17.Daubechies17,
    "db18": db18.Daubechies18,
    "db19": db19.Daubechies19,
    "db20": db20.Daubechies20,
    "sym2": sym2.Symlet2,
    "sym3": sym3.Symlet3,
    "sym4": sym4.Symlet4,
    "sym5": sym5.Symlet5,
    "sym6": sym6.Symlet6,
    "sym7": sym7.Symlet7,
    "sym8": sym8.Symlet8,
    "sym9": sym9.Symlet9,
    "sym10": sym10.Symlet10,
    "sym11": sym11.Symlet11,
    "sym12": sym12.Symlet12,
    "sym13": sym13.Symlet13,
    "sym14": sym14.Symlet14,
    "sym15": sym15.Symlet15,
    "sym16": sym16.Symlet16,
    "sym17": sym17.Symlet17,
    "sym18": sym18.Symlet18,
    "sym19": sym19.Symlet19,
    "sym20": sym20.Symlet20,
    "haar": haar.Haar,
    "coif1": coif1.Coiflets1,
    "coif2": coif2.Coiflets2,
    "coif3": coif3.Coiflets3,
    "coif4": coif4.Coiflets4,
    "coif5": coif5.Coiflets5,
    "bior1.1": bior1_1.Biorthogonal11,
    "bior1.3": bior1_3.Biorthogonal13,
    "bior1.5": bior1_5.Biorthogonal15,
    "bior2.2": bior2_2.Biorthogonal22,
    "bior2.4": bior2_4.Biorthogonal24,
    "bior2.6": bior2_6.Biorthogonal26,
    "bior2.8": bior2_8.Biorthogonal28,
    "bior3.1": bior3_1.Biorthogonal31,
    "bior3.3": bior3_3.Biorthogonal33,
    "bior3.5": bior3_5.Biorthogonal35,
    "bior3.7": bior3_7.Biorthogonal37,
    "bior3.9": bior3_9.Biorthogonal39,
    "bior4.4": bior4_4.Biorthogonal44,
    "bior5.5": bior5_5.Biorthogonal55,
    "bior6.8": bior6_8.Biorthogonal68,
    "meyer": dmey.Meyer
}


def getWaveletDefinition(name):
    """
    Returns the wavelet class

    Parameters
    ----------
    name: str
        name of the wavelet

    Raises
    ------
    WaveletImplementationMissing
        missing wavelet implementation

    Returns
    -------
    object
        object of the wavelet
    """
    if name not in wavelet:
        raise WaveletImplementationMissing(WaveletImplementationMissing.__cause__)
    return wavelet[name]


def getAllWavelets():
    """
    Returns a list of all the implemented/stored wavelets

    Returns
    -------
    list
        list of all the wavelets
    """
    return list(wavelet.keys())
