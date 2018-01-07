#!/usr/bin/python
# -*- coding: utf-8 -*-

from SketchWindow import *
from Crash_tolerant import *

MY_APP_VERSION_STRING = "v1.0"


class SketchFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, -1, "Crash tolerant consensus", size=(800, 600))
        self.sketch = SketchWindow(self, -1)
        self.sketch.Bind(wx.EVT_MOTION, self.OnSketchMotion)
        self.initStatusBar()
        self.createMenuBar()
        self.createPanel()

        # create a pubsub receiver
        pub.subscribe(self.updateDisplay, 'update')

    def updateDisplay(self, msg):
        """
        Receives data from thread and updates the display
        """
        t = msg
        if isinstance(t, str):
            self.statusbar.SetStatusText(t, 2)
        else:
            (index, value, Round) = t
            self.sketch.setValue(index, value)
            
    def initStatusBar(self):
        self.statusbar = self.CreateStatusBar()
        self.statusbar.SetFieldsCount(3)
        self.statusbar.SetStatusWidths([-1, -2, -3])

    def OnSketchMotion(self, event):
        self.statusbar.SetStatusText("Pos: %s" %
                                     str(event.GetPositionTuple()), 0)
        self.statusbar.SetStatusText("Node Count: %s" %
                                     len(self.sketch.nodes), 1)
        event.Skip()

    def menuData(self):  # 2 菜单数据
        return [("Run", (
            ("Start", "Start communicating", self.OnRun),
            ("Clear", "Clear all nodes", self.OnClear)))] + [("Help", (
            ("About", "Information about this app", self.OnAbout),
            ("Exit", "Quit", self.OnCloseWindow))
            )]

    def OnClear(self, e):
        print "Clear..."
        self.sketch.clear()

    def OnRun(self, e):
        self.fail = [0, 1]  # Fail节点
        self.threads = []  # 线程列表

        nodes = [self.sketch.nodes[i][3] for i in range(len(self.sketch.nodes))]  # 所有节点的IP
        values = [self.sketch.nodes[i][4]
                  for i in range(len(self.sketch.nodes))]  # 节点初始值
        print("Crash list : ")
        print(self.fail)
        for i in range(len(self.fail), len(self.sketch.nodes)):
            self.fail.append(None)
        print("\nNode's original values : ")
        print(values)
        print("\nThe smallest is: %d\n" % min(values))

        self.statusbar.SetStatusText("Start...", 2)
        # 创建线程
        for i in range(len(nodes)):
            t = ThreadNode(nodes[i], values[i], nodes, i, self.fail)
            self.threads.append(t)

        self.statusbar.SetStatusText("Communicating...", 2)    

    def createMenuBar(self):
        menuBar = wx.MenuBar()
        for eachMenuData in self.menuData():
            menuLabel = eachMenuData[0]
            menuItems = eachMenuData[1]
            menuBar.Append(self.createMenu(menuItems), menuLabel)
        self.SetMenuBar(menuBar)

    def createMenu(self, menuData):
        menu = wx.Menu()
#3 创建子菜单
        for eachItem in menuData:
            if len(eachItem) == 2:
                label = eachItem[0]
                subMenu = self.createMenu(eachItem[1])
                menu.AppendMenu(wx.NewId(), label, subMenu)

            else:
                self.createMenuItem(menu, *eachItem)
        return menu

    def createMenuItem(self, menu, label, status, handler,
                       kind=wx.ITEM_NORMAL):
        if not label:
            menu.AppendSeparator()
            return
        menuItem = menu.Append(-1, label, status, kind)  # 4 使用kind创建菜单项
        self.Bind(wx.EVT_MENU, handler, menuItem)

    def OnColor(self, event):  # 5 处理颜色的改变
        menubar = self.GetMenuBar()
        itemId = event.GetId()
        item = menubar.FindItemById(itemId)
        color = item.GetLabel()
        self.sketch.SetColor(color)

    def OnCloseWindow(self, event):
        self.Destroy()

    def OnAbout(self, event):
        aboutInfo = wx.AboutDialogInfo()
        aboutInfo.SetName("Crash tolerant consensus")
        aboutInfo.SetVersion(MY_APP_VERSION_STRING)
        aboutInfo.SetDescription("This app is used to simulate crash tolerant consensus with f-resilient algorithm.")
        aboutInfo.SetCopyright("(C) 2017")
        aboutInfo.AddDeveloper("Haimin Luo, Chao Dong and Jinhui Zhu from HUST CS, Wuhan, China")
        wx.AboutBox(aboutInfo)

    def createPanel(self):
        box = wx.BoxSizer(wx.HORIZONTAL)
        box.Add(self.sketch, 1, wx.EXPAND)
        self.SetSizer(box)


class SketchApp(wx.App):
    def OnInit(self):
        frame = SketchFrame(None)
        frame.Show(True)
        self.SetTopWindow(frame)
        return True

if __name__ == '__main__':
    app = SketchApp()
    if app:
        app.MainLoop()
