from itertools import combinations, product
import copy
from variable import board
from pysat.solvers import Glucose3
import numpy as np


class Sentence:
    def __init__(self, varivale, nblue):
        self._n_blue = nblue # Số lượng ô màu xanh có xung quanh variable
        self._set_cells = [var._pos for var in varivale]


    def knownBlue(self): 
        set_blue = list(combinations(self._set_cells, self._n_blue + 1))
        cl = np.asarray(set_blue) * -1
        return cl


    def knownRed(self):
        set_red = list(combinations(self._set_cells, len(self._set_cells) - self._n_blue + 1))
        cl = np.asarray(set_red)
        return cl


    def convertClause(self): # Convert Clause 
        blue = self.knownBlue()
        red = self.knownRed()
        clause = []
        clause.extend(blue)
        clause.extend(red)
        return clause


    def __repr__(self):
        return f"{self._set_cells}"



class XAT:
    def __init__(self, _board):
        self._py_sat_kb = Glucose3()
        self._kb = []
        self._heuristic_kb = []
        self.__b = _board # copy board


    def addKB(self, cell): # có bao nhiêu ô màu xanh được tô màu xanh xung quanh các ô được đánh số
        adj_cells = self.__b.getAdjacentCell(cell._x, cell._y)
        sentence = Sentence(adj_cells, cell._value)
        clause = sentence.convertClause()
        self._kb.extend(clause)
        for i in clause:
            self._py_sat_kb.add_clause([int(k) for k in i])

    def buildKB(self):
        for i in range(len(self.__b._board)):
            for j in range(len(self.__b._board[0])):
                if(self.__b._board[i][j]._value >= 0):
                    self.addKB(self.__b._board[i][j])

    def usePySAT(self):  # Pysat Algorithm
        self._py_sat_kb.solve()
        model = self._py_sat_kb.get_model()
        #print(model)
        for i in range(len(self.__b._board)):
            for j in range(len(self.__b._board[0])):
                if(self.__b._board[i][j]._pos in model):
                    self.__b._board[i][j]._logic = True
                else:
                    self.__b._board[i][j]._logic = False
        return model



    def heuristic(self, clause):
        blue = 0
        red = 0
        h = 0
        for i in clause:
            if(i < 0):
                red += 1
            if(i > 0):
                blue += 1
        h = self.__b.countCellBlue() - blue + self.__b.countCellRed() - red + 1
        return h

    def getHeuristicKB(self):
        for i in self._kb:
            self._heuristic_kb.append([i,self.heuristic(i)])
            
    def addHeuristicKB(self, cnf):
        for i in cnf:
            self._heuristic_kb.append([i,self.heuristic(i)])

    def sorter(self, item):
        for i in self._heuristic_kb:
            if item is i[0]:
                return i[1]
        return 10000

    def selectHeuristicClause(self, kb):
        for c in kb:
            return c

    def adpll(self, clause, model = []):
        if len(clause) == 0:
            return True, model

        if any([len(c) == 0 for c in clause]):
            return False, None

        l = self.select_literal(clause)
        new_cnf = [c for c in clause if l not in c]
        self.addHeuristicKB(new_cnf)
        temp = []
        

        for c in new_cnf:
            if -l in c:
                c = c[c != -l]
            temp.append(c)

        clause.extend(temp)
        clause.sort(key= self.sorter)
        t = model.copy()
        t.append(l)
        sat, vals = self.Build_BT(temp, t)
        
        if sat:
            return sat, vals
        else:
            t.remove(l)

        new_cnf = [c for c in clause if -l not in c]
        self.addHeuristicKB(new_cnf)
        temp = []

        for c in new_cnf:
            if l in c:
                c = c[c != l]
            temp.append(c)

        clause.extend(temp)
        clause.sort(key= self.sorter)
        t = model.copy()
        t.append(-l)
        sat, vals = self.Build_BT(temp, t)

        if sat:
            return sat, vals
        else:
            t.remove(-l)
        return False, None

    def useAStar(self):
        self.getHeuristicKB()
        sol, model = self.adpll(self._kb)

        print(model)
        for i in range(len(self.__b._board)):
            for j in range(len(self.__b._board[0])):
                if(self.__b._board[i][j]._pos in model):
                    self.__b._board[i][j]._logic = True
                else:
                    self.__b._board[i][j]._logic = False

        return model

    def BF(self): 
        literals = set()
        for conj in self._kb:
            for disj in conj:
                literals.add(abs(disj))
        literals = list(literals)
        n = len(literals)
        for seq in product([1, -1], repeat=n):
            a = np.asarray(seq) * np.asarray(literals)
            if all([bool(set(disj).intersection(set(a))) for disj in self._kb]):
                return a
        return None

    def useBruceForce(self): # Bruce- Force Algorithm
        model = self.BF()
        for i in range(len(self.__b._board)):
            for j in range(len(self.__b._board[0])):
                if(self.__b._board[i][j]._pos in model):
                    self.__b._board[i][j]._logic = True
                else:
                    self.__b._board[i][j]._logic = False
        return model

    def select_literal(self, cnf):
        for c in cnf:
            for literal in c:
                return literal

    def Build_BT(self, cnf, assignments = []):
        if len(cnf) == 0:
            return True, assignments
        if any([len(c) == 0 for c in cnf]):
            return False, None
        l = self.select_literal(cnf)
        new_cnf = [c for c in cnf if l not in c]
        temp = []
        for c in new_cnf:
            if -l in c:
                c = c[c != -l]
            temp.append(c)
        t = assignments.copy()
        t.append(l)
        sat, vals = self.Build_BT(temp, t)
        if sat:
            return sat, vals
        else:
            t.remove(l)
        new_cnf = [c for c in cnf if -l not in c]
        temp = []
        for c in new_cnf:
            if l in c:
                c = c[c != l]
            temp.append(c)
        t = assignments.copy()
        t.append(-l)
        sat, vals = self.Build_BT(temp, t)
        if sat:
            return sat, vals
        else:
            t.remove(-l)
        return False, None

    def useBackTracking(self):
        sol, model = self.Build_BT(self._kb)
        for i in range(len(self.__b._board)):
            for j in range(len(self.__b._board[0])):
                if(self.__b._board[i][j]._pos in model):
                    self.__b._board[i][j]._logic = True
                else:
                    self.__b._board[i][j]._logic = False
        return model

    def __repr__(self):
        return f" KB = {self._set_kb}"
