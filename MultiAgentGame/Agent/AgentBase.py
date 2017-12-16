# -*- coding:utf-8 -*-

import numpy as np
import cv2
import random

import Field

class AgentBase():

    def __init__(self, field):
        self.field = field
        self.x, self.y = self.__setLocation()
        p = field.getAround(self.x, self.y, 2)
        print(p)


    # Private Method
    def __setLocation(self):
        tx = random.randint(0, self.field.MAX - 1)
        ty = random.randint(0, self.field.MAX - 1)
        while(True):
            if self.field.getFieldVal(tx, ty) == 0:
                self.field.setFieldValXY(tx, ty, 1) 
                break
        return tx, ty



    # For Accessor Methods
    def __get_x(self):
        return self._x


    def __get_y(self):
        return self._y


    def __set_x(self, tx):
        self._x = tx


    def __set_y(self, ty):
        self._y = ty

    x = property(__get_x, __set_x)
    y = property(__get_y, __set_y)