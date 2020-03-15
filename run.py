import tkinter as tk
import random
import copy, time

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.board_init()
        self.init_canvas()
        self.draw_grid()
        self.master.bind("<Right>", self.right_key)
        self.master.bind("<Left>", self.left_key)
        self.master.bind("<Up>", self.up_key)
        self.master.bind("<Down>", self.down_key)
        self.pack()

    def board_init(self):
        self.board = [[2,0,0,0],
                      [0,0,0,0],
                      [0,0,0,0],
                      [2,2,0,2]]
        r, c = random.randint(0,99)%3, random.randint(0,99)%3
        self.board[r][c] = 2

    def add_random_tile(self):
        empty_tiles = []
        for r in [0,1,2,3]:
            for c in [0,1,2,3]:
                if self.board[r][c] == 0:
                    empty_tiles.append((r,c))
        r,c=random.choice(empty_tiles)
        self.board[r][c] = 2


    def init_canvas(self):
        self.background = tk.Canvas(self.master, bg="yellow", height=600, width=600)
        self.update_canvas()
        self.background.pack()

    def update_canvas(self):
        self.add_random_tile()
        self.draw_canvas()
        self.background.pack()



    def draw_canvas(self):
        for r in [0,1,2,3]:
            for c in [0,1,2,3]:
                num = self.board[r][c]
                if num != 0:
                    self.draw_tile(100*(c+1), 100*(r+1), num)
                else:
                    self.erase_tile(100*(c+1), 100*(r+1))



    def draw_tile(self, x, y, i):
        self.background.create_rectangle(x, y, x+100, y+100, fill="red")
        self.background.create_text(x+50, y+50, text=i, font=("Sans-serif",50))

    def draw_grid(self):
        self.background.create_line(100, 100, 500, 100)
        self.background.create_line(100, 200, 500, 200)
        self.background.create_line(100, 300, 500, 300)
        self.background.create_line(100, 400, 500, 400)
        self.background.create_line(100, 500, 500, 500)
        self.background.create_line(100, 100, 100, 500)
        self.background.create_line(200, 100, 200, 500)
        self.background.create_line(300, 100, 300, 500)
        self.background.create_line(400, 100, 400, 500)
        self.background.create_line(500, 100, 500, 500)

    def right_key(self, event):
        self.shift_right()
        self.update_canvas()

    def shift_right(self):
        for r in [0,1,2,3]:
            new_r = []
            ptr = 3
            while ptr >= 0:
                num = self.board[r][ptr]
                # print(new_r)
                # cur num is not 0
                if num != 0:
                    prev_ptr = ptr-1
                    # prev num exists
                    if prev_ptr >= 0:
                        prev_num = self.board[r][prev_ptr]
                        # if prev num is 0
                        while prev_ptr >= 0 and self.board[r][prev_ptr] == 0:
                            # print("aaa")
                            prev_ptr -= 1
                            prev_num = self.board[r][prev_ptr] if prev_ptr >= 0 else prev_num
                        if prev_num == num:
                            # print("debug")
                            new_r.append(num*2)
                            ptr=prev_ptr-1
                        else:
                            new_r.append(num)
                            ptr=prev_ptr
                    else:
                        new_r.append(num)
                        ptr-=1
                else:
                    ptr-=1
            while len(new_r) != 4:
                new_r.append(0)
            new_r.reverse()
            self.board[r] = new_r

    def left_key(self, event):
        flipped_board = []
        for r in [3,2,1,0]:
            flipped_board.append(list(reversed(self.board[r])))
        self.board=flipped_board
        self.shift_right()
        correct_board = []
        for r in [3, 2, 1, 0]:
            correct_board.append(list(reversed(self.board[r])))
        self.board=correct_board
        self.update_canvas()

    def up_key(self, event):
        rotated_board = copy.deepcopy(self.board)
        for c in [0,1,2,3]:
            for r in [0,1,2,3]:
                rotated_board[c][3-r] = self.board[r][c]
        self.board=rotated_board
        self.shift_right()
        copy_board = copy.deepcopy(self.board)
        for c in [0,1,2,3]:
            for r in [0,1,2,3]:
                self.board[r][c] = copy_board[c][3-r]
        self.update_canvas()

    def down_key(self, event):
        rotated_board = copy.deepcopy(self.board)
        for c in [0, 1, 2, 3]:
            for r in [0, 1, 2, 3]:
                rotated_board[3-c][r] = self.board[r][c]
        self.board = rotated_board
        self.shift_right()
        copy_board = copy.deepcopy(self.board)
        for c in [0, 1, 2, 3]:
            for r in [0, 1, 2, 3]:
                self.board[r][c] = copy_board[3-c][r]
        self.update_canvas()

    def erase_tile(self, x, y):
        self.background.create_rectangle(x, y, x + 100, y + 100, fill="yellow")

    # def create_widgets(self):
    #     self.hi_there = tk.Button(self)
    #     self.hi_there["text"] = "Hello World\n(click me)"
    #     self.hi_there["command"] = self.say_hi
    #     self.hi_there.pack(side="top")
    #
    #     self.quit = tk.Button(self, text="QUIT", fg="red", command=self.master.destroy)
    #     self.quit.pack(side="bottom")
    #
    # def say_hi(self):
    #     print("hi there, everyone!")

if __name__ == '__main__':
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()