# -*- coding: utf-8 -*-
"""
@author:
Jackson Cagle
Brain Mapping Laboratory
J. Crayton Pruitt Family Department of Biomedical Engineering, 
University of Florida
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

# Define Positioning Variables
WINDOW_WIDTH	= 1280
WINDOW_HEIGHT	= 720
SHADING_WIDTH 	= WINDOW_WIDTH*0.255
SHADING_HEIGHT 	= WINDOW_HEIGHT*0.021
RESOURCES = sdl2.ext.Resources(__file__, "resources")

class textureDefinition:
    def __init__(self, x, y, w, h, angle):
        self.dst = sdl2.rect.SDL_Rect(int(x-w/2),int(y-h/2),int(w),int(h))
        self.default = (self.dst,angle)
        self.angle = angle

    def reset(self):
        self.angle = self.default[1]
        self.dst = self.default[0]
    
    def rotate(self, angle):
        self.angle = angle
    
    def translate(self, x, y):
        self.dst.x = x-w/2
        self.dst.y = y-h/2
        
    def resize(self, change):
        self.dst.x -= change
        self.dst.w += change
    
class renderingThread(threading.Thread):

    def __init__(self):
        sdl2.ext.init()
        self.window = sdl2.ext.Window("Rocket Demo", size=(WINDOW_WIDTH,WINDOW_HEIGHT))
        self.window.show()        
        self.renderer = SDL_CreateRenderer(self.window.window, -1, SDL_RENDERER_ACCELERATED | SDL_RENDERER_PRESENTVSYNC)
        
        self.background = sdl2.sdlimage.IMG_LoadTexture(self.renderer, RESOURCES.get_path("Background.png"))
        self.background_def = textureDefinition(WINDOW_WIDTH/2, WINDOW_HEIGHT/2, WINDOW_WIDTH, WINDOW_HEIGHT, 0)
        
        self.rocket = sdl2.sdlimage.IMG_LoadTexture(self.renderer, RESOURCES.get_path("Rocket.png"))
        self.rocket_def = textureDefinition(WINDOW_WIDTH/2, 500, 30, 100, 0)

        self.shading = sdl2.sdlimage.IMG_LoadTexture(self.renderer, RESOURCES.get_path("Shading.png"))
        self.shading_def = textureDefinition(WINDOW_WIDTH/2, WINDOW_HEIGHT*0.946, SHADING_WIDTH, SHADING_HEIGHT, 0)
        
        self.moon = sdl2.sdlimage.IMG_LoadTexture(self.renderer, RESOURCES.get_path("Moon.png"))
        self.moon_def = textureDefinition(WINDOW_WIDTH/2, WINDOW_HEIGHT/2, 200, 200, 0)
        
        self.running = True
        self.increase = False
        
        self.KeyAction = defaultdict(lambda: self.NoAction)
        self.KeyAction[SDL_SCANCODE_Q] = self.Quit
        self.KeyAction[SDL_SCANCODE_SPACE] = self.ChargeUp
        
        threading.Thread.__init__(self)
        self.p = int(round(time.time() * 1000))
        
    def run(self):
        while self.running:
            SDL_RenderClear(self.renderer)
            SDL_RenderCopy(self.renderer, self.background, None, self.background_def.dst)        
            SDL_RenderCopyEx(self.renderer, self.rocket, None, self.rocket_def.dst, self.rocket_def.angle, None, SDL_FLIP_NONE)        
            SDL_RenderCopyEx(self.renderer, self.moon, None, self.moon_def.dst, self.moon_def.angle, None, SDL_FLIP_NONE)        
            SDL_RenderCopy(self.renderer, self.shading, None, self.shading_def.dst)                    
            SDL_RenderPresent(self.renderer)

    def Launch(self):
        Force = self.shading_def.dst.w / SHADING_WIDTH
        self.shading_def.reset()
    
    def Quit(self):
        self.running = False
        
    def ChargeUp(self):
        if self.increase:
            self.shading_def.resize(3)
            if self.shading_def.dst.w >= int(SHADING_WIDTH):
                self.shading_def.dst.w = int(SHADING_WIDTH)
                self.increase = False
        else:
            self.shading_def.resize(-3)
            if self.shading_def.dst.w <= 0:
                self.shading_def.dst.w = 0
                self.increase = True
                
    def NoAction():
		pass
    
def main():
    Prog = renderingThread()
    Prog.start()
    
    event = SDL_Event()
    while Prog.running:
        while SDL_PollEvent(ctypes.byref(event)) != 0:
            if event.type == SDL_KEYDOWN:
                Prog.KeyAction[event.key.keysym.scancode]()
            elif event.type == SDL_KEYUP:
                Prog.Launch()

    return 0

if __name__ == "__main__":
    sys.exit(main())
