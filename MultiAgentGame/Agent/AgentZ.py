# -*- coding:utf-8 -*-

import numpy as np
import random

import Field
from Agent.AgentBase import AgentBase


# 行動がランダム（見つけ次第追跡）
class AgentZ(AgentBase):
    def __init__(self, field):
        super().__init__(field, 2)
        self.set_color( [180, 100, 200] )
        self.Qcount = 0

    # Public Method
    def reset(self, field):
        self.resetLocation(field)

    def action(self):
        around = self.get_around(2)
        index = self.__nextAction( around )
        if len(index) > 0:
            self.move( random.choice(index) )
        else:
            self.move( random.choice( [i for i in range(4)] ) )

    def getQcount(self):
        return self.Qcount

    # Private Method
    def __nextAction(self, around):
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
