# -*- coding:utf-8 -*-

import numpy as np
import random

import Field
from Agent.AgentBase import AgentBase

# 確保エージェント（座標で行動判断）
class AgentY(AgentBase):

    def __init__(self, field):
        super().__init__(field, 2)
        self.set_color( [180, 100, 200] )
        self.__resetQtable(field.get_MAX())
        self.LearnRate = 0.3
        self.Discount = 0.6


    # Public Method
    def reset(self, field):
        self.resetLocation(field)

    def action(self, count, MaxStep):
        around = self.get_around(2)
        index = self.__nextActionNearbyTarget( around )
        if len(index) > 0:
            self.move( random.choice(index) )
            self.Qupdate = False
        else:
            act = 0
            if ( int(count / MaxStep * 10) > random.randint(1, 10)):
                act = self.__getValueFromQTable(self.x, self.y)
                self.move( act )
                self.__remindPreviousAction(self.x, self.y, act)
            else:
                act = random.choice(range(4))
                self.move( act )
                self.__remindPreviousAction(self.x, self.y, act)
            self.Qupdate = True


    def update(self):
        super().update()
        if(self.Qupdate):
            self.Qtable[self.preX][self.preY][self.preAct] += self.LearnRate * ( self.__getReward(self.x, self.y) + self.Discount * self.__getMaxQValue(self.x, self.y) - self.Qtable[self.preX][self.preY][self.preAct] )


    # Private Method
    def __resetQtable(self, size):
        self.Qtable = []
        for i in range(size):
            bufi = []
            for j in range(size):
                bufj = []
                for k in range(5):
                    bufj.append(25)
                bufi.append(bufj)
            self.Qtable.append(bufi)

    def __getValueFromQTable(self, x, y, act):
         return self.Qtable[x][y][act]

    def __remindPreviousAction(self, x, y, act):
         self.preX = x
         self.preY = y
         self.preAct = act

    def __getMaxQValue(self, x, y):
        arr = self.Qtable[x][y]
        return self.__getMaxInArray(arr)

    def __getMaxInArray(self, Array):
        buf = 0
        for arr in Array:
            if buf <= arr:
                buf = arr

        return buf

    def __getReward(self, x, y):
        around = self.get_around(2)
        for around_y in around:
            if 1 in around_y:
                return 5
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



