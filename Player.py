# coding=UTF-8

import Global as gModel
import Render as renderModel
import Track as trackModel
import QLearning as qModel
from math import cos, sin, radians, floor

# 初始化游戏
def init():
    # 全局变量声明
    global v, r, bias               # 速度, 旋转角度与偏移
    global posx, posy, dir          # x坐标位置, y坐标位置与方向
    global isAI, isAlive, flag      # 是否为AI, 车辆是否存活, 限定游戏开始时选择AI还是人玩, 开始后不能再改变
    global frames, best, started    # 时间数据

    # 初始化玩家数据
    trackModel.initplayer()
    bias = 0.0
    best = 0.0
    frames = 0.0
    isAI = True
    flag = True
    isAlive = True
    started = True


# 更新玩家位置
def updatePosition():
    # 玩家数据
    global posx, posy, dir, v, r, bias

    # 方向向量更新
    r2radians = radians(r)      # 将旋转角度转换为弧度
    dir[0] = cos(r2radians)     # 计算X方向上的方向向量
    dir[1] = -sin(r2radians)    # 计算Y方向上的方向向量

    # 近似
    if -1e-4 < dir[0] < 1e-4:
        dir[0] = 0.0
    if -1e-4 < dir[1] < 1e-4:
        dir[1] = 0.0

    # 旋转角度更新计算
    r = r % 360
    r = r + bias / 30.0  # 根据车辆的偏移bias更新旋转角度

    # 速度范围约束
    v = max(0.2, min(v, 2.0))

    # 位置更新计算
    posx = posx + dir[0] * v  # 根据X方向上的方向向量和速度更新X坐标
    posy = posy + dir[1] * v  # 根据Y方向上的方向向量和速度更新Y坐标

    # 偏移重置计算
    if gModel.pressKey == 0:
        bias = 9.0 / 10.0 * bias  # 根据偏移的十分之一减小偏移
        if (-1e-4 < bias < 1e-4):
            bias = 0.0
    if gModel.pressKey > 0:
        gModel.pressKey = gModel.pressKey - 1  # 如果按键按下，减小按键按下的计数


# 检查玩家是否存活
def checkBounds():
    global isAlive
    if not getTrack():
        isAlive = False


# 获取车道信息
def getTrack():
    global posx, posy

    # 获取小车中心点的像素信息
    c = renderModel.trackBaseMap.pixels[int(posx) + int(posy) * 1024]

    if floor(red(c)) <= 15 and floor(green(c)) >= 240:
        # 判断是否成功越过终点线
        if floor(blue(c)) >= 240:
            gModel.passFlag = True
        else:
            if gModel.passFlag:
                gModel.STry = gModel.STry + 1
                print(" # Finish line crossed at try " + str(gModel.Try))
                print(" # Timestamp: " + str(frames) + " frames.")
                print(" # Total Successful laps: " + str(gModel.STry) + ". ")
                gModel.passFlag = False
        return True
    else:
        return False


# 向左转
def turnLeft():
    global bias, isAlive

    # 如果玩家已死亡，则退出函数
    if not isAlive:
        return

    # 设置状态为2
    gModel.pressKey = 2

    # 角度偏移
    if bias < 30.0:
        if bias < 0.0:
            bias = bias + 25.0
        bias = bias + 20.0


# 向右转
def turnRight():
    global bias, isAlive

    # 如果玩家已死亡，则退出函数
    if not isAlive:
        return

    # 设置状态为2
    gModel.pressKey = 2

    # 角度偏移
    if bias > -30.0:
        if bias > 0.0:
            bias = bias - 25.0
        bias = bias - 20.0


# 向左漂移
def driftLeft():
    global v, bias, isAlive

    # 如果玩家已死亡，则退出函数
    if not isAlive:
        return

    # 设置状态为2
    gModel.pressKey = 2

    # 角度偏移与速度增加
    if bias < 30.0:
        if bias < 0.0:
            bias = bias + 25.0
        bias = bias + 50.0
        v = v + 0.1


# 向右漂移
def driftRight():
    global v, bias, isAlive

    # 如果玩家已死亡，则退出函数
    if not isAlive:
        return

    # 设置状态为2
    gModel.pressKey = 2

    # 角度偏移与速度增加
    if bias > -30.0:
        if bias > 0.0:
            bias = bias - 25.0
        bias = bias - 50.0
        v = v + 0.1


# 加速
def accel():
    global isAlive, v
    # 如果玩家已死亡，则退出函数
    if not isAlive:
        return
    # 速度增加0.1
    v = v + 0.1


# 减速
def deccel():
    global isAlive, v
    # 如果玩家已死亡，则退出函数
    if not isAlive:
        return
    # 速度减少0.1
    v = v - 0.1


# 重置游戏状态
def resetGame():
    global bias, isAlive
    # 载入轨道
    trackModel.ldTrack()
    # 重置计时器
    resetTimer()
    # 分数重置为0.0
    qModel.scores = 0.0
    # 偏移重置为0.0
    bias = 0.0
    # 玩家状态设为存活
    isAlive = True
    # 按键状态设为0
    gModel.pressKey = 0
    # 强制重置标志设为False
    gModel.forceReset = False


# 重置计时器
def resetTimer():
    global frames, best
    # 计算最优时间, 重置时间帧
    best = max(frames, best)
    frames = 0.0


# 运行游戏
def run():
    global frames, started
    if started:
        frames = frames + 1