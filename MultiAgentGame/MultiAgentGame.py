# -*- coding:utf-8 -*-

# Standard Library
import numpy as np
import cv2

# Make Library
import Field
from Agent.AgentBase import AgentBase

if __name__ == "__main__":

    x = Field.Field(8)
    a = AgentBase(x)
    b = AgentBase(x)
    
    #img = np.zeros( (512, 512, 3), np.uint8 )
    #img = cv2.line( img, (0, 0), (100, 400), ( 255, 255, 255), 5)
    #cv2.imshow('log', img)
    #cv2.waitKey()