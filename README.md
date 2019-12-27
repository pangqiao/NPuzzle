# NPuzzle
In the 16-puzzle version of the game, a 4x4 board consists of 15 tiles numbered 1 through 15 and an empty tile
(marked as 0). One may move any tile into an orthogonally adjacent empty square, but maynot move outside the board 
or diagonally.The problem is to find a sequence of moves that transforms an initial board configuration into a 
specified goal configuration. The following are examples of an initial and goal configurations.

Initial configuration

![initial](https://github.com/pangqiao/NPuzzle/blob/master/init.jpg)

Goal configuration 

![goal](https://github.com/pangqiao/NPuzzle/blob/master/full.jpg)

# Algorithm:
The mouse click is mapped to UP, DOWN, LEFT and RIGHT accordingly.
Such as: 
0 is in the tile of(2,3)，if  I click 11,   11 moves to the right. 

![goal](https://github.com/pangqiao/NPuzzle/blob/master/right.jpg)

The method to move RIGHT like this:
```python
def move( direction):
  ... ...
  if(direction == Direction.RIGHT): 
    if column_0 != 0:
      blocks[row_0][column_0] = blocks[row_0][column_0 - 1]
      blocks[row_0][column_0 - 1] = 0
      column_0 -= 1 
```
# Make sure the final configuration can be reached.
In initial  state, make all the data according to the final configuration first. And then 
move the tiles in random direction with different rounds. The round decides the different
Level :easy, medium or high. 

# Tool chain
1. [Python3](https://www.python.org/)
2. [tkinter](https://docs.python.org/3/library/tkinter.html)
