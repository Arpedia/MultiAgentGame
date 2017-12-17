# -*- coding:utf-8 -*-

import numpy as np
import cv2
import random

import Field

class AgentBase():

    def __init__(self, field, type):
        self.type = type
        self.field = field
        self.x, self.y = self.__setLocation()
    
    # Public Method
    def resetLocation(self, field):     # エージェントの再配置
        self.field = field
        self.x, self.y = self.__setLocation()

    def move(self, id):                 # エージェントの移動（上 下 左 右 : 0 1 2 3）
        if id == 0 and self.__can_move( 0, -1 ):
            self.field.setFieldValXY(self.x, self.y, 0)
            self.y += -1;
            self.field.setFieldValXY(self.x, self.y, 1)
        elif id == 1 and self.__can_move( 0, 1 ):
            self.field.setFieldValXY(self.x, self.y, 0)
            self.y += 1;
            self.field.setFieldValXY(self.x, self.y, 1)
        elif id == 2 and self.__can_move( -1, 0 ):
            self.field.setFieldValXY(self.x, self.y, 0)
            self.x += -1;
            self.field.setFieldValXY(self.x, self.y, 1)
        elif id == 3 and self.__can_move( 1, 0 ):
            self.field.setFieldValXY(self.x, self.y, 0)
            self.x += 1;
            self.field.setFieldValXY(self.x, self.y, 1)

    def update(self):
        self.around = self.field.getAround( self.x, self.y, 2 )
        print(self.field.field)

    # Private Method
    def __setLocation(self):
        tx = random.randint(0, self.field.MAX - 1)
        ty = random.randint(0, self.field.MAX - 1)
        while(True):
            if self.field.getFieldVal(tx, ty) == 0:
                self.field.setFieldValXY(tx, ty, self.type) 
                break
        return tx, ty

    def __can_move(self, mx, my):
        pos = (int)( len( self.around ) / 2 )
        print(pos + mx, pos + my)
        if self.around[pos + my][pos + mx] == -1:
            return False
        else:
            return True


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