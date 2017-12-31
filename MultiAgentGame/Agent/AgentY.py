# -*- coding:utf-8 -*-

import numpy as np
import random

import Field
from Agent.AgentBase import AgentBase

# 確保エージェント（周囲状況で行動判断）
class AgentY(AgentBase):

    def __init__(self, field):
        self = AgentBase(field, 2)

    def reset(self, field):
        self.resetLocation(field)
        
    def action(self, field):
        self.update()

