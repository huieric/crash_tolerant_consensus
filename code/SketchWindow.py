#!/usr/bin/python
# -*- coding: utf-8 -*-

import wx
import random

RADIUS = 30
MIN = 0
MAX = 10000

class SketchWindow(wx.Window):
    def __init__(self, parent, ID):
        wx.Window.__init__(self, parent, ID)
        self.SetBackgroundColour("White")
        self.color = "Black"
        self.thickness = 1
        self.pen = wx.Pen(self.color, self.thickness,
                          wx.SOLID)  # 1 创建一个wx.Pen对象
        self.nodes = []
        self.curNode = []
        self.pos = (0, 0)
        self.InitBuffer()

#2 连接事件
        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
        # self.Bind(wx.EVT_MOTION, self.OnMotion)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_IDLE, self.OnIdle)
        self.Bind(wx.EVT_PAINT, self.OnPaint)

    def InitBuffer(self):
        size = self.GetClientSize()
        self.width = size.width
        self.height = size.height

#3 创建一个缓存的设备上下文
        self.buffer = wx.EmptyBitmap(size.width, size.height)
        dc = wx.BufferedDC(None, self.buffer)

#4 使用设备上下文
        dc.SetBackground(wx.Brush(self.GetBackgroundColour()))
        dc.Clear()
        self.DrawNodes(dc)

        self.reInitBuffer = False

    def clear(self):
        self.nodes = []
        self.curNode = []
        self.pos = (0, 0)
        self.Show()
        print "Clearing done"

    def GetNodesData(self):
        return self.nodes[:]

    def SetNodesData(self, nodes):
        self.nodes = nodes[:]
        self.InitBuffer()
        self.Refresh()

    def OnLeftDown(self, event):        
        self.pos = event.GetPositionTuple()  # 5 得到鼠标的位置
        addr = ("127.0.0.1", 5000 + len(self.nodes))
        self.curNode = [self.pos[0], self.pos[1], RADIUS, addr, random.randint(MIN, MAX)]
        self.CaptureMouse()  # 6 捕获鼠标

    def OnLeftUp(self, event):
        if self.HasCapture():
            dc = wx.BufferedDC(wx.ClientDC(self), self.buffer)  # 9 创建另一个缓存的上下文 
            self.drawNode(dc, self.curNode)
            self.nodes.append(self.curNode)                   
            self.curNode = []
            self.ReleaseMouse()  # 7 释放鼠标   

    def drawNode(self, dc, node):
        dc.SetPen(self.pen)
        dc.DrawCircle(node[0], node[1], node[2])
        dc.DrawLabel(str(node[4]), (node[0], node[1], 5, -1), wx.ALIGN_CENTER)

    def setValue(self, i, value):
        # x = self.nodes[i][0]
        # y = self.nodes[i][1]
        # r = self.nodes[i][2]
        dc = wx.BufferedDC(wx.ClientDC(self), self.buffer)
        dc.SetPen(self.pen)
        # dc.DrawCircle(x, y, r)
        # dc.DrawLabel(str(value), (x, y, 5, -1), wx.ALIGN_CENTER)
        # print i, value, x, y
        self.nodes[i][4] = value
        self.DrawNodes(dc)


    def OnMotion(self, event):
        if event.Dragging() and event.LeftIsDown():  # 8 确定是否在拖动
            dc = wx.BufferedDC(wx.ClientDC(self), self.buffer)  # 9 创建另一个缓存的上下文
            self.drawMotion(dc, event) 
        event.Skip()
    #10 绘画到设备上下文

    def drawMotion(self, dc, event):
        dc.SetPen(self.pen)
        newPos = event.GetPositionTuple()
        coords = self.pos + newPos
        node = (coords[0], coords[1], RADIUS)
        self.curNode.append(node)
        dc.DrawCircle(*node)
        self.pos = newPos

    def OnSize(self, event):
        self.reInitBuffer = True  # 11 处理一个resize事件

    def OnIdle(self, event):  # 12 空闲时的处理
        if self.reInitBuffer:
            self.InitBuffer()
            self.Refresh(False)

    def OnPaint(self, event):
        dc = wx.BufferedPaintDC(self, self.buffer)  # 13 处理一个paint（描绘）请求

    #14 绘制所有的线条
    def DrawNodes(self, dc):
        for node in self.nodes:
            # size = self.GetClientSize()
            # node = (node[0] * size.width / self.width, node[1] * size.height / self.height, node[2], node[4])
            # self.width = size.width
            # self.height = size.height
            self.drawNode(dc, node)

    def SetColor(self, color):
        self.color = color
        self.pen = wx.Pen(self.color, self.thickness, wx.SOLID)

    def SetThickness(self, num):
        self.thickness = num
        self.pen = wx.Pen(self.color, self.thickness, wx.SOLID)
