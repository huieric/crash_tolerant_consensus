# This Python file uses the following encoding: utf-8

#########################################
# 程序接收三个参数，第一、二各参数为节点初始值范围
# 第三个参数为全部节点相应的IP地址
#########################################

from threading import Thread
from wx.lib.pubsub import setupkwargs
from wx.lib.pubsub import pub
import wx
import sys
import socket
import pickle
import time
import random
from Queue import Queue

# 定义线程可执行类，模拟节点


class ThreadNode(Thread):

    def __init__(self, addr, val, targets, index, fail):
        Thread.__init__(self)
        self.skt = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.addr = addr
        self.args = (self.skt, val, targets, index, fail)
        self.skt.bind(addr)
        self.start()
        print("Threadode %d start with ip %s:%s with value %d" %
              (index, addr[0], addr[1], val))

    def run(self):
        skt = self.args[0]
        fst = self.args[1]  # 初始值
        targets = self.args[2]
        idx = self.args[3]  # 节点号
        fail = self.args[4]
        rcvd = [fst]  # 接收到的其余节点所有的值，初始化为自身的值
        Round = 0  # 轮数
        while True:
            if Round >= len(targets):  # 最对其余所有节点数的轮数结束
                break

            # 向其余节点发送本节点所有的值
            for i in range(len(targets)):
                if i == idx:
                    continue
                skt.sendto(pickle.dumps(fst), targets[i])
                # pub.sendMessage(
                #     'update', msg="Node %d sends node %d value %d" % (idx, i, fst))

                # 模拟节点crash
                if fail[Round] != None:
                    if fail[Round] == idx and i == fail[Round] + 5:
                        print("Node %d crash during round %d!" % (idx, Round))
                        # wx.CallAfter(pub.sendMessage, "Node %d crash during round %d!" % (idx, Round))
                        pub.sendMessage('update', msg="Node %d crash during round %d!" % (idx, Round))
                        return

            # 未收到要求数量的其余节点信息的节点，持续监听
            if len(rcvd) < len(targets):
                while True:
                    t, addr = skt.recvfrom(4096)
                    rcvd.append(pickle.loads(t))
                    fst = min(rcvd)
                    if len(rcvd) == len(targets):
                        break
            Round = Round + 1
            # time.sleep(0.5)
        print("index: %d, val: %d, round: %d" % (idx, fst, Round))
        # wx.CallAfter(pub.sendMessage, "update", (idx, fst, Round))
        pub.sendMessage('update', msg=(idx, fst, Round))

# 分割IP


def toAddr(s):
    addr = s.split(":")
    return addr[0], int(addr[1])

# 产生随机列表


def random_int_list(start, stop, length):
    start, stop = (int(start), int(stop)) if start <= stop else (
        int(stop), int(start))
    length = int(abs(length)) if length else 0
    random_list = []
    for i in range(length):
        dc = wx.BufferedDC(wx.ClientDC(self), self.buffer)
        random_list.append(random.randint(start, stop))
    return random_list

