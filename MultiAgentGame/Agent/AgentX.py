# -*- coding:utf-8 -*-

import numpy as np
import random

import Field
from Agent.AgentBase import AgentBase

# 確保エージェント（大まかな位置＆周囲状況のハイブリッド）
class AgentX(AgentBase):

    def __init__(self, field):
        self = AgentBase(field, 2)

    def reset(self, field):
        self.resetLocation(field)
        
    def action(self, field):
        self.update()