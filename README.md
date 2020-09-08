# Torpido 
Improved version of Video Editing Automation
Goal : To automate the video editing process

---

## Project Structure

    .
    ├── ...
    ├── lib                 
    │   ├── utils   
    │   │   ├── constants.py  
    │   │   ├── video_reader.py  
    │   ├── visual.py 
    │   └── ...                 
    └── ...


 * lib : contains all the libraries to handle video features (visual / auditory / textual)
 * lib/util : helper files 
 * constants : constants config for every operations
 * model : saved a trained model
 
---

## Working

1. Read a video, separate the video and audio
2. Rank video frames
3. Rank audio frames
4. Create transcripts for the audio
5. Calculate final rank by combining all ranks
6. Select highest ranking sub sequence
7. Stitch back video and audio and display watch ability scores

## Features

1. Motion detection ranking
2. BLur detection ranking
3. Audio de noising
4. Audio activity ranking / Silence detection
5. Text detection ranking
6. Transcript generation (not confirmed)

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

Note: Using WWavelet Transform to de noise, since the performance with FFT was very slow and memory consumption very high.
PyWaveletes is a great lib for using wavelets
Defaults: wavelet : db4; level : 1; mode = soft; method: per
