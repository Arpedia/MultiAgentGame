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
    TrialCount = 1000
    MaxStep = 2500
    Count = 0
    Step = 0

    targetNum = 5
    agentNum = 2

    AgentLogic = 'Y'

    Result = []

    size = (int)( WindowSize / fieldLegth )

    f = Field.Field(fieldLegth)

    TargetList = []
    AgentList = []
    for i in range(targetNum):
        TargetList.append(TargetAgent(f))
    for i in range(agentNum):
        if AgentLogic == 'Z':
            AgentList.append(AgentZ(f))
        if AgentLogic == 'Y':
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
        if AgentLogic == 'Z':
            for agent in AgentList:
                agent.action()
         ## 確保エージェント--AgentY
        if AgentLogic == 'Y':
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
        #cv2.imshow('log', img)

        # 確保判定シーケンス
        for target in TargetList:
            if not target.validFlag:
                continue
            target.judgement()


        # リセットシーケンス
        targetValidList = []
        for target in TargetList:
            targetValidList.append(target.validFlag)
        if not True in targetValidList or Step >= MaxStep:
            f.reset(fieldLegth)
            for target in TargetList:
                img = target.reset(f)
            for agent in AgentList:
                img = agent.reset(f)
            Count += 1
            print(str(Count) + ":" + str(Step))
            Result.append(Step)
            Step = 0

        #if cv2.waitKey() == 27: break 

    average5 = []
    average10 = []
    average50 = []
    counter = buf5 = buf10 = buf50 = 0
    for idx in range(len(Result)):
        buf5 += Result[idx]
        buf10 += Result[idx]
        buf50 += Result[idx]
        if (idx + 1) % 5 == 0:
            average5.append(buf5 / 5.0)
            buf5 = 0
        if (idx + 1) % 10 == 0:
            average10.append(buf10 / 10.0)
            buf10 = 0
        if (idx + 1) % 50 == 0:
            average50.append(buf50 / 50.0)
            buf50 = 0
    pyplot.plot(range(len(Result)), Result, color='lightgray', label = "Steps")
    pyplot.plot([i * 5 for i in range(len(average5))], average5, color='blue', label = "Steps(Average 5)")
    pyplot.plot([i * 10 for i in range(len(average10))], average10, color='green', label = "Steps(Average 10)")
    pyplot.plot([i * 50 for i in range(len(average50))], average50, color='red', label = "Steps(Average 50)")
    if AgentLogic == 'Z':
        pyplot.title("Steps - Trials[Normal]")
    if AgentLogic == 'Y':
        pyplot.title("Steps - Trials[Q-Learning]")
    pyplot.xlabel("Trial Counts")
    pyplot.ylabel("Steps")
    pyplot.legend()
    pyplot.show()
