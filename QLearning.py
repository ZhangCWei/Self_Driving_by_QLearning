# coding=UTF-8

import Player as player
import State as stateModel


def init():
    # q-learning的超参数
    global scores, qTable, alpha, gamma

    # 分数初始化
    scores = 0.0

    # 超参数选择
    alpha = 0.1
    gamma = 0.9

    # 状态state有2^7=128种, 动作有3种
    qTable = [[0.0 for row in range(3)] for col in range(128)]


# 保存Q-Table
def saveQTableToFile():
    global qTable
    with open("Q_Table.txt", 'w') as file:
        for row in qTable:
            file.write(','.join(map(str, row)) + '\n')


# 导入Q-Table
def loadQTableFromFile():
    q_table = []
    with open("Q_Table.txt", 'r') as file:
        for line in file:
            row = [float(value) for value in line.strip().split(',')]
            q_table.append(row)
    print("Data Loading Successful!")
    return q_table


# 奖赏函数
def getReward(action):
    global scores

    # 初始 0 分
    scores = 0.0
    if (player.isAlive):
        if any(stateModel.state):
            # 如果有碰撞检测线点未检测出碰撞，给出对应分数
            scores = 5.0 - (1.0 - stateModel.distFront) * 60.0
        else:
            # 如果所有检测线都没有检测出碰撞
            if (action == 0):
                # 汽车直行，分数=20
                scores = 20.0
            else:
                # 汽车采取左转或右转
                scores = 10.0
    else:
        # 如果车撞到障碍了，游戏重新开始，并给予惩罚
        scores = -3000.0

    return scores


# 计算状态
def calcualate_state():
    new_st = 0
    for n in range(0, len(stateModel.state)):
        new_st = new_st + (2 ** n) * int(stateModel.state[n])
    return new_st


# 选择动作
def select_action(state, epsilon):
    global qTable

    selected_a = 0
    val = -float("inf")

    # ε-greedy贪心，选择动作
    for n in range(0, 3):
        if (qTable[state][n] > val):
            selected_a = n
            val = qTable[state][n]

    # 如果epsilon为True, 用ε-贪心策略选择动作
    # 如果生成的随机数大于给定的ε, 则随机选择一个动作;否则就保持前面用贪心策略得到的动作
    if epsilon and random(0, 100) >= 99:
        selected_a = floor(random(0, 3))

    return selected_a


# 执行选择的动作
def perform(action):
    # 执行动作
    if (action == 1):
        player.turnLeft()
    if (action == 2):
        player.turnRight()

    # 计算下一状态
    player.run()
    player.updatePosition()
    player.checkBounds()
    stateModel.calculate_Testpoints()
    stateModel.updateState()


def qLearning():
    global qTable, alpha, gamma

    # 得到当前状态
    current_state = calcualate_state()

    # 为当前状态选择动作（行为策略：ε-greedy）
    action = select_action(current_state, True)

    # 执行动作
    perform(action)

    # 采样得到奖赏, 更新Q-table
    reward = getReward(action)

    # 得到跳转到的下一个状态
    fstate = calcualate_state()

    # 更新Q-table时选择maxq对应的动作（目标策略：greedy）
    faction = select_action(fstate, False)

    # 更新Q-table
    qTable[current_state][action] = qTable[current_state][action] + alpha * (reward + gamma * qTable[fstate][faction] - qTable[current_state][action])
