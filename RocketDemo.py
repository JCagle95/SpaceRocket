# -*- coding: utf-8 -*-
"""
Created on Wed Oct 12 17:27:51 2016

@author: Jackson
"""

import os
import sys
import time
os.environ['PYSDL2_DLL_PATH'] = '.\SDL2'

import ctypes
from sdl2 import *
import sdl2.sdlimage
import sdl2.ext

import threading

RESOURCES = sdl2.ext.Resources(__file__, "resources")

def EventDetection(event):
    while SDL_PollEvent(ctypes.byref(event)) != 0:
        if event.type == SDL_KEYDOWN:
            return event.key.keysym.scancode
    return 0

class textureDefinition:
    def __init__(self, x, y, w, h, angle):
        self.dst = sdl2.rect.SDL_Rect(x,y,w,h)
        self.angle = angle
    
    def rotate(self, angle):
        self.angle = angle
    
    def translate(self, x, y):
        self.dst.x = x
        self.dst.y = y
        
    def resize(self, w, h):
        self.dst.w = w
        self.dst.h = h
    
class renderingThread(threading.Thread):
    
    def __init__(self):
        sdl2.ext.init()
        self.window = sdl2.ext.Window("Rocket Demo", size=(1280,720))
        self.window.show()        
        self.renderer = SDL_CreateRenderer(self.window.window, -1, SDL_RENDERER_ACCELERATED | SDL_RENDERER_PRESENTVSYNC)
        
        self.background = sdl2.sdlimage.IMG_LoadTexture(self.renderer, RESOURCES.get_path("Space.png"))
        self.background_def = textureDefinition(0, 0, 1280, 720, 0)
        
        self.rocket = sdl2.sdlimage.IMG_LoadTexture(self.renderer, RESOURCES.get_path("Rocket.png"))
        self.rocket_def = textureDefinition(0, 0, 20, 100, 0)

        self.shading = sdl2.sdlimage.IMG_LoadTexture(self.renderer, RESOURCES.get_path("Shading.png"))
        self.shading_def = textureDefinition(0, 100, 20, 100, 0)
        
        self.running = True
        threading.Thread.__init__(self)
        
    def run(self):
        while self.running:
            SDL_RenderClear(self.renderer)            
            SDL_RenderCopy(self.renderer, self.background, None, self.background_def.dst)        
            SDL_RenderCopyEx(self.renderer, self.rocket, None, self.rocket_def.dst, self.rocket_def.angle, None, SDL_FLIP_NONE)        
            SDL_RenderCopy(self.renderer, self.shading, None, self.shading_def.dst)                    
            SDL_RenderPresent(self.renderer)            
        
def main():    
    Prog = renderingThread()
    Prog.start()
    
    event = SDL_Event()
    while True:
        if EventDetection(event) == SDL_SCANCODE_Q:
            Prog.running = False
            break
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
