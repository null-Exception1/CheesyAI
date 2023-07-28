from collections import namedtuple as nmd
import re, time
from itertools import count
from collections import namedtuple as nmd
import chess
import random
pval = { 'P': 10*10, 'N': 28*10, 'B': 32*10, 'R': 48*10, 'Q': 93*10, 'K': 6000*10 }

# values for optimal placement of pieces
f = open('placement.txt','r')
pst = eval(f.read())
f.close()
for k, t in pst.items():
    pd = lambda row: (0,) + tuple(x+pval[k] for x in row) + (0,)
    pst[k] = sum((pd(t[i*8:i*8+8]) for i in range(8)), ())
    pst[k] = (0,)*20 + pst[k] + (0,)*20

treeparam1, treeparam2, treeparam3, treeparam4 = 91, 98, 21, 28


directions = {'P': (-10, -20, -11, -9), 'N': (-19, -8, 12, 21, 19, 8, -12, -21), 'B': (-9, 11, 9, -11), 'R': (-10, 1, 10, -1), 'Q': (-10, 1, 10, -1, -9, 11, 9, -11), 'K': (-10, 1, 10, -1, -9, 11, 9, -11)}


lowerbound = pval['K'] - 10*pval['Q']
upperbound = pval['K'] + 10*pval['Q']

maxttsize = 1e7


Entry = nmd('Entry', 'lower upper')

class Board(nmd('Board', 'bd score castlingrights bc ep kp')):
    
    def generator(self):
        for i, p in enumerate(self.bd):
            if not p.isupper():
                continue
            for d in directions[p]:
                for j in count(i+d, d):
                    q = self.bd[j]
                    if q.isspace() or q.isupper(): break
                    if p == 'P' and d in (-10, -10+-10) and q != '.':
                        break
                    if p == 'P' and d == -10+-10 and (i < treeparam1+-10 or self.bd[i+-10] != '.'):
                        break
                    if p == 'P' and d in (-10+-1, -10+1) and q == '.' \
                            and j not in (self.ep, self.kp, self.kp-1, self.kp+1):
                        break
                    yield (i, j)
                    if p in 'PNK' or q.islower(): break
                    if i == treeparam1 and self.bd[j+1] == 'K' and self.castlingrights[0]:
                        yield (j+1, j+-1)
                    if i == treeparam2 and self.bd[j+-1] == 'K' and self.castlingrights[1]:
                        yield (j+-1, j+1)
    
    def move(self, move):
        i, j = move
        p, q = self.bd[i], self.bd[j]
        put = lambda bd, i, p: bd[:i] + p + bd[i+1:]
        bd = self.bd
        (castlingrights, bc, ep, kp) = self.castlingrights, self.bc, 0, 0
        score = self.score + self.value(move)
        bd = put(bd, j, bd[i])
        bd = put(bd, i, '.')
        if i == treeparam1:
            castlingrights = (False, castlingrights[1])
        if i == treeparam2:
            castlingrights = (castlingrights[0], False)
        if j == treeparam3:
            bc = (bc[0], False)
        if j == treeparam4:
            bc = (False, bc[1])
        if p == 'K':
            castlingrights = (False, False)
            if abs(j-i) == 2:
                kp = (i+j)//2
                bd = put(bd, treeparam1 if j < i else treeparam2, '.')
                bd = put(bd, kp, 'R')
        if p == 'P':
            if treeparam3 <= j <= treeparam4:
                bd = put(bd, j, 'Q')
            if j - i == 2*-10:
                ep = i + -10
            if j == self.ep:
                bd = put(bd, j+10, '.')
        return Board(
            Board(bd, score, castlingrights, bc, ep, kp).bd[::-1].swapcase(), -Board(bd, score, castlingrights, bc, ep, kp).score, Board(bd, score, castlingrights, bc, ep, kp).bc, Board(bd, score, castlingrights, bc, ep, kp).castlingrights,
            119-Board(bd, score, castlingrights, bc, ep, kp).ep if Board(bd, score, castlingrights, bc, ep, kp).ep else 0,
            119-Board(bd, score, castlingrights, bc, ep, kp).kp if Board(bd, score, castlingrights, bc, ep, kp).kp else 0)

    def value(self, move):
        i, j = move
        p, q = self.bd[i], self.bd[j]
        score = pst[p][j] - pst[p][i]
        if q.islower():
            score += pst[q.upper()][119-j]
        if abs(j-self.kp) < 2:
            score += pst['K'][119-j]
        if p == 'K' and abs(i-j) == 2:
            score += pst['R'][(i+j)//2]
            score -= pst['R'][treeparam1 if j < i else treeparam2]
        if p == 'P':
            if treeparam3 <= j <= treeparam4:
                score += pst['Q'][j] - pst['P'][j]
            if j == self.ep:
                score += pst['P'][119-(j+10)]
        return score
