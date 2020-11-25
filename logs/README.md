# Notes


### Main Libs
   - FFmpeg : to split the video and audio AND to merge the video and audio
   - OpenCV : to process the video for Motion, Text, and Blur Detection
   - Wavelet : to process the audio for Audio De-nosing

### Min Notes
   - FFT is very slow ```O(n)```
   - Wavelet Transform ```O(logn)```
   Wavelet will do the job, for de-noising
   FFmpeg will run inside subprocess module functions

### Need to build
   - Tools : FFmpeg helper, Cache, Logging, Image resizing, Exceptions, Non-max suppression, etc


-----------------------------------------------------------

# Logs

### Log 29, 25-11
```AP```
* Moved ranking from files to cache
* Analytics improved
* Performance improvements
* testing small parts

----------------------------------------
### Log 28, 20-11
```AP```
* Completed SRS and looked into any corrections in Mathematical
* Discussed about some more features or improvements
* SRS correction and some changes

----------------------------------------
### Log 27, 13-11
```AP```
* Clean up
* Analytics improved
* Wavelets imported 
* SNR plots added

----------------------------------------
### Log 26, 12-11
```AP```
* Added plots to visualize the final ranks
* Plotting to visualize the timestamps
* Clean up
* Bug fix in io clean
* Analytics improvements

----------------------------------------
### Log 25, 07-11
```AP```
* Decided to use Cython for c extension
* Added type declaration for all parts of dwt and idwt
* Massive performance increased
* Compressor bug found and resolved [once cal of threshold]
* Pushed all code to repo

----------------------------------------
### Log 24, 06-11
```AP```
* Displayed the diagrams
* Lots of improvements required
* Starting new repo for wavelets to improve the performance
* Writing c extension for the WT

----------------------------------------
### Log 23, 04-11
```AP```
* Gave the Review 2
* Missing diagrams UMLs
* Started working on the UMLs
* Using draw.io
* Completed few UMLs diagram

----------------------------------------
### Log 22, 30-10
```AP```
* Discussion on Internal Review 2
* PPT Structure and agenda to discuss
* Wavelet Implementation going on 

----------------------------------------
### Log 21, 30-10
```AP```
* Bit clean up in wavelets
* Documentation updated
* Ancient decomposition added
* Other wavelets added
* Set up file added
* tests added to test basic stuffs

----------------------------------------
### Log 20, 27-10
```AP```
* Changed project folder name from lib -> torpido
* Made directory changes
* Organize the directory 
* Included init s to quick import stuffs
* Removed noise directory

----------------------------------------
### Log 19, 24-10
```AP```
* Added docs to wavelet
* Bit clean up
* Speed improvements required
* It works well or accurate

----------------------------------------
### Log 18, 23-10
```AP```
* Started implementing the Wavelets transform
* Discussed to add the DB and Coiflet or some others
* Main motive is to make it as fast as possible
* Thresholding needed to be decided
* Completed 1D and 2D wavelets
* FWT implemented

----------------------------------------
### Log 17, 21-10
```AP```
* Wrong error in videoGet, added Empty check
* Added EAST_MODEL to the env var
* Added extra validations
* Added custom exceptions
* Code clean ups

----------------------------------------
### Log 16, 17-10
```AP```
* Videos with no audio stream handling, skipping such videos for now
* Added custom exceptions
* Code clean ups

----------------------------------------
### Log 15, 07-10
```AP```
* Added abstraction
* Minor changes
* Started with class diagram
* Started with UI design

----------------------------------------
### Log 14, 02-10
```AP```
* Fixed Textual
* Improved performance
* Add one more function to image util

----------------------------------------
### Log 13, 01-10
```AP```
* Completed the Feasibility report
* Completed the Mathematical Model report
* Minor communication

----------------------------------------
### Log 12, 30-09
```SC```
* Updated the README.md for the project
* Add features and working of the project

-----------------------------------------
### Log 11, 30-09
```AP```
* Synopsis Review meeting conducted
* 16 -> 20 Sept, completed some diagrams and cleared all idea
* Created a feasibility and some info on trello
* Docs update and some more discussion
* Updated the logs to Github Wiki

------------------------------------------
### Log 10, 16-09
```AP```
* Wrote to Guide regarding the synopsis
* No updates on Synopsis
* Completed the task distribution
* Added task to create the UI layout -> MK

------------------------------------------
### Log 9, 25-08
```AP```
* Started creating the work distribution diagram
* Worked on some samples to start with the project
* Minor discussions
* 16 -> 25 Aug finalized the features for the project

------------------------------------------
### Log 8, 14-08
```AP```
* Wrote to Guide on confirmation and clearances on some topics
* Received confirmation and response on 15-08-20
* Feasibility study and diagram creation.

-------------------------------------------
### Log 7, 11-08
```AP```
* Created a system architecture diagram added to Trello
* Added tools and paper links on Trello
* Discussions on features to add

--------------------------------------------
### Log 6, 31-07
```AP```
* Synopsis Submission
* Papers sorted for the support of the project
* Added content on Trello

--------------------------------------------
### Log 5, 24-07
```AP```
* Idea Selection, result VEA
* Started searching for IEEE papers
* Added more content on Trello

--------------------------------------------
### Log 4, 20-07
```AP```
* Project idea evaluation
* More idea discussions
* Two ideas finalization
  * Video Editing Automation
  * Face Mask Detection

--------------------------------------------
### Log 3, 18-07
```AP```
* Created board on Trello
* Added Notes and Todo
* Added links to previous works and references

--------------------------------------------
### Log 2, 16-07
```AP```
* Short discussion on project ideas
* Decided the domains and basic tech

--------------------------------------------
### Log 1, 15-07
```AP```
* 15 July 2020, Project formed
* Placed all ideas
* Multiple ideas on the board
