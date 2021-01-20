# Notes


### Main Libs
   - FFmpeg : to split the video and audio AND to merge the video and audio
   - OpenCV : to process the video for Motion, Text, and Blur Detection
   - Wavelet : to process the audio for Audio De-nosing
   - pympeg : ffmpeg command generator
   - pmpi : python message passing interface, simple pipe communication
   - manager : prlimit to add constraints on the process using the os module

### Min Notes
   - FFT is very slow ```O(n)```
   - Wavelet Transform ```O(logn)```
   Wavelet will do the job, for de-noising
   FFmpeg will run inside subprocess module functions

### Need to build
   - Tools : FFmpeg helper, Cache, Logging, Image resizing, Exceptions, Non-max suppression, etc


-----------------------------------------------------------

# Logs

### Log 49, 20-01
```AP```
* Minor clean up
* Few bugs fixed
* Added set sar and dar ffmpeg
* Fixed process lock errors

----------------------------------------
### Log 48, 17-01
```AP```
* Minor clean up
* Few bugs fixed
* Integrated yacp
* Fixed thread errors
* Optimized imports

----------------------------------------
### Log 47, 16-01
```AP```
* Minor clean up
* Few bugs fixed
* Added thumbnail generation
* Fixed multi-channel audio issue
* Thinking of integrating yacp.

----------------------------------------
### Log 46, 13-01
```AP```
* Creating unit tests for each module
* Written multiple tests for timestamps, image, and video utils
* Clean up
* Discussed on the important activities

----------------------------------------
### Log 45, 12-01
```AP```
* Add the pmpi module
* Cleaned up all extra comm threads
* Replaced all pipe and queue communication with pmpi
* Benchmarking on small scale for pmpi done

----------------------------------------
### Log 44, 11-01
```AP```
* Added pympeg into the project
* Fixed the ffmpeg progress bar
* Constructed the ffmpeg command line to accept new changes
* Minor clean up and bug fixes

----------------------------------------
### Log 43, 06-01
```AP```
* Changed project structures
* Re thought on the file, function, var naming convection
* Created multiple nodes in pympeg 
* Further activities discussed.

----------------------------------------
### Log 42, 01-01
```AP```
* Started working on the ffmpeg wrapper
* Command line arguments can be designed using a graph
* Worked on signal to noise ratio calculations
* Further activities discussed.

----------------------------------------
### Log 41, 26-12
```AP```
* Process manager
* Setting niceness for the processes
* Manager pool : distribution of nice value
* Performance improvement, priority for other apps too

----------------------------------------
### Log 40, 24-12
```AP```
* Watcher subprocess - files
* Improved performance of the Watcher
* Added support for multi-channels audio denoising
* Clean ups and fail proof watcher

----------------------------------------
### Log 39, 21-12
```AP```
* Added new theme
* Clean ups
* Change border styles for widgets

----------------------------------------
### Log 38, 19-12
```AP```
* Theme management created
* Color management
* Theme selection in setting and config
* Added multiple themes

----------------------------------------
### Log 37, 17-12
```AP```
* Report completion
* Report content improvement
* Minor mistakes resolved

----------------------------------------
### Log 36, 11-12
```AP```
* Added settings page
* Connected the config and the page load
* Improved the ui for the main window
* Fixed clean up

----------------------------------------
### Log 35, 06-12
```AP```
* Solved few bugs
* Update analytics
* Changes to controller

----------------------------------------
### Log 34, 05-12
```AP```
* Completed the workbook, send it
* Updated the documents like reports
* Basic discussions on the sem report
* Started with the sem report

----------------------------------------
### Log 33, 01-12
```AP```
* Created widget for video display
* Use diff backend for matplot lib
* Checkbox connected
* Clean up

----------------------------------------
### Log 32, 29-11
```AP```
* Pipes needed to be create for slot connections
* Inter process communication completed
* Created pipes, queue, class communication between different components
* Changes matplot lib backend

----------------------------------------
### Log 31, 28-11
```AP```
* UI connection created
* Processing between two controllers designed
* Implemented few parts

----------------------------------------
### Log 30, 26-11
```AP```
* Started with ui
* Built basic ui
* Completed the ui structure
* Added assets cleaned up
* Added splash screen

----------------------------------------
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
