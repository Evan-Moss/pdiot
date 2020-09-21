# Week 3 Lab

# Introduction

This week we will introduce you to Android development and Bluetooth Low Energy (BLE). Your task will be to start using the [TFLite](https://www.tensorflow.org/lite) package to perform real-time human activity recognition on the mobile phone.

# Android
Your future Android app will interface to your wireless sensor (called the Cube) using Bluetooth LE and provide a user interface showing the activity prediction.

You already have access to a basic app which can be used to record sensor data for offline analysis. You are free to use this app as a starting point for your own application.

## 1. If you don't already have it - Install Android Studio

It is recommended that you use Android Studio. The IDE can be downloaded from [here](https://developer.android.com/studio/).

## 2. Phone

We use Xiaomi Redmi 4A or 5A phones and can lend one if required. Other phones may work for the practical but there can be Bluetooth compatibility issues with other devices. Please let the demonstrators know if your device is not working.

## 3. BLE Introduction

Bluetooth Low Energy (BLE) provides wireless communications for low power devices. Devices advertise one or more services, which themselves contain a number of characteristics. For example, a heart rate monitor may provide a service which contains a characteristic which will send the current pulse rate. Characteristics can either be readable, writable or allow notifications, which means that new data will be streamed over BLE when it is available. This is the mode that we use to send accelerometer and gyroscope data from the Cube.

The Nordic Semiconductor NRF Connect app (available on play/app store) will allow you to connect to BLE devices and interrogate the services and characteristics that they provide. It can also send/receive data and log communications to a file, which can be useful for debugging. Try this with the Cube to see how the sensor data is sent over BLE. Gyroscope, accelerometer and magnetometer data are packed into an 18-byte packet, where each axis of each sensor requires 2 bytes to send a 16-bit value.

## 4. BLE on Android

As mentioned previously, the repository contains the PDIoT data collection app, which you can use as an example of BLE communication on Android. We use the [RXAndroidBLE](https://polidea.github.io/RxAndroidBle) library which simplifies much of the communication code. Note that this requires Java 8 support (enabled in build.gradle as shown below).

build gradle:

```java
android {
        compileOptions {
            sourceCompatibility JavaVersion.VERSION_1_8
            targetCompatibility JavaVersion.VERSION_1_8
            }
}
```

## 7. Permissions

To make the data collection app work correctly, you&#39;ll need to enable _location_ and _storage_ permissions in _settings/apps/permissions_. Location permissions is required when scanning for BLE devices. If you don&#39;t have this you&#39;ll see a _BLE Scanning Error_ message when starting the app.

# More resources
Check out the following links for more information about:
* [Android development](https://developer.android.com/training/basics/firstapp)
* [TFLite for Android](https://www.tensorflow.org/lite/examples)
* [Bluetooth Low Energy](https://developer.android.com/guide/topics/connectivity/bluetooth-le)
* [More BLE](https://www.bluetooth.com/bluetooth-resources/intro-to-bluetooth-low-energy/)
