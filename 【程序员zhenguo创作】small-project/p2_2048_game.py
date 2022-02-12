# encoding: utf-8
"""
@file: tmp_test.py
@desc:
@author: guozhen3
@time: 2021/11/29
"""
from tkinter import *
from tkinter import messagebox
import random


class Board:
    """
    棋盘底层类
    """
    bg_color = {
        '2': '#eee4da',
        '4': '#ede0c8',
        '8': '#edc850',
        '16': '#edc53f',
        '32': '#f67c5f',
        '64': '#f65e3b',
        '128': '#edcf72',
        '256': '#edcc61',
        '512': '#f2b179',
        '1024': '#f59563',
        '2048': '#edc22e',
    }
    color = {
        '2': '#776e65',
        '4': '#f9f6f2',
        '8': '#f9f6f2',
        '16': '#f9f6f2',
        '32': '#f9f6f2',
        '64': '#f9f6f2',
        '128': '#f9f6f2',
        '256': '#f9f6f2',
        '512': '#776e65',
        '1024': '#f9f6f2',
        '2048': '#f9f6f2',
    }

    def __init__(self):
        self.n = 4
        self.window = Tk()
        self.window.title('程序员zhenguo 2048 Game')
        self.game_area = Frame(self.window, bg='azure3')
        self.board = []
        self.grid_cell = [[0] * 4 for _ in range(4)]
        self.compress = False
        self.merge = False
        self.moved = False
        self.score = 0

        for i in range(4):
            rows = []
            for j in range(4):
                l = Label(self.game_area, text='', bg='azure4',
                          font=('arial', 22, 'bold'), width=4, height=2)
                l.grid(row=i, column=j, padx=7, pady=7)
                rows.append(l)
            self.board.append(rows)
        self.game_area.grid()

    def reverse(self):
        """
        某行单元格值反转
        :return:
        """
        for ind in range(4):
            self.grid_cell[ind].reverse()

    def transpose(self):
        """
        二维数组转秩
        :return:
        """
        self.grid_cell = [list(t) for t in zip(*self.grid_cell)]

    def drifting_left(self):
        """
        向左偏流，消除0方格
        :return:
        """
        self.compress = False
        temp = [[0] * 4 for _ in range(4)]
        for i in range(4):
            # cnt：慢指针，j: 快指针
            cnt = 0
            for j in range(4):
                if self.grid_cell[i][j] != 0:
                    temp[i][cnt] = self.grid_cell[i][j]
                    if cnt != j:
                        self.compress = True
                    cnt += 1

        self.grid_cell = temp

    def merge_grid(self):
        """
        向左移动，合并邻近的两个非零相等单元格
        :return:
        """
        self.merge = False
        for i in range(4):
            for j in range(3):
                if self.grid_cell[i][j] == self.grid_cell[i][j + 1] and self.grid_cell[i][j] != 0:
                    self.grid_cell[i][j] *= 2
                    self.grid_cell[i][j + 1] = 0
                    self.score += self.grid_cell[i][j]
                    self.merge = True

    def random_cell(self):
        """
        从零单元格中随机产生一个2号单元格
        :return:
        """
        i, j = random.choice([(i, j) for i in range(4) for j in range(4) if self.grid_cell[i][j] == 0])
        self.grid_cell[i][j] = 2

    def can_merge(self):
        """
        判断是否需要存在邻近的两个非零相等单元格
        :return:
        """
        for i in range(4):
            for j in range(3):
                if self.grid_cell[i][j] == self.grid_cell[i][j + 1]:
                    return True

        for i in range(3):
            for j in range(4):
                if self.grid_cell[i][j] == self.grid_cell[i + 1][j]:
                    return True
        return False

    def paint_grid(self):
        """
        对应单元格着色对应的颜色，包括背景色、前景色
        :return:
        """
        for i in range(4):
            for j in range(4):
                if self.grid_cell[i][j] == 0:
                    self.board[i][j].config(text='', bg='azure4')
                else:
                    self.board[i][j].config(text=str(self.grid_cell[i][j]),
                                            bg=self.bg_color.get(str(self.grid_cell[i][j])),
                                            fg=self.color.get(str(self.grid_cell[i][j])))


class Game:
    """
    游戏事件和方法处理
    """
    def __init__(self, gamepanel):
        self.gamepanel = gamepanel
        self.end = False
        self.won = False

    def start(self):
        self.gamepanel.random_cell()
        self.gamepanel.random_cell()
        self.gamepanel.paint_grid()
        # 键盘按下事件: <Key>
        # event中的keysym, keycode, char都可以获取按下的键
        # 【其他想要获取值的也可以先看看event中有什么】
        self.gamepanel.window.bind('<Key>', self.event_handlers)
        self.gamepanel.window.mainloop()

    def event_handlers(self, event):
        """
        事件回调函数
        :param event:
        :return:
        """
        if self.end or self.won:
            return

        self.gamepanel.compress = False
        self.gamepanel.merge = False
        self.gamepanel.moved = False

        enter_key = event.keysym

        if enter_key == 'Up':
            self.gamepanel.transpose()
            self.gamepanel.drifting_left()
            self.gamepanel.merge_grid()
            self.gamepanel.moved = self.gamepanel.compress or self.gamepanel.merge
            self.gamepanel.drifting_left()
            self.gamepanel.transpose()

        elif enter_key == 'Down':
            self.gamepanel.transpose()
            self.gamepanel.reverse()
            self.gamepanel.drifting_left()
            self.gamepanel.merge_grid()
            self.gamepanel.moved = self.gamepanel.compress or self.gamepanel.merge
            self.gamepanel.drifting_left()
            self.gamepanel.reverse()
            self.gamepanel.transpose()

        elif enter_key == 'Left':
            self.gamepanel.drifting_left()
            self.gamepanel.merge_grid()
            self.gamepanel.moved = self.gamepanel.compress or self.gamepanel.merge
            self.gamepanel.drifting_left()

        elif enter_key == 'Right':
            self.gamepanel.reverse()
            self.gamepanel.drifting_left()
            self.gamepanel.merge_grid()
            self.gamepanel.moved = self.gamepanel.compress or self.gamepanel.merge
            self.gamepanel.drifting_left()
            self.gamepanel.reverse()

        self.gamepanel.paint_grid()
        print(self.gamepanel.score)

        flag = 0
        for i in range(4):
            for j in range(4):
                # 判断WIN
                if self.gamepanel.grid_cell[i][j] == 2048:
                    messagebox.showinfo('2048', message='You Wonnn!!')
                    print("won")
                    return

        for i in range(4):
            for j in range(4):
                if self.gamepanel.grid_cell[i][j] == 0:
                    flag = 1
                    break
        if not (flag or self.gamepanel.can_merge()):
            # 判断OVER
            self.end = True
            messagebox.showinfo('2048', 'Game Over!!!')
            print("Over")

        if self.gamepanel.moved:
            self.gamepanel.random_cell()

        self.gamepanel.paint_grid()


if __name__ == "__main__":
    gamepanel = Board()
    game2048 = Game(gamepanel)
    game2048.start()
