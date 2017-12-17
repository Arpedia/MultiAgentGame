# -*- coding:utf-8 -*-

# Standard Library
import numpy as np
import cv2
import random

# Make Library
import Field
from Agent.AgentBase import AgentBase
from Agent.Agent import Agent

if __name__ == "__main__":

    fieldLegth = 15
    WindowSize = 512

    size = (int)( WindowSize / fieldLegth )

    x = Field.Field(fieldLegth)
    a = Agent(x)
    b = Agent(x)

    while( True ):

        a.update()
        b.update()

        a.move(random.randint(0, 3))
        b.move(random.randint(0, 3))


        img = np.zeros( (WindowSize, WindowSize, 3), np.uint8 )
        img = a.draw(img, size)
        img = b.draw(img, size)
        cv2.imshow('log', img)
        if cv2.waitKey() == 27: break 