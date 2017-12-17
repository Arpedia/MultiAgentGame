# -*- coding:utf-8 -*-


# Standard Library
import numpy as np
import cv2
import random

# Make Library
import Field
from .AgentBase import AgentBase

class Agent(AgentBase):
    def __init__(self, field):
        AgentBase.__init__(self, field, 1)
        self.color = [ 100, 150, 230] # BGRÇÃèá

    def draw(self, img, size):          # ï`âÊóp
        img = cv2.rectangle( img, ( self.x * size, self.y * size), ( (self.x + 1) * size, (self.y + 1) * size ), self.color, -1)
        return img
