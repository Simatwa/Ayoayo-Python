<h1 align="center"> Ayoayo-Python</h1>

<p align="center">
<a href="https://github.com/Simatwa/Ayoayo-Python/blob/main/LICENSE"><img alt="License" src="https://img.shields.io/static/v1?logo=text&color=Blue&message=Unlicense&label=License"/></a>
<a href="https://python.org"><img alt="Python Version" src="https://img.shields.io/static/v1?logo=text&color=Blue&message=>=3.6&label=Python"/></a>
<a href="https://github.com/psf/black"><img alt="Black" src="https://img.shields.io/badge/code%20style-black-000000.svg"/></a>
</p>

## Overview

This project implements a text-based version of the Ayoayo game in Python. The implementation follows the rules specified in the requirements document.

## Approach

1. **Object-Oriented Design**:
   - `Player` class to manage player-specific data (name and store count)
   - `Ayoayo` class to manage game state and logic

2. **Game Logic**:
   - Implemented all core rules including:
     - Basic sowing mechanics
     - Special rules (extra turns and captures)
     - Game end conditions

## Key Assumptions

1. **Player Indices**: Used 0 and 1 for player indices internally while maintaining 1-6 pit indices for user input
2. **Input Handling**: Assumed all player inputs would be integers
3. **Game Flow**: Didn't enforce strict turn alternation to allow for flexible testing
4. **Board Representation**: Used a list of lists for the board (instead of dictionary) for cleaner implementation

## How to Run

### Prerequisites

- [Python 3.6](https://python.org) or higher

### Running the Game

1. **Interactive Mode**:

   ```bash
   python main.py
   ```

    > [!NOTE]
    > The current implementation focuses on the game logic. For interactive play, you would need to add input handling.

### Example Usage

```python
from ayoayo import Ayoayo

# Initialize game
game = Ayoayo()
player1 = game.createPlayer("Alice")
player2 = game.createPlayer("Bob")

# Make moves
print(game.playGame(0, 3))  # Player 1 (index 0) moves from pit 3
game.printBoard()

# Check game status
print(game.returnWinner())
```

## File Structure

- `main.py`: Main game implementation
- `reflection.txt`: Contains notes and reflections on the design and implementation process.
- `README.md`: This documentation file

## Additional Files

- `LICENSE`: Specifies the licensing terms for the project.

## Future Enhancements

1. Add interactive command-line interface
2. Implement AI opponent
3. Add game history tracking
4. Create graphical interface option
