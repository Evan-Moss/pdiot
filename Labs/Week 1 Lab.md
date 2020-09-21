# Week 1 Lab

# Introduction

Welcome to the PDIoT course! You will experience the different facets of designing and implementing a complex IoT system, from specification to demonstration of a prototype implementation, over the course of 10 weeks (Coursework 3). The practical work will be complemented by knowledge gained through personal research on foundational topics in Internet of Things to be distilled in two 3000-word essays (Coursework 1 and 2).

Each student will be provided the following for Coursework 3:
* A wearable Respeck sensor for activity data collection.
* An mBed development board (NRF52-DK)
* A Nordic Cube
* The on-line ARM mBed compiler and software development environment.


This year, your task will be to implement a human activity recognition system for a range of common activities listed below by analysing data from a wearable sensor using machine learning techniques and displaying the results in real-time in an Android application.

The activities to be recognised are:
* Sitting/Standing
*	Lying down
*	Walking
*	Running/Jogging
*	Ascending and descending stairs
*	Desk work (working at a computer, writing, etc.)

You will first collect data using the Respeck sensor and store the data in a common repository. Please refer to the PDIoT Data Collection Protocol [document](https://github.com/specknet/pdiot-practical/blob/master/PDIoT%20Data%20Collection%20Protocol.pdf). Then, you will develop data analysis and machine learning methods for identifying the different types of activities. You will then be exposed to embedded programming concepts and you will establish a connection between the Nordic Cube and your Android App.

After this point, you will have a choice between:
* continuing with the machine learning development and concentrating on porting the algorithm on the phone for real-time HAR  
* continuing with embedded system development of the application in the Cube sensor

Use this week's tutorial to set up your development environment and to start collecting data.

# Git repository

A list of supporting files are available from the following GitHub [repository](https://github.com/specknet/pdiot-practical). In case the data collection app is missing after cloning visit this [repository](https://github.com/specknet/pdiotapp).

You are encouraged to use version control for your own work. A short tutorial on Git and Github can be found [here](https://www.freecodecamp.org/news/what-is-git-and-how-to-use-it-c341b049ae61/).

Start by cloning this repository:
1. Open the terminal app.
2. Navigate to the folder where you wish to have the files using the terminal.
3. Run ```git clone https://github.com/specknet/pdiot-practical.git``` to get the repo.
4. Type ```git submodule init``` and ```git submodule update``` to download the Android app as well.
4. Now all the files can be found in the "pdiot-practical" folder.

Alternatively you can download the files in the following way:
1. Go to the link above.
2. Click the "Clone or Download" button.
3. Select the "Download as ZIP.
4. Save and unarchive the file.
5. On the Github page click on "pdiotapp", which will take you to the code for the Android app.
6. Once on the "pdiotapp" page proceed similarly and download the files as zip.
7. Unarchive the files inside the "pdiot-practical" folder.
8. You should now have all the required files in their place.

# Data Analysis

### 1. If you don't already have it then Install conda
1. **Check you don't already have conda installed!**
    1. `which conda`
    2. **if you already have it installed, skip ahead to Create an Environment**
    3. It doesn't matter if you have miniconda3, or anaconda3 installed (it does not even matter if it is version 2).
2. If you don't have conda, download the latest version of miniconda3
    1. `cd ~/Downloads` (you can make a Downloads folder if you don't have one)
    2. Download the installer (we prefer to use miniconda since it carries less baggage), depending on your system (you can check links [here](https://conda.io/miniconda.html)):
        * Linux: `wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh`
        * Mac: `wget https://repo.continuum.io/miniconda/Miniconda3-latest-MacOSX-x86_64.sh` or ```curl -LOk https://repo.continuum.io/miniconda/Miniconda3-latest-MacOSX-x86_64.sh```
        * Or just simply download from [the site](https://conda.io/miniconda.html)
3. Install miniconda3 *with default settings*
    1. `bash Miniconda3-latest-Linux-x86_64.sh`
    2. Follow the prompt - **type `yes` and hit `enter` to accept all default
    settings when asked**
4. Close Terminal and reopen
5. Try executing `conda -h`. If it works, you can delete the installer
`rm ~/Downloads/Miniconda3-latest-Linux-x86_64.sh`

### 2. Create an environment for PDIoT
1. Update conda: `conda update conda`
2. Create the environment for the course. Call it pdiot and install python 3:
`conda create -n pdiot python=3.7`

### 3. Err...what's an environment?
An environment is a collection of packages of specific versions. You can have
multiple environments and switch between them for different projects. Conda is
a tool for managing both environments *and* the packages within each
environment. Here's a quick intro:

1. Show a list of your environments: `conda env list`
2. Print `$PATH`, one of your system's [environment variables](https://en.wikipedia.org/wiki/Environment_variable), in the
terminal: `echo $PATH`
    * `$PATH` is the list of directories your terminal can search to find
anything you execute:
3. Print a list of python installations on your `$PATH` (the top one is the one
    that will get executed if you type `python` in the terminal):
    `which python -a`
4. Activate the new environment: `source activate pdiot`
5. Show list of python installations on your system *now*: `which python -a`
6. Show your system `$PATH` again: `echo $PATH`
7. Deactivate the new environment: `source deactivate`
8. Observer how your $PATH has changed again: `echo $PATH`
9. Make an empty environment: `conda create --name empty`
10. You can clone environments; this is useful for backing up: `conda create
--name empty_bkp --clone empty`
11. Make another python 3 environment with numpy already installed: `conda create
--name py3 python=3.7 numpy`
12. `conda env list`
13. Activate py3: `source activate py3`
14. Show the installed packages: `conda list`
15. Switch environments: `source deactivate; source activate empty`
16. `conda list` to show packages (note that python and, crucially,
    [pip](https://pip.pypa.io/en/stable/) are not installed)
17. Q: What python would get used now? `which python` A: the conda root
environment installation of python i.e. *not* this environment's python.
18. Install numpy: `conda install numpy`
19. Q: What python would get used *now*? `which python` A: You may have clocked
that conda installed a dependency of numpy (a python package)...python!
20. Let's delete these test environments:
    * `source deactivate`
    * `conda env list`
    * `conda remove --name empty --all`
    * `conda remove --name empty_bkp --all`
    * `conda remove --name py3 --all`
    * `conda env list`

### 4. Recommended setup
* Conda environment with python 3.7
* Jupyter notebooks + [Numpy](https://docs.scipy.org/doc/numpy-1.17.0/numpy-user-1.17.0.pdf) + [Pandas](https://pandas.pydata.org/pandas-docs/stable/getting_started/10min.html) + [Matplotlib](https://matplotlib.org/tutorials/introductory/pyplot.html#sphx-glr-tutorials-introductory-pyplot-py) + [Tensorflow2](https://www.tensorflow.org/install).

# Android setup

## 1. If you don't already have it - Install Android Studio

It is recommended that you use Android Studio. The IDE can be downloaded from [here](https://developer.android.com/studio/).

## 2. Phone

We use Xiaomi Redmi 4A or 5A phones and can lend one if required. Other phones may work for the practical but there can be Bluetooth compatibility issues with other devices.

## 3. Testing the development environment and collecting data

In order to test that the environment has been set up properly, we will install the app on the phone and test to see if it receives data from the Respeck.

1. Open Android Studio
2. Open the pdiot project which has been downloaded along with the rest of the files
3. Connect the phone to the computer using a USB cable.
4. Press on the "Run App" button, which can be found in the top right-hand part of the Android Studio interface. This will compile the code and install the app on the phone.
5. Unlock the phone and open the app.
6. In the app, nevigate to the Connect Respeck activity, click Scan Respeck and scan the QR code on the back on your Respeck.
7. The app should automatically connect to your Respeck.
8. Go back to the main menu in the app, then to the Watch Live Processing page. You should now see live data coming from the Respeck.

## 9. Accessing the data
The data is saved directly to the storage of the phone.
To access it:

1. Connect the phone to your computer.
2. On the phone there should appear a popup/notification indicating that it has connected.
3. Tap on the notification, this will present you with three options: Charge this device; Transfer files, Transfer photos (PTP).
4. Select the Transfer files option.
5. In your file browser you should now be able to find the phone and browse the files.
6. The recorded files should be in the Internal Storage > Android > com.specknet.pdiotapp > files, but this might differ depending on the Android device you are using.
