# coding=UTF-8

import Player as player
import Render as renderModel
import State as stateModel

def init():
    global init_v, init_r                           # 初始速度与角度
    global nTracks, sTrack                          # 地图总数与选择的地图
    global init_dir, init_posx, init_posy           # 初始化方向和x,y坐标
    global trackNames, trackTopMap, trackBaseMap    # 地图名称, 顶图, 底图

    # 初始化
    sTrack = 0
    nTracks = 4
    trackNames = ["Map 1",
                  "Map 2",
                  "Map 3",
                  "Map 4"]

    trackTopMap = ["model_1.png",
                   "model_2.png",
                   "model_3.png",
                   "model_4.png"]

    trackBaseMap = ["model_1_map.png",
                    "model_2_map.png",
                    "model_3_map.png",
                    "model_4_map.png"]

    init_posx = [312.0, 215, 475, 805]
    init_posy = [495.0, 520, 795, 570]

    init_dir = [[0.0, -1.0],
                [0.0, -1.0],
                [0.0, -1.0],
                [0.0, -1.0]]

    init_v= [1.0, 1.0, 1.0, 1.0]

    init_r = [90.0, 90.0, 180.0, 270.0]


# 导入地图
def ldTrack():
    global init_v, init_r
    global sTrack, nTracks
    global trackTopMap, trackBaseMap
    global init_posx, init_posy, init_dir

    if (sTrack >= nTracks):
        sTrack = 0
    # 导入图片进行渲染
    renderModel.track = loadImage(trackTopMap[sTrack])
    renderModel.trackBaseMap = loadImage(trackBaseMap[sTrack])

    # 初始化玩家参数
    player.v = init_v[sTrack]
    player.r = init_r[sTrack]
    player.dir = init_dir[sTrack]
    player.posx = init_posx[sTrack]
    player.posy = init_posy[sTrack]

    # 初始化状态
    stateModel.init()


# 初始化玩家
def initplayer():
    global init_v, init_r
    global sTrack, nTracks
    global init_posx, init_posy, init_dir

    if (sTrack >= nTracks):
        sTrack = 0

    # 初始化赋值
    player.v = init_v[sTrack]
    player.r = init_r[sTrack]
    player.dir = init_dir[sTrack]
    player.posx = init_posx[sTrack]
    player.posy = init_posy[sTrack]


# 初始化渲染器
def initrender():
    global sTrack, nTracks
    global trackNames, trackTopMap,trackBaseMap

    if (sTrack >= nTracks):
        sTrack = 0

    # 地图导入并渲染
    renderModel.track = loadImage(trackTopMap[sTrack])
    renderModel.trackBaseMap = loadImage(trackBaseMap[sTrack])
    print("Loaded track: "+trackNames[sTrack])


# 更换地图
def setTrack(number):
    global sTrack, nTracks

    if (number >= nTracks or number < 0):
        return

    sTrack = number
