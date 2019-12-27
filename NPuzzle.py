#!/usr/bin/python
# -*- coding:utf-8 -*-

# Script Name   : NPuzzle.py
# Author        : QiaoWei(qiaowei1976@qq.com)
# Created       : 24th December 2019
# Version       : 1.0.0
#
# Description   : This is a 16-puzzle game. The level you can choose is: easy, medium, and high.
#                 It also shows the time elapse when you win.

from tkinter import *
from enum import Enum, unique, IntEnum
import time
import random

@unique
class Size(Enum):
    grid_width = 4
    grid_high = grid_width + 2
    btn_size = 60

class game_lv(IntEnum):
    EASY = 20
    MEDIUM = 200
    HIGH = 500

#direction: used to initialize the blocks
class Direction(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3

class Color():
    btn_bg = "tan"
    btn_fg = 'green'

class TimeElapse(object):
    def __init__(self, master = None):
        self.root = master
        self.old_time = round(time.time())
        self.current_elapse = 0
        self.create_lable()
        
    def reset(self):
        self.old_time = round(time.time())
        self.current_elapse = 0
        self.TimeLable['text'] = '00:00'

    def create_lable(self):
        #used for time elapse refresh_btn
        self.TimeLable = Button(self.root, text = '00:00', font = ('KaiTi', 24, 'bold'),
            bg = Color().btn_bg, fg = 'red')
        self.TimeLable.place(x = (0) * Size.btn_size.value, 
            y = (Size.grid_high.value - 1)  * Size.btn_size.value - int(Size.btn_size.value / 2), 
                    width = Size.btn_size.value*2, height = Size.btn_size.value)
        
    def update_clock(self):
        self.current_elapse = round(time.time())
        elapse = self.current_elapse - self.old_time
        elapse = time.strftime('%M:%S',time.localtime(elapse))  
        self.TimeLable['text'] = elapse     
        self.clock = self.root.after(1000, self.update_clock)
    
    def stop_clock(self):
        self.root.after_cancel(self.clock) 

class Numbers(object):
    def __init__(self, master = None):
        self.root = master
        self.blocks = [[0]*Size.grid_width.value for i in range(Size.grid_width.value)]
        self.row_0 = 0
        self.column_0 = 0
        self.level = game_lv.EASY
        
    def init_data(self):
        self.nums = list(range(1, Size.grid_width.value*Size.grid_width.value))
        self.nums.append(0)

        #add to the 2d array.
        for row in range(Size.grid_width.value):
            for column in range(Size.grid_width.value):
                temp = self.nums[row * Size.grid_width.value + column]
                if temp == 0:
                    self.row_0 = row
                    self.column_0 = column
                self.blocks[row][column] = temp

        #make the data of the blocks randomly.
        for i in range(self.level):
            random_num = random.randint(0, 3)
            self.move(Direction(random_num))
			
    def move(self, direction):
        if(direction == Direction.UP):
            if self.row_0 != Size.grid_width.value - 1:
                self.blocks[self.row_0][self.column_0] = self.blocks[self.row_0 + 1][self.column_0]
                self.blocks[self.row_0 + 1][self.column_0] = 0
                self.row_0 += 1
				
        if(direction == Direction.DOWN):
            if self.row_0 != 0:
                self.blocks[self.row_0][self.column_0] = self.blocks[self.row_0 - 1][self.column_0]
                self.blocks[self.row_0 - 1][self.column_0] = 0
                self.row_0 -= 1
				
        if(direction == Direction.LEFT):
            if self.column_0 != Size.grid_width.value - 1:
                self.blocks[self.row_0][self.column_0] = self.blocks[self.row_0][self.column_0 + 1]
                self.blocks[self.row_0][self.column_0 + 1] = 0
                self.column_0 += 1
				
        if(direction == Direction.RIGHT): 
            if self.column_0 != 0:
                self.blocks[self.row_0][self.column_0] = self.blocks[self.row_0][self.column_0 - 1]
                self.blocks[self.row_0][self.column_0 - 1] = 0
                self.column_0 -= 1

    def check_result(self):
        if self.blocks[Size.grid_width.value-1][Size.grid_width.value-1] != 0:
            return False

        for row in range(Size.grid_width.value):
            for column in range(Size.grid_width.value):
                if row == (Size.grid_width.value-1) and column == (Size.grid_width.value - 1):
                    pass
                elif self.blocks[row][column] != row * Size.grid_width.value + column + 1:
                    return False
        return True

class NPuzzle(object):
    def __init__(self, master, t, num, btn):
        self.root = master
        self.root.title("NPuzzle")
        self.t = t
        self.num = num
        self.num.init_data()

        self.dim_str = str(Size.grid_width.value*Size.btn_size.value) + 'x' + \
            str(int(Size.grid_high.value*Size.btn_size.value - Size.btn_size.value/2))
        self.root.geometry(self.dim_str)

        self.root.resizable(0,0)

        #Paint the panel
        self.btn_button = btn
        self.create_panel()
        
        while (self.num.check_result()):
            self.num.init_data()
        self.refresh_btn()

    def update_level(self, level):
        #level = game_lv.EASY, game_lv.MEDIUM, game_lv.HIGH, in this situation.
        #it need the change the difficult leave, and reset the panel.
        self.reflesh_panel(level)

    def btn_reset_clicked(self):
        #0 means reset button, do not need to change the level.
        self.reflesh_panel(0)

    def reflesh_panel(self, level):
        if level != 0:
            self.num.level = level
        
        #restore the button of the zero
        self.btn_button[self.num.row_0][self.num.column_0].place(y = self.num.row_0 * Size.btn_size.value,
            x = self.num.column_0 * Size.btn_size.value, 
            width = Size.btn_size.value, height = Size.btn_size.value)

        #reset the data 
        self.num.init_data()
        while (self.num.check_result()):
            self.num.init_data()

        #reset the timer
        self.t.reset()
        if self.ctl_btn['text'] == 'Start' and level == 0:
            self.ctl_btn['text'] = 'Reset'
            self.t.update_clock()

        #only update the level
        if self.ctl_btn['text'] == 'Start' and level != 0:
            pass
        
        #update the level, stop and rest the timer
        if self.ctl_btn['text'] == 'Reset' and level != 0:
            self.ctl_btn['text'] = 'Start'
            self.t.reset()
            self.t.stop_clock()

        self.refresh_btn()

    def refresh_btn(self):
        for row in range(Size.grid_width.value):
            for column in range(Size.grid_width.value):
                self.btn_button[row][column]["text"] = str(self.num.blocks[row][column])
        self.btn_button[self.num.row_0][self.num.column_0].place_forget()

    def btn_clicked_common(self, x, y):
        #print(x, y)
        if (self.num.check_result() == True):
            return
        
        direction = Direction.RIGHT

        if self.ctl_btn['text'] == 'Start':
            self.ctl_btn['text'] = 'Reset'
            self.t.reset()
            self.t.update_clock()

        if (abs(x-self.num.row_0) + abs(y-self.num.column_0)) == 1:
            if x-self.num.row_0 == 1:
                direction = Direction.UP
            elif x-self.num.row_0 == -1:
                direction = Direction.DOWN
            elif y-self.num.column_0 == 1:
                direction = Direction.LEFT
            elif y-self.num.column_0 == -1:
                direction = Direction.RIGHT
            
            #restore the button of the zero
            self.btn_button[self.num.row_0][self.num.column_0].place(y = self.num.row_0 * Size.btn_size.value,
                x = self.num.column_0 * Size.btn_size.value, 
                width = Size.btn_size.value, height = Size.btn_size.value)

            #switch the button
            self.num.move(direction)
            if (self.num.check_result() == True):
                self.ctl_btn['text'] = 'Start'
                self.t.stop_clock()

            self.refresh_btn()    


    def create_panel(self):
        #Creat the first number button.
        for  row in range(Size.grid_width.value):
            for column in range(Size.grid_width.value):
                btn = Button(self.root, text = str(0), font = ('KaiTi', 24, 'bold'),
                    bg = Color().btn_bg, fg = Color().btn_fg, command = lambda x = row, 
					y = column:self.btn_clicked_common(x, y))
                btn.place(y = row * Size.btn_size.value, x = column * Size.btn_size.value, 
                    width = Size.btn_size.value, height = Size.btn_size.value)
                self.btn_button[row][column] = btn

        #the reset button here.
        self.ctl_btn = Button(self.root, text = 'Start', font = ('KaiTi', 24, 'bold'),
            bg = Color().btn_bg, fg = Color().btn_fg, command = lambda:self.btn_reset_clicked())
        self.ctl_btn.place(x = (Size.grid_width.value - 2) * Size.btn_size.value, 
            y = (Size.grid_high.value - 1)  * Size.btn_size.value - int(Size.btn_size.value / 2), 
            width = Size.btn_size.value*2, height = Size.btn_size.value)

class level(NPuzzle):
    def __init__(self, master, t, num, btn):
        super().__init__(master, t, num, btn)
        
        self.EASY = (float)(game_lv.EASY)
        self.MEDIUM = (float)(game_lv.MEDIUM)
        self.HIGH = (float)(game_lv.HIGH)
        self.defualt = (float)(game_lv.EASY)

        Lv_info = [('Easy', self.EASY, 0, 4), ('Medium', self.MEDIUM, 1, 9), ('High', self.HIGH, 2, 7)]

        self.value = IntVar()
        self.value.set(self.defualt)

        for lv, num, posx, posx_bias in Lv_info:
            radio = Radiobutton(self.root, text = lv, value = num, bg = Color().btn_bg, fg = 'black',
                command = self.btn_radio_clicked, font = ('Kailti', 9, 'normal'), variable = self.value)
            radio.place(x = (posx/3.0 * Size.btn_size.value) * Size.grid_width.value - posx_bias, 
				y = (Size.grid_high.value - 2)  * Size.btn_size.value, 
                width = Size.btn_size.value*1.5, height = Size.btn_size.value/2)

    def set_default_level(self):
        self.defualt = self.value.get()

    def btn_radio_clicked(self):
        self.set_default_level()
        self.update_level(self.defualt)
        
if __name__ == '__main__':
    root = Tk()
    root.title("NPuzzle")

    t = TimeElapse(root)
    num = Numbers()

    #the button need to be fresh.
    btn = [[0]*Size.grid_width.value for i in range(Size.grid_width.value)]
    #level is derived from NPuzzle.
    #class level(NPuzzle):
    level(root, t, num, btn)

    root.mainloop()