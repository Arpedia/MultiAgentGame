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

    def move(self, id):                 # エージェントの移動（上 下 左 右 留: 0 1 2 3 4）
        if id == 0 and self.__can_move( 0, -1 ):
            self.field.setFieldValXY(self.x, self.y, 0)
            self.y += -1;
            self.field.setFieldValXY(self.x, self.y, self.type)
            return True

        elif id == 1 and self.__can_move( 0, 1 ):
            self.field.setFieldValXY(self.x, self.y, 0)
            self.y += 1;
            self.field.setFieldValXY(self.x, self.y, self.type)
            return True

        elif id == 2 and self.__can_move( -1, 0 ):
            self.field.setFieldValXY(self.x, self.y, 0)
            self.x += -1;
            self.field.setFieldValXY(self.x, self.y, self.type)
            return True

        elif id == 3 and self.__can_move( 1, 0 ):
            self.field.setFieldValXY(self.x, self.y, 0)
            self.x += 1;
            self.field.setFieldValXY(self.x, self.y, self.type)
            return True

        elif id == 4:
            return True
        
        return False

    def update(self):                   # 状況の更新
        self.around = self.field.getAround( self.x, self.y, 2 )

    def invalid(self):
        self.field.setFieldValXY(self.x, self.y, 0)

    def get_around(self, width):
        self.around = self.field.getAround( self.x, self.y, width )
        return self.around

    def set_color(self, color):
        self.color = color

    def draw(self, img, size):
        img = cv2.rectangle( img, ( self.x * size, self.y * size), ( (self.x + 1) * size, (self.y + 1) * size ), self.color, -1)
        return img

    # Private Method
    def __setLocation(self):
        tx = ty = 0
        while(True):
            tx = random.randint(0, self.field.MAX - 1)
            ty = random.randint(0, self.field.MAX - 1)
            if self.field.getFieldVal(tx, ty) == 0:
                self.field.setFieldValXY(tx, ty, self.type) 
                break
        return tx, ty

    def __can_move(self, mx, my):
        pos = (int)( len( self.around ) / 2 )
        if self.around[pos + my][pos + mx] != 0:
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