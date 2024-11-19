import sys
import os
import math

import numpy as np
from numpy import zeros, array
from numpy.linalg import norm

import pyglet
from pyglet import *

sys.path.append(os.path.dirname(os.path.dirname(__file__) + '/../util'))
from util.properties import *
from util.constants import *

win = window.Window(*SCREEN_SIZE, 
                    caption = 'Gold Foil Scattering',
                    resizable = True, vsync = False
                    )

if FULLSCREEN:
    screen = canvas.get_display().get_screens()[0]
    win.set_size(screen.width, screen.height)
    win.set_fullscreen(True)
    
win.view = win.view.translate((win.width / 2, win.height / 2, 1))
win.view = win.view.scale((ZOOM_FACTOR, ZOOM_FACTOR, 1))

# Graphics Batches and Object Lists

guiElements = graphics.Batch()
goldAtoms = graphics.Batch()
goldAtomicBorders = graphics.Batch()
alphaParticles = graphics.Batch()

guiElements.list, goldAtoms.list, alphaParticles.list = [], [], []

# GUI Elements

# Body Definitions

class goldAtom():
    def __init__(self, position):
            
        self.name = "Gold Atom"
        self.mass = gold_Mass
        self.charge = gold_AtomicNumber * e
        
        self.position = position
        
        if gold_drawAtomicBorder:
            self.sprite_atom_outer = shapes.Circle(
                *position, gold_AtomicRadius,
                color = (255, 215, 0), batch = goldAtomicBorders,
                segments=100
            )
            
            self.sprite_atom_inner = shapes.Circle(
                *position, 0.97 * gold_AtomicRadius,
                color = (0, 0, 0), batch = goldAtomicBorders,
                segments=100
            )
        
        self.sprite_nucleus = shapes.Circle(
            *position, gold_NuclearRadius, 
            color = (255, 215, 0), batch = goldAtoms,
            segments=100
        )

class alphaParticle(): 
    def __init__(self, position, velocity = zeros(2)):  
            
        self.name = "Alpha Particle"
        self.mass = alpha_Mass
        self.charge = alpha_AtomicNumber * e
        
        self.position = position
        self.velocity = velocity
        
        self.sprite = shapes.Circle(
            *position, alpha_NuclearRadius, 
            color = (255, 255, 255), batch = alphaParticles,
            segments=100
        )
        
    def acceleration(self):
        force = zeros(2)
        if self.mass == 0: return force
        
        for body in goldAtoms.list:
            r = body.position - self.position
            force += k * self.charge * body.charge * r / norm(r)**3
        
        return (force / self.mass)
        
    def update(self, dt):
        self.velocity += self.acceleration() * dt
        self.position += self.velocity * dt
        self.sprite.position = self.position

# Body Instance Creation

goldAtoms.list = []

def create(n, d):
    if n % 2 == 0:
        m = n // 2
        for i in range(m):
            goldAtoms.list.append(goldAtom(([-d * (2 * i + 1) / 2, 0])))
            goldAtoms.list.append(goldAtom(([d * (2 * i + 1) / 2, 0])))
         
    else:
        m = (n-1) // 2
        for i in range(m):
            goldAtoms.list.append(goldAtom(([-d * (i + 1), 0])))
            goldAtoms.list.append(goldAtom(([d * (i + 1), 0])))
            goldAtoms.list.append(goldAtom(zeros(2)))

create(12, 2*gold_AtomicRadius)

alphaParticles.list.append(alphaParticle(array([0*effectiveRadius, -effectiveRadius])))

@win.event
def on_draw():
    win.clear()

    goldAtomicBorders.draw()
    goldAtoms.draw()
    alphaParticles.draw()
    guiElements.draw()

def update(dt): 
    for particle in alphaParticles.list:
        particle.update(dt)

if __name__ == '__main__':
    pyglet.clock.schedule_interval(update, dt)
    app.run()