# coding=UTF-8

import Render as renderModel
import Player as player

def init():
    # 状态变量
    global state, ranges, distFront, testPoints

    # 检测碰撞是否发生的范围
    distFront = 1.0
    ranges = [i * 0.05 for i in range(21)]
    testPoints = [[0.0, 0.0] for _ in range(7)]
    state = [False, False, False, False, False, False, False]

    calculate_Testpoints()


# 计算碰撞检测点坐标
def calculate_Testpoints():
    global testPoints

    r2radians = radians(player.r)
    veint = radians(20)

    angles = [PI / 2, PI / 4, veint, 0, -veint, -PI / 4, -PI / 2]
    distances = [20, 40, 45, 50, 45, 40, 20]

    for i in range(len(testPoints)):
        testPoints[i][0] = distances[i] * cos(r2radians + angles[i])
        testPoints[i][1] = -distances[i] * sin(r2radians + angles[i])

    testPoints[3][0] = 50 * player.dir[0]
    testPoints[3][1] = 50 * player.dir[1]


# 绘制车头前面的7条碰撞检测线-无缩放
def NoScaleTestlines():
    global state, testPoints

    for n in range(0, len(testPoints)):
        if (state[n]):
            stroke(255, 255, 0)
        else:
            stroke(0)
        line(width / 2, height / 2, width / 2 + testPoints[n][0], height / 2 + testPoints[n][1])


# 绘制车头前面的7条碰撞检测线-有缩放
def Testlines():
    global state, testPoints

    for n in range(0, len(testPoints)):
        if (state[n]):
            stroke(255, 255, 0)  # 黄色
        else:
            stroke(0)  # 黑色
        line(width / 2, height / 2, width / 2 + testPoints[n][0] * renderModel.scale, height / 2 + testPoints[n][1] * renderModel.scale)


# 更新状态
def updateState():
    global state
    for n in range(0, len(testPoints)):
        state[n] = checkColl(n)


# 检查该碰撞检测点是否发生碰撞
def checkColl(n):
    global ranges, testPoints, distFront

    for i in range(0, len(ranges)):
        nx = player.posx + ranges[i] * testPoints[n][0]
        ny = player.posy + ranges[i] * testPoints[n][1]
        if not getTrack(nx, ny):
            if n == 3:
                # 在QLearning中获得奖赏时有用
                distFront = ranges[i]
            return True

    if n == 3:
        # 在QLearning中获得奖赏时有用
        distFront = 1.0

    return False


# 取赛道地图上指定位置 (x, y) 处的信息，检测该像素点是否可通过
def getTrack(x, y):
    # 计算像素点颜色
    c = renderModel.trackBaseMap.pixels[int(x) + 1024 * int(y)]
    if (floor(red(c)) <= 15 and floor(green(c)) >= 240):
        # (0, 255, *) 这样的颜色（*表示任意值），表示这个位置可通过
        return True
    # 其他像素点颜色不可通过
    return False
