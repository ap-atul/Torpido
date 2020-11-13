cimport numpy as np
import numpy as np
cimport cython


from torpido.wavelet.wavelets import getWaveletDefinition


class WaveletTransform:
    def __init__(self, waveletName):
        self.w = getWaveletDefinition(waveletName)

    @cython.boundscheck(False)
    @cython.wraparound(False)
    def dwt(self, double[:] arrTime, int level):

        cdef double[:] decompHF = np.array(self.w.decompositionHighFilter)
        cdef double[:] decompLF = np.array(self.w.decompositionLowFilter)

        cdef np.ndarray arrHilbert = np.zeros(level)
        cdef double[:] arrHilbert_view = arrHilbert

        # shrinking value 8 -> 4 -> 2
        cdef int a = level >> 1
        cdef int i
        cdef int j
        cdef int k
        cdef int motherWaveletLength = self.w.__motherWaveletLength__

        for i in range(a):
            for j in range(motherWaveletLength):
                k = (i << 1) + j

                # circulate the array if scale is higher
                while k >= level:
                    k -= level

                # approx & detail coefficient
                arrHilbert_view[i] += arrTime[k] * decompLF[j]
                arrHilbert_view[i + a] += arrTime[k] * decompHF[j]

        return arrHilbert


    @cython.boundscheck(False)
    @cython.wraparound(False)
    def idwt(self, double[:] arrHilbert, int level):

        cdef double[:] reconLF = np.array(self.w.reconstructionLowFilter)
        cdef double[:] reconHF = np.array(self.w.reconstructionHighFilter)

        cdef np.ndarray arrTime = np.zeros(level)
        cdef double[:] arrTime_view = arrTime

        # shrinking value 8 -> 4 -> 2
        cdef int a = level >> 1
        cdef int i
        cdef int j
        cdef int k
        cdef int motherWaveletLength = self.w.__motherWaveletLength__

        for i in range(a):
            for j in range(motherWaveletLength):
                k = (i << 1) + j

                # circulating the array if scale is higher
                while k >= level:
                    k -= level

                # summing the approx & detail coefficient
                arrTime_view[k] += (arrHilbert[i] *  reconLF[j] +
                               arrHilbert[i + a] * reconHF[j])

        return arrTime
