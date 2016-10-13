# -*- coding: utf-8 -*-
"""
@author:
Jackson Cagle
"""

import os
import sys
import time
os.environ['PYSDL2_DLL_PATH'] = '.\\SDL2\\x86'

import ctypes
from sdl2 import *
import sdl2.sdlimage
import sdl2.ext

import threading
from collections import defaultdict

RESOURCES = sdl2.ext.Resources(__file__, "resources")

class textureDefinition:
    def __init__(self, x, y, w, h, angle):
        self.dst = sdl2.rect.SDL_Rect(x-w/2,y-h/2,w,h)
        self.angle = angle
    
    def rotate(self, angle):
        self.angle = angle
    
    def translate(self, x, y):
        self.dst.x = x-w/2
        self.dst.y = y-h/2
        
    def resize(self, decrease):
        self.dst.x -= decrease
        self.dst.w += decrease
    
class renderingThread(threading.Thread):

    

    def __init__(self):
        sdl2.ext.init()
        self.window = sdl2.ext.Window("Rocket Demo", size=(1280,720))
        self.window.show()        
        self.renderer = SDL_CreateRenderer(self.window.window, -1, SDL_RENDERER_ACCELERATED | SDL_RENDERER_PRESENTVSYNC)
        
        self.background = sdl2.sdlimage.IMG_LoadTexture(self.renderer, RESOURCES.get_path("Background.png"))
        self.background_def = textureDefinition(1280/2, 720/2, 1280, 720, 0)
        
        self.rocket = sdl2.sdlimage.IMG_LoadTexture(self.renderer, RESOURCES.get_path("Rocket.png"))
        self.rocket_def = textureDefinition(1280/2, 400, 30, 100, 0)

        self.shading = sdl2.sdlimage.IMG_LoadTexture(self.renderer, RESOURCES.get_path("Shading.png"))
        self.shading_def = textureDefinition(1280/2, 681, 322, 15, 180)
        
        self.moon = sdl2.sdlimage.IMG_LoadTexture(self.renderer, RESOURCES.get_path("Moon.png"))
        self.moon_def = textureDefinition(1280/2, 720/2, 200, 200, 0)
        
        self.running = True
        self.increase = False
        
        self.KeyAction = defaultdict(lambda: self.NoAction)
        self.KeyAction[SDL_SCANCODE_Q] = self.Quit
        self.KeyAction[SDL_SCANCODE_SPACE] = self.ChargeUp
        
        threading.Thread.__init__(self)
        self.p = int(round(time.time() * 1000))
        
    def run(self):
        while self.running:
            self.t = int(round(time.time() * 1000))
            if self.t-self.p > 100:
                print "Renderring Rate: " + str(1000.0/(self.t-self.p))
                self.p = self.t
            
            SDL_RenderClear(self.renderer)
            SDL_RenderCopy(self.renderer, self.background, None, self.background_def.dst)        
            SDL_RenderCopyEx(self.renderer, self.rocket, None, self.rocket_def.dst, self.rocket_def.angle, None, SDL_FLIP_NONE)        
            SDL_RenderCopyEx(self.renderer, self.moon, None, self.moon_def.dst, self.moon_def.angle, None, SDL_FLIP_NONE)        
            SDL_RenderCopy(self.renderer, self.shading, None, self.shading_def.dst)                    
            SDL_RenderPresent(self.renderer)

    def Quit(self):
        self.running = False
        
    def ChargeUp(self):
        if self.increase:
            self.shading_def.resize(3)
            if self.shading_def.dst.w >= 322:
                self.shading_def.dst.w = 322
                self.increase = False
        else:
            self.shading_def.resize(-3)
            if self.shading_def.dst.w <= 0:
                self.shading_def.dst.w = 0
                self.increase = True
        
    def NoAction():
        print "Nothing"
    
def main():
    Prog = renderingThread()
    Prog.start()
    
    event = SDL_Event()
    
    while Prog.running:
        while SDL_PollEvent(ctypes.byref(event)) != 0:
            if event.type == SDL_KEYDOWN:
                Prog.KeyAction[event.key.keysym.scancode]()

    return 0

if __name__ == "__main__":
    sys.exit(main())
