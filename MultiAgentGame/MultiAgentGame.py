# -*- coding:utf-8 -*-

# Standard Library
import numpy as np
import cv2
import random

# Make Library
import Field
from Agent.AgentBase import AgentBase
from Agent.TargetAgent import TargetAgent
from Agent.AgentZ import AgentZ

if __name__ == "__main__":

    fieldLegth = 15
    WindowSize = 512

    targetNum = 3
    agentNum = 2

    size = (int)( WindowSize / fieldLegth )

    f = Field.Field(fieldLegth)

    TargetList = []
    AgentList = []
    for i in range(targetNum):
        TargetList.append(TargetAgent(f))
    for i in range(agentNum):
        AgentList.append(AgentZ(f))

    while( True ):

        # アクションシーケンス
         ## 逃走エージェント
        for target in TargetList:
            if not target.validFlag:
                continue
            target.action()

         ## 確保エージェント
        for agent in AgentList:
            agent.action()

        # 情報アップデートシーケンス
        for target in TargetList:
            if not target.validFlag:
                continue
            target.update()
        for agent in AgentList:
            agent.update()


        # 描画シーケンス
        img = np.zeros( (WindowSize, WindowSize, 3), np.uint8 )
        for target in TargetList:
            if not target.validFlag:
                continue
            img = target.draw(img, size)
        for agent in AgentList:
            img = agent.draw(img, size)

        cv2.imshow('log', img)
        print(f.field)

        # 確保判定シーケンス
        for target in TargetList:
            if not target.validFlag:
                continue
            target.judgement()

        # リセットシーケンス
        targetValidList = []
        for target in TargetList:
            targetValidList.append(target.validFlag)
        if not True in targetValidList:
            f.reset(fieldLegth)
            for target in TargetList:
                img = target.reset(f)
            for agent in AgentList:
                img = agent.reset(f)

                


        if cv2.waitKey() == 27: break 