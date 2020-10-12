# Week 4 Lab

# Introduction

This week we will introduce you to the mBed platform and development environment.

You will start programming the Nordic Cube using the NRF board as an interface. Your task will be to establish a connection between your app and the Nordic Cube using BLE. Note that the terms 'Thingy' and 'Nordic Cube' are used interchangeably throughout the tutorial.

# Installing the toolchain
You will need the following software to program and debug your cube:
* Git
* GNU ARM embedded toolchain
* make
* nRF Command Line Tools
* JLink

### Git
Install [git](https://git-scm.com/downloads), if you don't already have it, and use the default configurations.

### Obtain the Nordic Thingy FW repo
Clone the [Nordic Thingy FW](https://github.com/NordicSemiconductor/Nordic-Thingy52-FW) repo on your local machine. In the README file you will find similar instructions to what we have given you, however some instructions were out of date. Please try to follow this setup tutorial instead of the FW one.

### GNU Arm embedded toolchain
You can either use the recommended version for the nRF Cube (v4.9-2015q3) or install the latest version (v9.0-2020q2). Working with the newest version of the toolchain should not affect the code.

Download the toolchain from [here](developer.arm.com/tools-and-software/open-source-software/developer-tools/gnu-toolchain/gnu-rm/downloads). If you are working on macOS, you can install the toolchain via homebrew:
```bash
brew install homebrew/cask/gcc-arm-embedded
```

### Make
The make command should have been installed together with the gcc toolchain. Check it is correctly installed by running:
```bash
make --version
```

### nRF Command Line Tools & JLink
We will be using the nRF Command Line Tools for flashing the firmware and debugging the cube. You can obtain the files from [here](https://www.nordicsemi.com/Software-and-tools/Development-Tools/nRF-Command-Line-Tools/Download#infotabs). Select your operating system before downloading any package.

Note that you will have to install both CLTools and JLink. The installation instructions for each operating system are [here](https://infocenter.nordicsemi.com/index.jsp?topic=%2Fug_nrf5x_cltools%2FUG%2Fcltools%2Fnrf5x_command_line_tools_lpage.html).

Now you should be ready to run the firmware.

# Preparing the code
You will need to download the MPU Motion Driver from Invensense to be able to access the IMU on the cube.

### Downloading the motion driver
First, create a username on https://www.invensense.com/ and then navigate to the Downloads section. The Embedded Motion Driver should be listed as `eMD6.12`. Click on it to download. If for any reason you do not manage to create an account or if your request is not being approved, get in touch with Teo or Ilie through MS Teams, email or Piazza and they will provide the library for you.

### Setting up the repo with new folders
Please manually add the following folders to your Nordic-Thingy52-FW folder:
* `Nordic-Thingy52-FW/libs/libmpllib_Keil_M4FP`
* `Nordic-Thingy52-FW/libs/liblibmplmpu_m4_hardfp`

### Copying the relevant files
1. Unzip the downloaded `motion_driver_6.12` folder and navigate to `motion_driver_6.12/mpl libraries/arm/Keil`.
2. Unzip the folder `libmpllib_Keil_M4FP.zip` and copy the extracted library `libmpllib.lib` into `Nordic-Thingy52-FW/libs/libmpllib_Keil_M4FP`.
3. Finally, unzip `/motion_driver_6.12/mpl libraries/arm/gcc4.9.3/liblibmplmpu_m4_hardfp.zip` and copy the extracted library `liblibmplmpu.a` into the folder `Nordic-Thingy52-FW/libs/liblibmplmpu_m4_hardfp/`.

### Running the setup file
Open the terminal and navigate to the `Nordic-Thingy52-FW` folder. Run the `setup_sdk.sh` file.

You might get a permission denied error. In this case you need to allow the script to be executed by running:
```bash
chmod u+x setup_sdk.sh
```

Depending on which gcc embedded toolchain you chose to install, you might get errors related to the SDK. If you have installed the latest version of the toolchain and this happens, navigate to `Nordic-Thingy52-FW/external/sdk13/components/toolchain/gcc/Makefile.posix` and change the contents of the file to:
```bash
GNU_INSTALL_ROOT := /usr/local/Caskroom/gcc-arm-embedded/9-2020-q2-update/gcc-arm-none-eabi-9-2020-q2-update
GNU_VERSION := 9.0
GNU_PREFIX := arm-none-eabi
```
or replace the specific 2020 version with the version you have installed on your computer.

If you are running this on macOS Catalina, you will have to restart the installation multiple times and concurrently allow the programs to run from System Preferences > Security & Privacy and click the Allow Anyway button whenever a warning shows up.

# Connecting the hardware
You will need:
* The nRF52-DK board
* The Nordic Thingy52
* Debugging 10-pin cable
* A USB cable

### The Nordic Cube
First, take the cube out of the rubber case. There in an LED on the top left side of your cube which will light up blue when the cube is not connected, and green when it is connected (G).

![Image of cube from the top](https://github.com/specknet/pdiot-practical/blob/master/Images/cube_top.jpeg)

Make sure the cube is turned on by flipping the switch towards the closest edge of the cube (A). You will also see the USB input (B) which you can use for charging the cube, and the debug output (C).

![Image of cube from side](https://github.com/specknet/pdiot-practical/blob/master/Images/cube_side.jpeg)

### The board
The board is used as an interface between the cube and your computer. You will connect to the cube through a cable going into the Debug Out port (D). The USB port is used to connect the board to the computer (F). Finally, the power switch is shown in (E). Make sure the board is on whenever you plug it into the computer.

![Image of board](https://github.com/specknet/pdiot-practical/blob/master/Images/board_top.jpeg)

### Connection
Plug one end of the debug cable into the Nordic Cube and the other end into the Debug Out port of the board. Ensure that both are turned on. Then plug the USB cable into the board and connect it to the computer. You should see a `JLINK` drive appear on your desktop.

![Image of connections](https://github.com/specknet/pdiot-practical/blob/master/Images/board_usb.jpeg)

# Building the default firmware
To compile the default firmware, follow the instructions [here](https://nordicsemiconductor.github.io/Nordic-Thingy52-FW/documentation/firmware_compile.html).
1. Set up the path in makefile.windows or makefile.posix, depending on the platform you are using. The .posix file is used when working with Linux or macOS.
2. Open the makefile in a text editor.
3. Make sure that the GNU_INSTALL_ROOT variable points to your GNU Tools for Arm Embedded Processors directory. Example:
```bash
GNU_INSTALL_ROOT := $(PROGFILES)/GNU Tools ARM Embedded/4.9 2015q3 // Toolchain path
GNU_VERSION := 4.9.3
GNU_PREFIX := arm-none-eabi
```
You might be able to skip this if you have already changed the posix file before.
4. Navigate to the folder `Nordic-Thingy52-FW/project/pca20020_s132/armgcc`
5. Run the following command to compile the Thingy application code:
```bash
make -j
```
This will create a `_build` folder where all the compiled files live.
6. Run the following to reset the cube:
```bash
nrfjprog --eraseall
```
7. Next, run the following:
```bash
make flash_softdevice
make flash
```

Now the default code should be on the cube. You can verify it is working by turning of the nRF Connect App and trying to connect to your Thingy.

# Debugging
You will be able to use the nRF board to view the debug logs from the cube directly on your screen. For this you will be using the [nRF Logger Module](https://infocenter.nordicsemi.com/index.jsp?topic=%2Fcom.nordic.infocenter.sdk5.v15.2.0%2Flib_nrf_log.html&cp=4_0_0_3_26_0_1). You can see some example usages in the `Nordic-Thingy52-FW/project/pca20020_s132/main.c` file:

```c
NRF_LOG_INFO(NRF_LOG_COLOR_CODE_GREEN"=== Thingy started! ===\r\n");
```

You will need to enable logging by navigating to `Nordic-Thingy52-FW/project/pca20020_s132/config/sdk_config.h` and change the following on line 5530:
```c
#define NRF_LOG_ENABLED 1
```

You can also change the debug level on line 5599:
```c
#define NRF_LOG_DEFAULT_LEVEL 4
```
The file contains information about the log levels.

Once you add new logging statements to the code, make sure you are still in the armgcc folder and run:
```bash
make -j
make flash
```

The new code will be transferred to the cube.

To view the debug output, open up two separate terminal sessions.
In the first terminal window run:
```bash
jlink -device NRF52 -if SWD -speed 4000 -AutoConnect 1
```
or, if you are running on macOS:
```bash
jlinkexe -device NRF52 -f SWD -speed 4000 -AutoConnect 1
```
In the second terminal window, run:
```bash
jlinkrttclient
```

You should now be able to see the logs in the second terminal window.

# Task 1 - Adding a new debug statement
To first check that your cube is talking to the computer, add the following logging statement to your main.c file:
```c
NRF_LOG_INFO(NRF_LOG_COLOR_CODE_GREEN"=======Test=========\r\n");
```
Then recompile the code and check the debug output in your terminal window. You should see a continuous output of the test string, as it is being printed from an infinite loop.

# Task 2 - Changing the advertising name of your Thingy
Now we will change the cube's bluetooth name. Navigate to the `config/thingy_config.h` file and change the `DEVICE_NAME` to a string of your choice (max 10 characters).

We will need to erase the `_build` folder and the cube and flash it again.
Do the following while you are in the armgcc folder:
```bash
rm -rf _build
nrfjprog --eraseall
make -j
make flash_softdevice
make flash
```

Check your cube again using the nRF Connect App. The advertised name should now be your chosen string.  

# Task 3 - Logging the accelerometer values
We will now ask the cube to print out the new accelerometer values whenever it is receiving new ones.

Navigate to `Nordic-Thingy52-FW/source/drivers/drv_motion.c` and go to line 190. This is where the driver is getting the raw data from the accelerometer.

Under `valid_raw = true`, add the following logs:
```c
NRF_LOG_INFO(NRF_LOG_COLOR_CODE_GREEN"=== Accel x = %d ===\r\n", data[0]);
NRF_LOG_INFO(NRF_LOG_COLOR_CODE_GREEN"=== Accel y = %d ===\r\n", data[1]);
NRF_LOG_INFO(NRF_LOG_COLOR_CODE_GREEN"=== Accel z = %d ===\r\n", data[2]);
```

Rebuild the files and flash the firmware again:
```bash
rm -rf _build
nrfjprog --eraseall
make -j
make flash_softdevice
make flash
```

Now start your debug windows and connect to the cube through the nRF Connect app. You should see a screen enumerating the services offered by the cube:

![Image of services](https://github.com/specknet/pdiot-practical/blob/master/Images/nrf_connect_1.jpg)

Expand the `Thingy Motion Service` and find the `Thingy Raw Data Characteristic`.

![Image of characteristics](https://github.com/specknet/pdiot-practical/blob/master/Images/nrf_connect_2.jpg)

Click on the three arrows next to the name to subscribe to that characteristic:

![Image of subscription](https://github.com/specknet/pdiot-practical/blob/master/Images/nrf_connect_3.jpg)

You should now start to see the accelerometer values being printed into the output window on your screen.

# Task 4 - Connect the cube to your own Android App
Your task for next week will be to establish a connection between the cube and the Android App you were provided with (or your own app if you built something else).

For this, you will need to learn about [the packet format and characteristics](https://nordicsemiconductor.github.io/Nordic-Thingy52-FW/documentation/firmware_architecture.html) that the cube is using to send its data. You should focus on the Motion service.

The documentation also contains comprehensive APIs which you can use to access the drivers and the different modules of the cube. 
