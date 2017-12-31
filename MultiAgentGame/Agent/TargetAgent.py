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
        # self.update()
        around = self.get_around()
        moveIndex = self.__refine_actionIndex(around)
        while(True):
            if self.move( random.choice( moveIndex ) ):
                break

    def caught(self):
        self.validFlag = False
        self.invalid()


    # Private Method
    def __refine_actionIndex(self, around):
        action_index = [ i for i in range(5) ]
        around_save = around
        escapeFlag = False

        # 上三角の判定
        around[1][0] = 0
        around[1][4] = 0
        for around_x in around[:2]:
            if 2 in around_x and 0 in action_index:
                action_index.remove(0)
                escapeFlag = True
                break

        around = around_save
        # 下三角の判定
        around[3][0] = 0
        around[3][4] = 0
        for around_x in around[3:]:
            if 2 in around_x and 1 in action_index:
                action_index.remove(1)
                escapeFlag = True
                break

        around = around_save
        # 左三角の判定
        around[0][1] = 0
        around[4][1] = 0
        for around_x in around:
            if 2 in around_x[:2] and 2 in action_index:
                action_index.remove(2)
                escapeFlag = True
                break

        around = around_save
        # 下三角の判定
        around[0][3] = 0
        around[4][3] = 0
        for around_x in around:
            if 2 in around_x[3:] and 3 in action_index:
                action_index.remove(3)
                escapeFlag = True
                break

        if escapeFlag:
            action_index.remove(4)

        return action_index

    # For Accessor Methods
    def __get_validFlag(self):
        return self._validFlag

    def __set_validFlag(self, flag):
        self._validFlag = flag


    validFlag = property(__get_validFlag, __set_validFlag)