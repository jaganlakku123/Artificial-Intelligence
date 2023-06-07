## **Part 1: Raichu**
---

### Evaluation Function

We calculate the evaluation function by the mobility of each piece.
Therefore,
1. Pichu = 2 as it can only move right diagonal and left diagonal
2. Pikachu =3 as it can only move Forward, Right and Left
3. Raichu = 8 as it can move Forward, Backward, Right, Left, Diagonal Left forward, Diagonal Right forward,  Diagonal Left backward, Diagonal Right backward

**Final Cost = Max Player pieces - Opponent pieces**

---
### Algorithm

We have used Alpha Beta Minimax method as the algorithm for this Game.
This algorithm is very useful when we have a large game tree as it prunes unnecassary child nodes. This makes the game perform faster, more efficient and saves memory.

1. Read the file inputs - size of board, player, board configuration, timelimit
2. Perform iterative deepening from depth 2 to 10 until the specified timelimit.
    * Perform alpha beta minimax algorithm till we hit 'max_depth' or reach 'terminal_state' to all moves as we iterate through the board
        * Return evaluation cost of all child node moves. ('White - Black')
        * Bubble the values according to the alpha beta algorithm.
        * Prune tree - for min if beta<=alpha or for max if alpha>= beta
        * Return the move with best move
        * Perform #2 while increasing max depth
3. Convert the given 2D board to the required output format
4. If there is no output, the program generates a random move just 1 second before it exceeds the time limit.
---

### Output

This file outputs the best move while performing iterative deepening.
We find the best move for each depth from 2 to 10.

---

### Problems Faced
Initially I tried creating the moves using 1D board but unfortunately there were a lot of issues. Also, I tried to implement Forward, Right, Left etc methods and passing the piece and steps to these methods for pichu, pikachu and raichu. But, this failed too. My code for Raichu moves kept going into an infinite loop as soon as it encountered an opponent Raichu. I tried debugging for a good amount of time which resulted in my game not working at all.

---

### Random generated function
I have implemented a random move function that generates a random move just before the timer ends in case no output is given. This would result in my code not terminating and the game will keep going.

---

### Ideas 
I noticed that the tree contains mulitple recursive board configurations. It stumbled upon me if there was a way to store these board configurations somehow in a hash table. Upon 'googling' I came across **Zobrist Hash table** where we store generate a unique hash value for each piece on all tiles of the board and perform an 'XOR' function. I would really like to implement it if I had the time but this was a really interesting idea and I'm quite sure it would save a lot of time and I could use this to leverage a greater 'max_depth' and get a more accurate best move.