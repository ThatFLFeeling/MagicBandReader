import board
import neopixel
import time
import argparse
import logging
import sys
import threading
import RPi.GPIO as GPIO
sys.path.append('/home/pi/MFRC522-python')
from mfrc522 import SimpleMFRC522

# GPIO Pin
pixel_pin = board.D18

ring_pixels = 40
reverse_circle = bool(True)
log = logging.getLogger('main')
log.setLevel(logging.CRITICAL)

COLORS = {
    "green" : (255,0,0),
    "white" : (255,255,255),
    "errorBlue" : (179,60,247)
}

green = COLORS["green"]

class MagicBand():
    def __init__(self):
            self.RING_LIGHT_SIZE = 4
            self.total_pixels = ring_pixels
            self.ring_pixels = ring_pixels
            self.pixels = neopixel.NeoPixel(pixel_pin, self.total_pixels, brightness=1.0, pixel_order=neopixel.RGB)
            self.rdwr_commands = { }
            self.currentScan = 0
            self.reader = SimpleMFRC522()
            #Add valid MagicBand IDs inside []
            self.validIds = []
            self.scanThread = threading.Thread(target=self.scan)
            self.scanThread.start()
            self.playSequence(green)
            parser = ArgumentParser(
                    formatter_class=argparse.RawDescriptionHelpFormatter,
                    description="")
            
    def wheel(self, pos):
        if pos < 85:
             return (pos * 3, 255 - pos * 3, 0)
        elif pos < 170:
             pos -= 85
             return (255 - pos * 3, 0, pos * 3)
        else:
             pos -= 170
             return (0, pos * 3, 255 - pos * 3)
            
    def scan(self):
        while(True):
            id, _ = self.reader.read()
            print(id)
            self.currentScan = id
            
    def playStartupSequence(self):
            for x in range(0,3):
                self.do_lights_on(COLORS["white"])
                time.sleep(.5)
                self.do_lights_off()
                time.sleep(.5)

    def do_lights_on(self, color):
            for i in range(self.total_pixels):
                self.pixels[i] = color
            self.pixels.show()
            
    def do_lights_off(self):
            for i in range(self.total_pixels):
                self.pixels[i] = 0
            self.pixels.show()
            
    def playSequence(self, sequence):
        while(True):
            if (self.currentScan == 0):
                self.pixels.brightness = 1.0
                self.do_lights_circle_preScan(COLORS["white"], reverse_circle)
            elif (self.currentScan in self.validIds):
                self.do_lights_circle(COLORS["green"], reverse_circle)
                self.do_lights_on_fade(COLORS["green"])
                time.sleep(5)
                self.do_lights_off_fade() 
                self.pixels.brightness = 0
                self.currentScan = 0                
            else:
                self.do_lights_circle(COLORS["errorBlue"], reverse_circle)
                self.do_lights_on_fade(COLORS["errorBlue"])
                time.sleep(5)
                self.do_lights_off_fade() 
                self.pixels.brightness = 0
                self.currentScan = 0
    
    def do_lights_circle_preScan(self,color,reverse):
        self.color_chase(color,.03, reverse)
    
    def do_lights_circle(self,color,reverse):
        self.color_chase(color,.01, reverse)
        self.color_chase(color,.001, reverse)
        self.color_chase(color,.0001, reverse)
        self.color_chase(color,.00001, reverse)
        
        
            
    def do_lights_on_fade(self, color):
        for i in range(self.total_pixels):
            self.pixels[i] = color
        j = .01
        for x in range(100):
            j = j + .01
            self.pixels.brightness = j
            self.pixels.show()
            time.sleep(.001)
            
    def do_lights_off_fade(self):
        j = 1.01
        for x in range(100):
            j = j - .01
            self.pixels.brightness = j
            self.pixels.show()
            time.sleep(.0005)
        self.do_lights_off()
        
    def color_chase(self, color, wait, reverse):
        size = self.RING_LIGHT_SIZE
        for i in range(self.ring_pixels+size+1):
            for x in range(1, size):
                if (x+i) <= self.ring_pixels:
                    pixelNum = x + i
                    if reverse == True:
                        pixelNum = self.ring_pixels - (pixelNum - 1)
                    if pixelNum > 0 and pixelNum < self.ring_pixels:  
                        self.pixels[pixelNum] = color
            if (i > size) :
                off = (i-size)
                if reverse == True:
                    off = self.ring_pixels- (off - 1)
                if off > 0 and off < self.ring_pixels:                
                    self.pixels[off] = 0
            self.pixels.show()
            time.sleep(wait)
            
    def run(self):
            log.info('.')
                
class ArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        raise ArgparseError(self.prog, message)
    
class ArgparseError(SystemExit):
    def __init__(self, prog, message):
        super(ArgparseError, self).__init__(2, prog, message)

if __name__ == "__main__":
     try:
        MagicBand().run()
     except ArgparseError as e:
        print("exception")
        print(e)
        _prog = e.args[1].split()
     else:
        sys.exit(0)
