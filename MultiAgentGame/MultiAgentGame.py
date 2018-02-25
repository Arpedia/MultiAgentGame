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
from Agent.AgentX import AgentX
from Agent.AgentW import AgentW

if __name__ == "__main__":

    fieldLegth = 30
    WindowSize = 512
    TrialCount = 1000
    MaxStep = 3000
    Count = 0
    Step = 0

    targetNum = 7
    agentNum = 2
    
    AgentLogic = input('Agent(Z, Y ,W): ')

    fourcc = cv2.VideoWriter_fourcc(*'MP4V')
    writer = cv2.VideoWriter('q-learning' + AgentLogic + '.mp4', fourcc, 10, (WindowSize, WindowSize))

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
        if AgentLogic == 'X':
            AgentList.append(AgentX(f))
        if AgentLogic == 'W':
            AgentList.append(AgentW(f))

    while( Count < TrialCount ):
        Step += 1

        # アクションシーケンス---------------------------------------
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
         ## 確保エージェント--AgentX
        if AgentLogic == 'X':
            for num in range(len(AgentList)):
                AgentList[num].action(AgentList[num - 1], Count, TrialCount)
         ## 確保エージェント--AgentW
        if AgentLogic == 'W':
            for agent in AgentList:
                agent.action(Count, TrialCount)


        # 情報アップデートシーケンス---------------------------------
        for target in TargetList:
            if not target.validFlag:
                continue
            target.update()

        if AgentLogic == 'X':   ## エージェントXの場合はもう一つのターゲットの情報がいるため
            flag = False
            for agent in AgentList:
                if agent.getIsAroundTarget():
                    flag = True
                    break
            for agent in AgentList:
                agent.update(flag)
        else:
            for agent in AgentList:
                agent.update()


        # 描画シーケンス---------------------------------------------
        if AgentLogic == 'W':
            img = np.zeros( (WindowSize, WindowSize, 3), np.uint8 )
            for target in TargetList:
                if not target.validFlag:
                    continue
                img = target.draw(img, size)
            for agent in AgentList:
                img = agent.draw(img, size)
        
            if Count % (TrialCount / 10) == 0:
                cv2.imshow('log', img)
                writer.write(img)
                if cv2.waitKey(1) == 27: break 

        # 確保判定シーケンス---------------------------------------------
        for target in TargetList:
            if not target.validFlag:
                continue
            target.judgement()


        # リセットシーケンス----------------------------------------
        targetValidList = []
        for target in TargetList:
            targetValidList.append(target.validFlag)
        if not True in targetValidList or Step >= MaxStep:
            f.reset(fieldLegth)
            for target in TargetList:
                img = target.reset(f)
            for agent in AgentList:
                #print(agent.getQcount())
                img = agent.reset(f)
            Count += 1
            print(str(Count) + ":" + str(Step))
            Result.append(Step)
            Step = 0
            cv2.destroyAllWindows()


    # END LOOP

    # Q値の表示
        ## 確保エージェント--AgentX
    if AgentLogic == 'Y':
        for agent in AgentList:
            agent.showQ()
        ## 確保エージェント--AgentW
    if AgentLogic == 'W':
        for agent in AgentList:
            agent.showQ()


    # 結果のグラフ化----------------------------------------------------
    average5 = []
    average10 = []
    average50 = []
    total = 0
    success = 0
    counter = buf5 = buf10 = buf50 = 0
    for idx in range(len(Result)):
        total += Result[idx]
        buf5 += Result[idx]
        buf10 += Result[idx]
        buf50 += Result[idx]
        if Result[idx] < MaxStep:
            success += 1
        if idx % 5 == 4:
            average5.append(buf5 / 5.0)
            buf5 = 0
        if idx % 10 == 9:
            average10.append(buf10 / 10.0)
            buf10 = 0
        if idx % 50 == 49:
            average50.append(buf50 / 50.0)
            buf50 = 0
    print("TOTAL AVERAGE: " + str(total / TrialCount))
    print("SUCCESS RATE: " + str(success / TrialCount * 100) + "%")
    pyplot.plot(range(len(Result)), Result, color='lightgray', label = "Steps")
    pyplot.plot([i * 5 for i in range(len(average5))], average5, color='blue', label = "Steps(Average 5)")
    pyplot.plot([i * 10 for i in range(len(average10))], average10, color='green', label = "Steps(Average 10)")
    pyplot.plot([i * 50 for i in range(len(average50))], average50, color='red', label = "Steps(Average 50)")
    if AgentLogic == 'Z':
        pyplot.title("Steps - Trials[AgentZ]")
    if AgentLogic == 'Y':
        pyplot.title("Steps - Trials[AgentY]")
    if AgentLogic == 'X':
        pyplot.title("Steps - Trials[AgentX]")
    if AgentLogic == 'W':
        pyplot.title("Steps - Trials[AgentW]")
    pyplot.xlabel("Trial Counts")
    pyplot.xlim([0, TrialCount])
    pyplot.ylabel("Steps")
    pyplot.ylim([0, MaxStep])
    pyplot.legend()
    pyplot.show()
