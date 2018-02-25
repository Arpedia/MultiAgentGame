# -*- coding:utf-8 -*-

import numpy as np
import random

import Field
from Agent.AgentBase import AgentBase

# 逃走エージェント
class TargetAgent(AgentBase):

    def __init__(self, field):
        super().__init__(field, 1)
        self.set_color( [100, 150, 230] ) # BGR
        self.validFlag = True

    # Public Method
    def reset(self, field):
        self.resetLocation(field)
        self.validFlag = True

    def action(self):
        around = self.get_around(3)
        moveIndex = self.__refine_actionIndex(around)
        counter = 0
        while(True):
            if counter == 10 or len(moveIndex) == 0:
                self.move(4)
                break
            if self.move( random.choice( moveIndex ) ):
                break
            counter += 1

    def judgement(self):
        around = self.get_around(1)
        if self.__existAgent(around):
            self.caught()

    def caught(self):
        self.validFlag = False
        self.invalid()


    # Private Method
    def __refine_actionIndex(self, around_save):
        action_index = [ i for i in range(5) ]
        around = np.copy(around_save)
        escapeFlag = False

        # 上三角の判定
        around[1][0] = 0
        around[1][6] = 0
        around[2][0] = around[2][1] = 0
        around[2][6] = around[2][5] = 0
        for around_x in around[:3]:
            if 2 in around_x and 0 in action_index:
                action_index.remove(0)
                escapeFlag = True
                break

        around = np.copy(around_save)
        # 下三角の判定
        around[5][0] = 0
        around[5][6] = 0
        around[4][0] = around[4][1] = 0
        around[4][6] = around[4][5] = 0
        for around_x in around[4:]:
            if 2 in around_x and 1 in action_index:
                action_index.remove(1)
                escapeFlag = True
                break

        around = np.copy(around_save)
        # 左三角の判定
        around[0][1] = 0
        around[6][1] = 0
        around[0][2] = around[1][2] = 0
        around[6][2] = around[5][2] = 0
        for around_x in around:
            if 2 in around_x[:3] and 2 in action_index:
                action_index.remove(2)
                escapeFlag = True
                break

        around = np.copy(around_save)
        # 右三角の判定
        around[0][5] = 0
        around[6][5] = 0
        around[0][4] = around[1][4] = 0
        around[6][4] = around[5][4] = 0
        for around_x in around:
            if 2 in around_x[4:] and 3 in action_index:
                action_index.remove(3)
                escapeFlag = True
                break

        if escapeFlag:
            action_index.remove(4)

        return action_index

    def __existAgent(self, around):
        if 2 in around:
            return True
        return False

    # For Accessor Methods
    def __get_validFlag(self):
        return self._validFlag

    def __set_validFlag(self, flag):
        self._validFlag = flag


    validFlag = property(__get_validFlag, __set_validFlag)