from tkinter import *

class cell(Button):
    def __init__(self, i, j, value, logic, pos, master):
        Button.__init__(self, master)
        self._logic = logic
        self._value = value
        self._x = i
        self._y = j
        self._pos = pos
        self.configure( # khởi tạo
            fg='#1f1f1f', 
            font='arial',
            relief= 'groove',
            justify='center',
            text= str(self._value) if self._value != -1 else str("") 
        )


    def showColor(self, _width):
        if(self._logic):
            self.configure(bg= '#0870e1')
        else:
            self.configure(bg= '#FF0000')

        self.place(x=self._y*_width, y=self._x*_width, width=_width, height=_width) 


    def __repr__(self):
        return f"{self._value}"


class board(Frame):
    def __init__(self, master, matrix):
        Frame.__init__(self, master)
        self.configure(     # frame đã được kế thừa
            height = 700,
            width = 700,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
        )
        # khoi tao matrix
        self.m = len(matrix)
        self.n = len(matrix[0])
        # tao mot list cac cell
        self._board = []
        for i in range(self.m): # object cell[i][j].value
            tb = []
            for j in range(self.n):
                tb.append(cell(i, j, matrix[i][j], None, i * self.n + j + 1,self))
            self._board.append(tb)


    def getAdjacentCell(self, i, j):
        adj_lst = []
        if i-1 >= 0:
            adj_lst.append(self._board[i-1][j])
        if i+1 < len(self._board):
            adj_lst.append(self._board[i+1][j])
        if j-1 >= 0:
            adj_lst.append(self._board[i][j-1])
        if j+1 < len(self._board[0]):
            adj_lst.append(self._board[i][j+1])
        if i-1 >= 0 and j-1 >= 0:
            adj_lst.append(self._board[i-1][j-1])
        if i-1 >= 0 and j+1 < len(self._board[0]):
            adj_lst.append(self._board[i-1][j+1])
        if i+1 < len(self._board) and j-1 >= 0:
            adj_lst.append(self._board[i+1][j-1])
        if i+1 < len(self._board) and j+1 < len(self._board[0]):
            adj_lst.append(self._board[i+1][j+1])
        adj_lst.append(self._board[i][j])
        return adj_lst



    def draw(self):
        self.grid(row=0, column=0, sticky="nsew")
        width = 700 // self.m
        offset = (700 - width)
        for i in range(self.m):
            for j in range(self.n):
                self._board[i][j].showColor(width)

    def countCellBlue(self): # dem so o co the to mau xanh
        count = 0
        for i in self._board:
            for j in i:
               if(j._value >= -1):
                    count += 1
            
        return count

    def countCellRed(self):
        return self.m*self.n - self.countCellBlue()

    def toLogicMatrix(self): # convert logic to matrix 0 and 1
        matrix = []
        for i in self._board:
            t = []
            for j in i:
                t.append(int(j._logic))
            matrix.append(t)

        return matrix