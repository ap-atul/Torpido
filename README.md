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
 
---

## Working

1. Read a video, separate the video and audio
2. Rank video frames
3. Rank audio frames
4. Create transcripts for the audio
5. Calculate final rank by combining all ranks
6. Select highest ranking sub sequence
7. Stitch back video and audio and display watch ability scores

 