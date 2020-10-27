# Torpido 
Improved version of Video Editing Automation
Goal : To automate the video editing process

* For more details documentation refer ```docs/```
* For dev logs refer [DEV LOGS](https://github.com/AP-Atul/Torpido/blob/master/logs)
---

## Working

```
- Start
- Accepts video from the user
- Reads the video [All processes below are parallel]

    - Processes the video stream for [Visual] :
        - Motion ranking, no motion will be ranked 0
        - Blur detection, blur detected ranked 0

    - Processes the video stream for [Textual] :
        - Text detection, high rank for text detected

    - Processes the audio stream for [Auditory] :
        - Audio de-noising with DWT & FWT
        - Audio activity ranking

- Calculate the sum of all ranks
- Select slices satisfying min rank
- Make trims to video using the ranks time stamps
- End
```

## Features

1. Motion detection ranking
2. BLur detection ranking
3. Audio de noising
4. Audio activity ranking / Silence detection
5. Text detection ranking

## Wavelet Transform 
Looking at performances, WT performs well and faster than SFT or FFT.
Note: Using WWavelet Transform to de noise, since the performance with FFT was very slow and memory consumption very high.
PyWaveletes is a great lib for using wavelets
Defaults: wavelet : db4; level : 1; mode = soft; method: per
