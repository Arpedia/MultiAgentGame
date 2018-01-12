# -*- coding:utf-8 -*-

import numpy as np
import cv2


class Field():
    def __init__(self, x):
        self.field = np.zeros( (x, x), np.int8 )
        self.MAX = x
        
    # Public Get Method
    def reset(self, x):
        self.field = np.zeros( (x, x), np.int8 )

    def getField(self):
        return self.field

    def getFieldVal(self, x, y):        # 座標地点の値を取得
        return self.field[y][x]

    def setFieldValXY(self, x, y, val): # 座標地点の値を変更
        self.field[y][x] = val

    def getAround(self, x, y, wid):     # 周囲の状況を取得
        length = wid * 2 + 1                # 一辺の長さの計算
        around = np.zeros( (length, length), np.int8 )

        for i in range(-1 * wid, wid + 1):
            py = y + i                      # 受け取ったy座標に( ...,-2, -1, 0, 1, 2,... )と足してく

            if (py < 0 or py >= self.MAX ):  # 配列の範囲を下回る or 超える
                for q in range(length):
                    around[i + wid][q] = -1
                continue

            for j in range(-1 * wid, wid + 1):
                px = x + j                  # 受け取ったx座標に( ...,-2, -1, 0, 1, 2,... )と足してく

                if (px < 0 or px >= self.MAX):  # 配列の範囲を下回る or 超える
                    around[i + wid][j + wid] = -1
                    continue
                
                around[i + wid][j + wid] = self.getFieldVal(px, py)
        around[wid][wid] = 1               # 自分の位置は1であらわす

        return around


    # Private Method
    def get_MAX(self):
        return self.MAX

    def __set_MAX(self, max):
        self.MAX = max

    # Define Accessor
    #MAX = property(__get_MAX, __set_MAX)