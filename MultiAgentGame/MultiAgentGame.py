# -*- coding:utf-8 -*-

# Standard Library
import numpy as np
import cv2
import random
from matplotlib import pyplot

# Make Library
import Field
from Agent.AgentBase import AgentBase
from Agent.TargetAgent import TargetAgent
from Agent.AgentZ import AgentZ
from Agent.AgentY import AgentY

if __name__ == "__main__":

    fieldLegth = 25
    WindowSize = 512
    TrialCount = 500
    MaxStep = 2000
    Count = 0
    Step = 0

    targetNum = 3
    agentNum = 2

    Result = []

    size = (int)( WindowSize / fieldLegth )

    f = Field.Field(fieldLegth)

    TargetList = []
    AgentList = []
    for i in range(targetNum):
        TargetList.append(TargetAgent(f))
    for i in range(agentNum):
        ##AgentList.append(AgentZ(f))
        AgentList.append(AgentY(f))

    while( Count < TrialCount ):
        Step += 1

        # アクションシーケンス
         ## 逃走エージェント
        for target in TargetList:
            if not target.validFlag:
                continue
            target.action()

         ## 確保エージェント--AgentZ
        #for agent in AgentList:
        #    agent.action()
         ## 確保エージェント--AgentY
        for agent in AgentList:
            agent.action(Count, TrialCount)

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

        # 確保判定シーケンス
        for target in TargetList:
            if not target.validFlag:
                continue
            target.judgement()

        # リセットシーケンス
        targetValidList = []
        for target in TargetList:
            targetValidList.append(target.validFlag)
        if not True in targetValidList or Step > MaxStep:
            f.reset(fieldLegth)
            for target in TargetList:
                img = target.reset(f)
            for agent in AgentList:
                img = agent.reset(f)
            Count += 1
            print(str(Count) + ":" + str(Step))
            Result.append(Step)
            Step = 0
        print(str(Count) + ":" + str(Step) + str(not True in targetValidList))

        if cv2.waitKey() == 27: break 

    pyplot.plot(range(len(Result)), Result)
    pyplot.show()