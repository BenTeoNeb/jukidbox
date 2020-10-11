#!/usr/bin/env python3
# Copyright 2017 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse
import time
import threading
from os import path, walk
import numpy
import alsaaudio

from aiy.board import Board
from aiy.voice.audio import AudioFormat
from aiy.leds import (Leds, Pattern, PrivacyLed, RgbLeds, Color)

import pygame
from pygame import mixer  # Load the popular external library

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--filename', '-f', default='recording.wav')
    args = parser.parse_args()

    leds = Leds()
    leds.pattern = Pattern.breathe(4000)
    leds.update(Leds.rgb_on((0, 8, 0)))

    pygame.init()
    pygame.mixer.init()

    mix = alsaaudio.Mixer() 
    mix.setvolume(30)

    # Files
    all_files=[]
    for (dirpath, dirnames, filenames) in walk('/home/pi/jukidbox_store'):
        all_files.extend([path.join(dirpath, file) for file in filenames])

    while True:
        leds.update(Leds.rgb_on((0, 8, 0)))
        try: 
            with Board() as board:
              while True:
                print('Press button to start.')
                board.button.wait_for_press()

                done = threading.Event()
                board.button.when_pressed = done.set

                print('Playing...')
                leds.update(Leds.rgb_pattern(Color.PURPLE))
                # Get random file
                file = numpy.random.choice(all_files)
                print(file) 
                pygame.mixer.music.load(file)
                pygame.mixer.music.play(-1)

                while mixer.music.get_busy(): 
                    if done.is_set():
                        leds.update(Leds.rgb_on((32, 0, 0)))
                        mixer.music.stop()
                    time.sleep(0.5) 

                print("Finished ..")
                leds.update(Leds.rgb_on((0, 8, 0)))
        except Exception as e:
            print(e) 
            leds.update(Leds.rgb_on(Color.YELLOW))
            time.sleep(2) 

if __name__ == '__main__':
    main()
