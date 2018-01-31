# -*- coding:utf-8 -*-

import numpy as np
import random

import Field
from Agent.AgentBase import AgentBase

# 確保エージェント（座標で行動判断）
class AgentW(AgentBase):

    def __init__(self, field):
        super().__init__(field, 2)
        self.set_color( [180, 100, 200] )
        self.FieldSize = field.get_MAX()
        self.__resetQtable()
        self.LearnRate = 0.3
        self.Discount = 0.6
        self.QCount = 0


    # Public Method
    def reset(self, field):
        self.resetLocation(field)
        del self.preAct
        del self.preX
        del self.preY
        self.Qupdate = False
        self.QCount = 0

    def action(self, count, MaxStep):
        index = self.__nextActionNearbyTarget( self.get_around(2) )
        oldx = self.x
        oldy = self.y
        act = 0
        if len(index) > 0:
            while(True):
                act = random.choice(index)
                if self.move( act ):
                    break
            self.Qupdate = False
        else:
            if ( int(( count / MaxStep )* 10 + 1) > random.randint(0, 12) ):
                LimitCounter = 0

                while(True):
                    act = random.choice(self.__getMaxQValueAction(self.x, self.y))
                    if self.move( act ):
                        break
                    LimitCounter += 1

                    # 無限ループを抜けるために
                    if LimitCounter > 10:
                        while(True):
                            act = random.choice(range(4))
                            if self.move( act ):
                                break
                        break
            else:
                while(True):
                    act = random.choice(range(4))
                    if self.move( act ):
                        break
            self.Qupdate = True
        self.__remindPreviousAction(oldx, oldy, act)


    def update(self):
        super().update()
        if(self.Qupdate):
            self.Qtable[self.preY][self.preX][self.preAct] += self.LearnRate * ( self.__getReward() + self.Discount * self.__getMaxQValue(self.x, self.y) - self.Qtable[self.preY][self.preX][self.preAct] )
            if self.Qtable[self.preY][self.preX][self.preAct] < 0:
                self.Qtable[self.preY][self.preX][self.preAct] = 0
            if self.Qtable[self.preY][self.preX][self.preAct] > 25:
                self.Qtable[self.preY][self.preX][self.preAct] = 25

    def getQcount(self):
        return self.QCount

    # Private Method
    def __resetQtable(self):
        self.Qtable = []
        size = int(self.FieldSize / 5)
        for i in range(size):
            bufi = []
            for j in range(size):
                bufj = []
                for k in range(4):
                    bufj.append(25)
                bufi.append(bufj)
            self.Qtable.append(bufi)

    def __getValueFromQTable(self, x, y, act):
         return self.Qtable[(int)(y / 5)][(int)(x / 5)][act]

    def __setValueIntoQTable(self, x, y ,act, val):
        self.Qtable[(int)(y / 5)][(int)(x / 5)][act] = val

    def __remindPreviousAction(self, x, y, act):
         self.preX = (int)(x / 5)
         self.preY = (int)(y / 5)
         self.preAct = act

    def __getMaxQValue(self, x, y):
        arr = self.Qtable[(int)(y / 5)][(int)(x / 5)]
        return self.__getMaxInArray(arr)

    def __getMaxQValueAction(self, x, y):
        arr = self.Qtable[(int)(y / 5)][(int)(x / 5)]
        MaxValue = self.__getMaxInArray(arr)
        actionArray = []
        for i in range(len(arr)):
            if MaxValue == arr[i]:
                actionArray.append(i)

        return actionArray

    def __getMaxInArray(self, Array):
        buf = 0
        for arr in Array:
            if buf <= arr:
                buf = arr

        return buf

    def __getReward(self):
        around = self.get_around(2)
        for around_y in around:
            if 1 in around_y:
                return 3
        return -1

    def __nextActionNearbyTarget(self, around):
        action_index = []
        around_save = around

        # 上三角の判定
        around[1][0] = 0
        around[1][4] = 0
        for around_x in around[:2]:
            if 1 in around_x:
                action_index.append(0)
                break

        around = around_save
        # 下三角の判定
        around[3][0] = 0
        around[3][4] = 0
        for around_x in around[3:]:
            if 1 in around_x:
                action_index.append(1)
                break

        around = around_save
        # 左三角の判定
        around[0][1] = 0
        around[4][1] = 0
        for around_x in around:
            if 1 in around_x[:2]:
                action_index.append(2)
                break

        around = around_save
        # 下三角の判定
        around[0][3] = 0
        around[4][3] = 0
        for around_x in around:
            if 1 in around_x[3:]:
                action_index.append(3)
                break

        return action_index



