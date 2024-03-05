# coding=UTF-8

def init():
    # 事件时间差
    global eventTimeDelta

    # Q-Learning控制变量:当前尝试的次数, 成功次数,是否通过标识
    global Try, STry, passFlag

    # 初始显示标识
    global pressKey             # 记录按键事件的状态
    global scalingFlag          # 是否禁用缩放功能
    global promptDisplay        # 是否显示提示文字
    global collisionLineFlag    # 是否渲染碰撞线
    global forceReset           # 是否强制重置

    # 初始化: 事件时间差为0
    eventTimeDelta = 0.0

    # Q-learning 参数设置
    Try = 1
    STry = 0
    passFlag = False

    # 初始化控制变量
    pressKey = 0
    forceReset = False
    scalingFlag = False
    promptDisplay = True
    collisionLineFlag = True
