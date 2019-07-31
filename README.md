# Projektor
Video Playback with LSL markers for experiments that involve showing videos to subjects.
The LSL integration, sends the number of frames showed to the user at each moment.
## Installation
### Using Anaconda
1. Download and Install Anaconda from: https://www.anaconda.com/distribution/
2. Clone the repository in a directory:
```console
git clone https://github.com/NeoVand/Projektor.git
```
3. Create a python 3.7 environment by typing this command in the Anaconda Prompt (or any shell with conda in PATH):
```console
cd Projektor
conda create -n projektor python=3.7
```
4. Activate the recently made environment:
```console
conda activate projektor
```
5. Install the dependencies:
```console
pip install -r requirements.txt
```
## Organizing Video Files
The Video Files Should be organized in subfolders. Metadata files can be placed in the same folder with video files. ***Each folder must only inlude a single file.*** 
```console
 ───Video_Folder
    ├───Video1
    │       log1.log
    │       vid1.mp4
    │
    ├───Video2
    │       log2.log
    │       vid2.mp4
    │
    ├───Video3
    │       log3.log
    │       vid3.mp4
    │
    ├───Video4
    │       log4.log
    │       vid4.mp4
    .
    .
    .
```
## Running the program
To run the program, we should run `app.py` with 2 arguments. The first argument `--path` tells the program where to look for videos.The second one `--fr` asks for the frame-rate of the video.
```console
python app.py --path "<THE PATH TO THE ROOT OF THE VIDEO_FOLDER>" --fr <THE CORRECT FRAME RATE OF THE VIDEOS>
```
Now point your browser (Chrome or Firefox) to:
```console
http://127.0.0.1:5000/
```
### Setting a default path and frame-rate
To set a default path, change the `default_folder` variable to the desired path in app.py. The default value for `--fr` is set to 32.0.

