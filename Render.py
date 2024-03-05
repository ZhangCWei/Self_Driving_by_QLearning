# coding=UTF-8

import Global as gModel
import Player as player
import State as stateModel
import Track as trackModel
import QLearning as qModel


def init():
    # 字体与缩放比例
    global font, scale

    # 车辆、赛道、赛道底图
    global car, track, trackBaseMap

    # 加载小车图像
    car = loadImage("car.png")

    # 设置缩放比例（整数）与字体
    scale = 3
    font = createFont("Hooge0553", 18)

    # 进行渲染
    trackModel.initrender()


def bordersText(txt, x, y):
    offsets = [(-1, 0), (-1, -1), (0, -1), (1, 0), (1, 1), (0, 1)]  # 不同方向的偏移

    fill(0)  # 设置文本的填充颜色为黑色
    for offset in offsets:
        text(txt, x + offset[0], y + offset[1])

    fill(255)  # 设置文本的填充颜色为白色
    text(txt, x, y)  # 在原始位置绘制文本


# 提示信息
def drawBegin():
    global font
    # 开始游戏的指南
    if (player.flag == True):
        textFont(font, 50)
        textAlign(CENTER, CENTER)
        bordersText("Tip:  Before playing, choose your player \n which 'j' or 'J' is AI play and 'k' or 'K' is people play", 670, 300)


def drawPrompt():
    global font
    # 右上角信息显示
    textFont(font, 18)
    textAlign(RIGHT)
    bordersText(trackModel.trackNames[trackModel.sTrack], width - 23, 20)
    bordersText("EPOCH " + str(gModel.Try), width - 23, 40)
    bordersText("TIME " + str(int(player.frames)), width - 23, 60)
    bordersText("BEST TIME " + str(int(player.best)), width - 23, 80)
    bordersText("REWARD " + str(int(qModel.scores)), width - 23, 100)


# 渲染模式，进行缩放
def AltRenderer():
    global car, track, scale

    # 显示赛道
    image(track, -(player.posx * scale) + (width / 2), -(player.posy * scale) + (height / 2), 1024 * scale, 1024 * scale)

    # 显示车辆
    pushMatrix()
    translate(width / 2, height / 2)
    rotate(radians(90.0 - player.r))
    rotate(radians(-player.bias))
    translate(-width / 2, -height / 2)
    image(car, (width / 2) - 10 * scale, (height / 2) - 22 * scale, 21 * scale, 45 * scale)
    popMatrix()

    # 绘制7条碰撞检测线
    if (gModel.collisionLineFlag):
        stateModel.Testlines()


# 渲染模式，未进行了缩放，原始尺寸显示
def NoAltRenderer():
    global car, track

    # 显示赛道
    image(track, -player.posx + (width / 2), -player.posy + (height / 2))

    # 显示车辆
    pushMatrix()
    translate(width / 2, height / 2)
    rotate(radians(90.0 - player.r))
    rotate(radians(-player.bias))
    translate(-width / 2, -height / 2)
    image(car, (width / 2) - 10, (height / 2) - 22)
    popMatrix()

    # 绘制7条碰撞检测线
    if (gModel.collisionLineFlag):
        stateModel.NoScaleTestlines()


