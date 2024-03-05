import Player as player
import Global as gModel
import QLearning as qModel
import Track as trackModel
import State as stateModel
import Render as renderModel


def setup():
    # 初始化：设置画布大小
    size(1280, 720)

    # 初始化各模块
    gModel.init()
    trackModel.init()
    renderModel.init()
    player.init()
    stateModel.init()
    qModel.init()

     # 设置帧速率为999帧每秒
    frameRate(999)

    # 关闭平滑处理
    noSmooth()
    # 加载画布上的像素数据到程序中
    loadPixels()
    # 加载赛道地图的像素数据
    renderModel.trackBaseMap.loadPixels()


def draw():
    gModel.eventTimeDelta = 1.0/frameRate

    # 画布的背景设置为黑色
    background(0)
    if (not gModel.scalingFlag):
        renderModel.AltRenderer()
    else:
        renderModel.NoAltRenderer()

    if(player.flag == False):
        if (player.isAlive):
            # 玩家是电脑，则开启训练模式
            if (player.isAI):
                qModel.qLearning()     # 学习
                if (gModel.forceReset):
                    player.resetGame()
                if (not player.isAlive):
                    print("-AI died in try "+str(gModel.Try)+". Timestamp: "+str(player.frames)+" frames.")
                    gModel.Try = gModel.Try+1
                    player.resetGame()
                if (gModel.Try + gModel.STry) % 30 == 0:
                    qModel.saveQTableToFile()
            # 玩家是人
            else:
                player.run()
                player.updatePosition()
                player.checkBounds()
                stateModel.calculate_Testpoints()
                stateModel.updateState()
                if (not player.isAlive or gModel.forceReset):
                    player.resetGame()
    
    # 信息显示
    if (gModel.promptDisplay):
        renderModel.drawBegin()
        renderModel.drawPrompt()

# 键盘控件
def keyPressed():
    # 游戏开始前选择玩家是AI自动玩还是人玩
    if(player.flag == True):
        if key == 'j' or key == 'J':
            # AI玩
            player.isAI = True
            player.flag = False
            print("you are AI!")
            qModel.qTable = qModel.loadQTableFromFile()
        if key == 'k' or key == 'K':
            # 人玩
            player.isAI = False
            player.flag = False
            print("you are people!")

    if player.isAI:
        if key == 'i' or key == 'I':
            qModel.qTable = [[0.0 for x in range(3)] for y in range(int(2**(len(stateModel.state))))]
            print("Q_Table has been initialized")

    if not player.isAI:
        if key == 'a' or key == 'A':
            player.turnLeft()
        if key == 'd' or key == 'D':
            player.turnRight()
        if key == 'w' or key == 'W':
            player.accel()
        if key == 's' or key == 'S':
            player.deccel()
        if key == 'q' or key == 'Q':
            player.driftLeft()
            player.v = player.v-0.1
        if key == 'e' or key == 'E':
            player.driftRight()
            player.v = player.v-0.1
        if key == ' ':
            player.resetTimer()

    if key == 'z' or key == 'Z':
        gModel.scalingFlag = not gModel.scalingFlag
    if key == 'h' or key == 'H':
        gModel.promptDisplay = not gModel.promptDisplay
    if key == 'l' or key == 'L':
        gModel.collisionLineFlag = not gModel.collisionLineFlag


    if key == '1' or key == '2' or key == '3' or key == '4':
        track_index = int(key) - 1
        trackModel.setTrack(track_index % trackModel.nTracks)
        gModel.forceReset = True
        print("Loaded track: " + trackModel.trackNames[trackModel.sTrack])
