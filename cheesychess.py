import re, time
from itertools import count
from collections import namedtuple as nmd
import chess
import random
from board import *
class ChessAI:
    def __init__(self, color: str):
        self.color = color # either "w" or "b"

        # took a much diff approach to rendering board
        # chess module was too slow
        b = ' rnbqkbnr\n'
        w = ' RNBQKBNR\n'
        
        self.hist = [Board((
        ' '+' '*8+'\n'
        ' '+' '*8+'\n'
        ' rnbqkbnr\n'
        ' '+'p'*8+'\n' 
        ' '+'.'*8+'\n'
        ' '+'.'*8+'\n'
        ' '+'.'*8+'\n'
        ' '+'.'*8+'\n'
        ' '+'P'*8+'\n'
        ' RNBQKBNR\n'
        ' '+' '*8+'\n'
        ' '+' '*8+'\n'
    ), 0, (True,True), (True,True), 0, 0)]
        self.tp_score = {}
        self.tp_move = {}
        self.history = set()
        self.nodes = 0
    def make_move(self) -> str:
        a = 'abcdefgh'
        mymove = self.playnext(self.hist)
        if self.color == 'w':
            mymove = [a[7-a.index(mymove[0][0])] + str(abs(9-int(mymove[0][1]))) + a[7-a.index(mymove[0][2])] + str(abs(9-int(mymove[0][3]))),mymove[1],mymove[2]]

        self.hist.append(self.hist[-1].move(mymove[2]))

        return mymove[0]
    def add_move(self, move: str) -> None:
        a = 'abcdefgh'
        if self.color == 'w':
            move = a[7-a.index(move[0])] + str(abs(9-int(move[1]))) + a[7-a.index(move[2])] + str(abs(9-int(move[3])))
        match = re.match('([a-h][1-8])'*2, move)
        fil, rank = ord(match.group(1)[0]) - ord('a'), int(match.group(1)[1]) - 1
        m1 = treeparam1 + fil - 10*rank
        fil, rank = ord(match.group(2)[0]) - ord('a'), int(match.group(2)[1]) - 1
        m2 = treeparam1 + fil - 10*rank
        m = m1,m2
        
        self.hist.append(self.hist[-1].move(m))
        
    def playnext(self, bd):
        
        start = time.time()
        for _depth, move, score in self.search(bd[-1], bd):
            if time.time() - start > 1:
                break
        
        rank, fil = divmod((119-move[0]) - treeparam1, 10)
        rank2, fil2 = divmod((119-move[1]) - treeparam1, 10)
        m1 = chr(fil + ord('a')) + str(-rank + 1)
        m2 = chr(fil2 + ord('a')) + str(-rank2 + 1)
        
        return m1+m2,score,move
    def search(self, position, history=()):
        self.nodes = 0
        if True:
            self.history = set(history)
            
            self.tp_score.clear()
            
        # iterative deepening
        for depth in range(7, 1000):

            
            lower, upper = -upperbound, upperbound
            while lower < upper - 13:
                gamma = (lower+upper+1)//2
                score = self.bound(position, gamma, depth)
                if score >= gamma:
                    lower = score
                if score < gamma:
                    upper = score
            self.bound(position, lower, depth)
            
            yield depth, self.tp_move.get(position), self.tp_score.get((position, depth, True)).lower
            
    def bound(self, position, gamma, depth, root=True):

        # main stuff happens here
        
        self.nodes += 1

        depth = max(depth, 0)

        if position.score <= -lowerbound:
            return -upperbound

        if True:
            if not root and position in self.history:
                return 0

        entry = self.tp_score.get((position, depth, root), Entry(-upperbound, upperbound))
        if entry.lower >= gamma and (not root or self.tp_move.get(position) is not None):
            return entry.lower
        if entry.upper < gamma:
            return entry.upper

        # had to actually define the move system because i was making it myself
        def moves():
            
            if depth > 0 and not root and any(c in position.bd for c in 'RBNQ'):
                yield None, -self.bound(Board(position.bd[::-1].swapcase(), -position.score,position.bc, position.castlingrights, 0, 0), 1-gamma, depth-3, root=False)
            if depth == 0:
                yield None, position.score
            killer = self.tp_move.get(position)
            if killer and (depth > 0 or position.value(killer) >= 219):
                yield killer, -self.bound(position.move(killer), 1-gamma, depth-1, root=False)
            for move in sorted(position.generator(), key=position.value, reverse=True):
                if depth > 0 or position.value(move) >= 219:
                    yield move, -self.bound(position.move(move), 1-gamma, depth-1, root=False)

        # avg bound 
        best = -upperbound
        for move, score in moves():
            best = max(best, score)
            if best >= gamma:
                if len(self.tp_move) > maxttsize: self.tp_move.clear()
                self.tp_move[position] = move
                break
        if best < gamma and best < 0 and depth > 0:
            is_dead = lambda position: any(position.value(m) >= lowerbound for m in position.generator())
            if all(is_dead(position.move(m)) for m in position.generator()):
                in_check = is_dead(Board(
            position.bd[::-1].swapcase(), -position.score,
            position.bc, position.castlingrights, 0, 0))
                best = -upperbound if in_check else 0

        if len(self.tp_score) > maxttsize: self.tp_score.clear()
        if best >= gamma:
            self.tp_score[position, depth, root] = Entry(best, entry.upper)
        if best < gamma:
            self.tp_score[position, depth, root] = Entry(entry.lower, best)

        return best
"""
# sample game between itself

bd = chess.Board()
ai1 = ChessAI('w')

ai2 = ChessAI('b')
while True:
    print('-'*10)
    print(bd)
    #move=str(random.choice(list(bd.legal_moves)))
    

    # ai1 makes it's own move
    move = ai1.make_move()

    
    # inputs move into ai2
    ai2.add_move(move)

    # pushing the piece on the board
    bd.push(chess.Move.from_uci(move))
    
    print('-'*10)
    print(bd)

    # makes it's own move
    move = ai2.make_move()

    # input move
    ai1.add_move(move)

    
    # pushing the piece on the board
    bd.push(chess.Move.from_uci(move))
    



"""
import subprocess
engine = subprocess.Popen(
    'cmd.exe',
    universal_newlines=True,
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    bufsize=1
)


def put(command):
    print(command+'\n')
l = ""
def get():
    # using the 'isready' command (engine has to answer 'readyok')
    # to indicate current last line of stdout
    engine.stdin.write('isready\n')
    while True:
        text = engine.stdout.readline().strip()
        if text == 'readyok':
            break
        if text != '':
            pass
            #print(text)
        if text.split(' ')[0] == 'bestmove':
            ai.add_move(text.split(' ')[1])
            m = ai.make_move()
            put("position moves "+text.split(' ')[1]+'\n'+"position moves "+m+'\ngo')
        if text == 'isready':
            put("isreadyok")
        if text == 'isreadyok':
            ai = ChessAI('b')
            put('position startpos\ngo')
        if text == 'position startpos':
            ai = ChessAI('w')
        if text == 'go':
            put("bestmove "+ai.make_move())
        if text.split(' ')[0] == "position" and text.split(' ')[1] == "moves" and "position" in l:
            ai.add_move(text.split(' ')[2])
        if text == 'uci':
            put("id name CheezyChess\nid author itzcool\nuciok")
        l = text

# in case when white (they start first)
while True:
    get()
    
# in case when black
put('ucinewgame\nisready')
get()


# im bad at uci protocol no judge pls
# u can dm me at cheeesey101 to fix anything because i really dont know how to implement uci    
#"""

