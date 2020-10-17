# Torpido 
Improved version of Video Editing Automation
Goal : To automate the video editing process

* For more details documentation refer ```docs/```
* For dev logs refer [DEV LOGS](https://github.com/AP-Atul/Torpido/blob/master/logs)
---

## Working

1. Accept a video file in the input
2. Separate the video into video and audio
3. Perform ranking for all the features (visual, auditory, textual)
4. Perform de-noising on the audio
5. Finally calculate a max sub sequences from the ranks
6. Generate a timestamps for the sequences
7. Trim the video using the timestamps

## Features

1. Motion detection ranking
2. BLur detection ranking
3. Audio de noising
4. Audio activity ranking / Silence detection
5. Text detection ranking

## Notes

## FFT : Fast fourier tranform, mostly discrete fourier transform
* Time series to frequency domain

1. Most occurring signals are maximized after a FFT on the signal on the time and frequency sequence.

2. FFT: wraps the signal around the circle circumference, that rise the signals that occurs most.

3. Application in audio de noising:
- FFT will increase the power of the signal that occurs the most. Signals like talking, when in the talking audio, the most signal will be of person speaking. So FFT on such signal will give us only the speaker audio with great height.

- Then shifting the signal, we eliminate the low power signal, mostly noise, then inverse FFT will takes us back to original signal, only this time there would be no, noise.

4. Application in blur detection
- Similarly, most occurring data would be image data, if it is consistent we get a good sequence on the info, if we dont then image is classified as blurry.


Numpy has fft and ifft (much easier)
Librosa has stft and istft (short time fourier transform)
Opencv also has a laplacian method  (Hankel) (performs similar to FFT)

## Wavelet Transform 
Looking at performances, WT performs well and faster than SFT or FFT.
Note: Using WWavelet Transform to de noise, since the performance with FFT was very slow and memory consumption very high.
PyWaveletes is a great lib for using wavelets
Defaults: wavelet : db4; level : 1; mode = soft; method: per
