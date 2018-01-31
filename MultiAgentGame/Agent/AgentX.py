# -*- coding:utf-8 -*-

import numpy as np
import random

import Field
from Agent.AgentBase import AgentBase

# 確保エージェント（座標で行動判断）
class AgentX(AgentBase):

    def __init__(self, field):
        super().__init__(field, 2)
        self.set_color( [180, 100, 200] )
        self.__resetQtable(field.get_MAX())
        self.LearnRate = 0.5
        self.Discount = 0.5
        self.FindTarget = False
        self.QCount = 0


    # Public Method
    def reset(self, field):
        self.resetLocation(field)
        del self.preAct
        del self.preOther
        del self.preX
        del self.preY
        self.Qupdate = False
        self.FindTarget = False
        self.QCount = 0

    def action(self, otherAgent, count, MaxStep):
        around = self.get_around(2)
        index = self.__nextActionNearbyTarget( around )
        oldx = self.x
        oldy = self.y
        otherAgentArea = otherAgent.getArea()
        act = 0

        if len(index) > 0:
            self.move( random.choice(index) )
            self.Qupdate = False
        else:
            if ( int(( count / MaxStep )* 10 + 1) > random.randint(0, 12) ):
                act = random.choice(self.__getMaxQValueAction(self.x, self.y, otherAgentArea))
                LimitCount = 0
                while(True):
                    if self.move( act ):
                        break
                    if LimitCount > 10:
                        while(True):
                            act = random.choice(range(4))
                            if self.move(act):
                                break
                        break
                    LimitCount += 1

            else:
                while(True):
                    act = random.choice(range(4))
                    if self.move( act ):
                        break
            self.Qupdate = True
        self.__remindPreviousAction(oldx, oldy, otherAgentArea, act)

    def update(self, AgentAroundFlag):
        super().update()
        if(self.Qupdate and AgentAroundFlag == False or (AgentAroundFlag and self.FindTarget == False)):
            self.QCount += 1
            self.Qtable[self.preY][self.preX][self.preOther][self.preAct] += self.LearnRate * ( self.__getReward(AgentAroundFlag) + self.Discount * self.__getMaxQValue(self.x, self.y, self.preOther) - self.Qtable[self.preY][self.preX][self.preOther][self.preAct] )
            if self.Qtable[self.preY][self.preX][self.preOther][self.preAct] < 0:
                self.Qtable[self.preY][self.preX][self.preOther][self.preAct] = 0
            if self.Qtable[self.preY][self.preX][self.preOther][self.preAct] > 25:
                self.Qtable[self.preY][self.preX][self.preOther][self.preAct] = 25
        self.FindTarget = AgentAroundFlag


    def getArea(self):
        size = self.field.get_MAX()
        Area = 0
        if self.y < int(size / 2):
            Area += 0
        else:
            Area += 2
        if self.x < int(size / 2):
            Area += 0
        else:
            Area += 1
        
        # [左上:0, 右上:1, 左下:2, 右下:3]
        return Area

    def getIsAroundTarget(self):
        around = self.get_around(2)
        for around_y in around:
            if 1 in around_y:
                return True
        return False

    def getQcount(self):
        return self.QCount

    # Private Method
    def __resetQtable(self, size):
        self.Qtable = []
        for i in range(size):
            bufi = []
            for j in range(size):
                bufj = []
                for o in range(4):
                    bufo = []
                    for k in range(4):
                        if j == 0 and k == 2:
                            bufo.append(-1)
                        elif j == size - 1 and k == 3:
                            bufo.append(-1)
                        elif i == 0 and k == 0:
                            bufo.append(-1)
                        elif i == size - 1 and k == 1:
                            bufo.append(-1)
                        else:
                            bufo.append(25)
                        bufj.append(bufo)
                    bufi.append(bufj)
            self.Qtable.append(bufi)

    def __getValueFromQTable(self, x, y, other, act):
         return self.Qtable[y][x][other][act]

    def __setValueIntoQTable(self, x, y , other, act, val):
        self.Qtable[y][x][other][act] = val

    def __remindPreviousAction(self, x, y, other, act):
         self.preX = x
         self.preY = y
         self.preOther = other
         self.preAct = act

    def __getMaxQValue(self, x, y, other):
        arr = self.Qtable[y][x][other]
        return self.__getMaxInArray(arr)

    def __getMaxQValueAction(self, x, y, other):
        arr = self.Qtable[y][x][other]
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

    def __getReward(self, flag):
        if flag:
            return 5
        else:
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



