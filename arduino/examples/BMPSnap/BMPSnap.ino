/*
BMPSnap.ino : grab a single frame and send it to host as a BMP file

Copyright (C) Simon D. Levy 2017

This file is part of BreezyArduCAM.

BreezyArduCAM is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

BreezyArduCAM is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with BreezyArduCAM.  If not, see <http://www.gnu.org/licenses/>.
*/

#include <Wire.h>
#include <BreezyArduCAM.h>
#include <SPI.h>

// set pin 10 as the slave select for the digital pot:
static const int CS = 7;

// btn pin
static const int btn_pin = 6;

Serial_ArduCAM_FrameGrabber fg;

/* Choose your camera */
ArduCAM_Mini_2MP myCam(CS, &fg);
//ArduCAM_Mini_5MP myCam(CS, &fg);

bool enabled = false;

void setup(void)
{

    pinMode(btn_pin, INPUT_PULLUP);

    // ArduCAM Mini uses both I^2C and SPI buses
    Wire.begin();
    SPI.begin();

    // Fastest baud rate (change to 115200 for Due)
    Serial.begin(921600);


    myCam.wrSensorReg8_8(0xff, 0x00);
    myCam.wrSensorReg8_8(0x7c, 0x00);
    myCam.wrSensorReg8_8(0x7d, 0x04);
    myCam.wrSensorReg8_8(0x7c, 0x09);
    myCam.wrSensorReg8_8(0x7d, 0x90);
    myCam.wrSensorReg8_8(0x7d, 0x00);

    // Begin capturing in  QVGA mode
    myCam.beginQvga();
}

void loop(void)
{
    if (digitalRead(btn_pin) == LOW) {
        enabled = !enabled;
        if (enabled) {
          Serial.println(F("capture enabled"));
        } else {
          Serial.println(F("capture disabled"));
        }
        delay(1000);
    }

    if (enabled) {
      myCam.capture();
    }
}