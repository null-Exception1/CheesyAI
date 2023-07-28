## Inspiration
We both have since childhood had a knack for chess and played it at a competitive level.Our increasing familiarity with technology led us to contemplate how two AI-driven chess players could engage in a contest. This inspiration motivated me to initiate and work on this project.

## What it does
The code I have submitted basically programs the Chess AI and trains it on some opening moves and at various depths and based upon the situation in the game it thinks of the most appropriate move. The core algorithm used in this AI is the Minimax algorithm.
Algorithms used Mini-max algorithm is a backtracking algorithm which is used in chess often. It provides the best move for the player assuming that opponent is also playing the best moves.

The Minimax algorithm is a decision-making approach commonly used in two-player games, like chess. It aims to maximize the AI's gains while minimizing the opponent's potential gains. The algorithm works by exploring the possible moves in the game up to a certain depth, creating a game tree. It then evaluates the positions on the tree using a scoring function to assess the desirability of each move. The AI chooses the move that leads to the highest score assuming the opponent will play optimally, and the AI itself will play optimally in response.

This AI uses the following methods to increase Minimax tree depth:

Transposition Tables - A transposition table is a cache of previously seen positions. The Chess AI uses this to improve it's speed by overlooking any previously seen positions, so it's processing power isn't wasted on it.

Alpha Beta Pruning - Alpha-beta pruning is a modified version of the minimax algorithm. It is an optimization technique for the minimax algorithm. The Alpha-beta pruning to a standard minimax algorithm returns the same move as the standard algorithm does, but it removes all the nodes which are not really affecting the final decision but making algorithm slow. Hence by pruning these nodes, it makes the algorithm fast.

MTD-bi - The binary search version of MTD(f), also known as NegaC*, is basically an improvement of alpha beta pruning on minimax.

Iterative Deepening - It applies the alpha beta pruning algorithm from depth 1 to max depth. This may seem excessive and wasteful, but it is the best time management technique as a larger depth may take more time than a needed, so it plays the best move of the depth that was allowed to be searched in the time given.

Move ordering - For the alpha-beta algorithm to perform well, the best moves need to be searched first. A PV-Move is used to find the best move in the previous iteration of Iterative deepening.

Quiescence search - It mitigates the effect of the horizon problem faced by alpha beta pruning by delaying evaluation until the position is stable enough to be evaluated statically.

Zobrist hash - To increase the depth even more, we encode the chessboard into a Zobrist hash which is fairly easier to store and process.
By combining these elements, the Chess AI is a formidable opponent, capable of making informed decisions and challenging even experienced human players.
## How we built it
General theory optimizations-

Openings - It uses a piece mapping formula to see optimal position of a piece on the chessboard usually. Example : A knight in the corner of the board is not as valuable as one in the center, defending more squares. Piece mapping formula for a knight would look like this -
[
-50, -40, -30, -30, -30, -30, -40, -50,
-40, -20,    0,  5,   5,   0,-20,  -40,
-30,   5,   10, 15,  15,  10,  5,  -30,
-30,   0,   15, 20,  20,  15,  0,  -30,
-30,   5,   15, 20,  20,  15,  5,  -30,
-30,   0,   10, 15,  15,  10,   0, -30,
-40, -20,    0,  0,   0,   0, -20, -40,
-50, -40, -30, -30, -30, -30, -40, -50]
Where each number in the list represents a square on the chessboard, it represents the value of the knight in that square. This map will be different for different pieces, like the bishop. Bishop covers more diagonal while in the corner, so it would actually benefit from being in the corner, than the knight.

This helps in making opening decisions where no particular depth can decide the game instantly. It imitates a fairly beginner and strong opening via following these maps, thus eliminating the need for keeping a database of openings.

Piece values - Assigns the worth of a piece, but this time with a different approach - Using a database of hundreds of chess games, we assigned worth of the pieces according to the win/loss ratio. It is given according to how much the piece impacts the game overall. This data-driven approach provides a more nuanced evaluation of each piece's importance during gameplay.

## Challenges we ran into
Creating a sophisticated and competitive Chess AI involves tackling several challenges. Some of the key challenges we encountered during the development process are:

1) Complexity and Search Space: Chess has a vast number of possible moves and positions, leading to an enormous search space and exploring this space is computationally expensive and time-consuming, making it challenging to reach deeper depths in the Minimax tree.
2) Time Constraints: In practical scenarios, the AI must make decisions within limited time frames. Achieving a balance between depth of search and decision speed is crucial for real-time gameplay.
3) The evaluation function needs to consider various factors such as piece values, piece placement, control of the center, pawn structure, and king safety.
4) Endgame Handling

Developing a strong Chess AI requires a combination of algorithmic innovation, domain knowledge, and optimizations and we have tried our best to put all those together to get such a good output.
