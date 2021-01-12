![logo](https://github.com/AP-Atul/Torpido/blob/master/img/torpido.png)


## Table of Contents
* [Introduction](https://github.com/AP-Atul/Torpido#introduction)
* [How?](https://github.com/AP-Atul/Torpido#how-are-we-doing-this)
* [Which?](https://github.com/AP-Atul/Torpido#which-features-are-we-talking-about)
   * [Visual](https://github.com/AP-Atul/Torpido#1-visual)
   * [Auditory](https://github.com/AP-Atul/Torpido#2-auditory)
   * [Textual](https://github.com/AP-Atul/Torpido#3-textual)
* [Basic Working](https://github.com/AP-Atul/Torpido#basic-working)
* [Applications](https://github.com/AP-Atul/Torpido#applications)
* [Architecture](https://github.com/AP-Atul/Torpido#architecture)
* [Screen](https://github.com/AP-Atul/Torpido#screens)
* [Documentation](https://github.com/AP-Atul/Torpido#docs)
* [Execution](https://github.com/AP-Atul/Torpido#execution)

## Introduction
As we progress in this digital life concept, everyone tries to create contents plus they almost shoot
everything moreover they spend a whole lot of time in editing and making that content watchable.

This raw content requires a lot of cleaning and tuning to make the final output easy to understand and
contains highlights to regions of interest, which then can be posted on media sites like Youtube,
Instagram, Twitter, etc.

So we provide a solution to automate the task by using various methods to analyze audio and video
aspects of the raw video and generate a better and summarized output content, expected by any user.


## How are we doing this?
Automated summarization of digital Video Sequences is accomplished using a vector rank filter. The
output of the rank vector is determined by the minimum rank to be given to the input sequence. And the
selection of the max ranking subset which is continuous and satisfies the minimum ranking.

Each frame in a Video Segment can be ranked according to its feature significance. Using all these
features to generate a ranking vector for each such feature.

Applying filter on the final summation of all the ranked feature vectors to extract subsequences on the
vector.


## Which features are we talking about?
### 1. Visual 
#### Motion 
* Every video has some moments. Nobody wants to see an idle image as a video. So proposing
a motion feature ranking. The amount of motion determines the rank for the FRAME in the
sequence.
* The rank is set to 0 if the motion is below a certain threshold

#### Blur
* Determining the sharpness of the video FRAME, to rank the subsequence.
* If the sharpness is below a certain threshold ranking is set to 0.
----------------------
### 2. Auditory 
#### Audio energy
* Ranking the video sequence based on the audio activity i.e. talking, sound, music. etc.
* A certain threshold will determine whether to rank the sequence or not

#### De-noising
* Audio will be denoised using Wavelet Transform
----------------------
### 3. Textual
#### Text Detection
* Ranking the video sequence based on the text detected in the video
* If text is detected rank gets added or else 0 is added

#### EAST model
* The east model of the OpenCV will be used to detect the text in the video.


## Basic Working

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


## Applications

1. Automatic video editing for any video
2. Security footage extraction of importance parts
3. Tutoring video, with text detection and motion it can extract good amount
4. In general video editing
5. Audio de-noising of vlogging videos


## Architecture
![arch](https://github.com/AP-Atul/Torpido/blob/master/img/arch.png)


## Screens

![window](https://github.com/AP-Atul/Torpido/blob/master/img/window.png)

## Docs

For all docs visit [torpido](https://ap-atul.github.io/torpido/)

For dev logs visit [logs](https://github.com/AP-Atul/Torpido/tree/master/logs)

## Execution
* Install ffmpeg
```
$ sudo apt install ffmpeg
```

* Install all the dependencies
```
$ pip install -r requirements.txt
```

* Compile the cython files
```
$ python setup.py build_ext --inplace
```

* Download EAST model and add it to the path
```
$ wget  https://www.dropbox.com/s/r2ingd0l3zt8hxs/frozen_east_text_detection.tar.gz?dl=1
$ tar -xvf frozen_east_text_detection.tar.gz

// set environment variable
$ sudo gedit /etc/environment

// add new var
EAST_MODEL="path_to_frozen_east_text_detection.pb"

// test the var
$ echo $EAST_MODEL
```

* Run the run.py using some video file
```
$ python run.py /example/sample.mp4
```


