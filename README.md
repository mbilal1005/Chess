# Chess

A fully playable two-player chess game built with Python and Pygame. All standard chess rules are implemented, including check detection, castling, and pawn promotion.

## Features

- **Player vs Player** — two players on the same machine, taking turns
- **Legal move validation** — only valid moves are accepted; illegal moves are ignored
- **Check detection** — moves that leave the king in check are filtered out
- **Castling** — both kingside and queenside castling supported
- **Pawn promotion** — pawns are automatically promoted to queen upon reaching the back rank
- **Drag-and-drop interface** — click and drag pieces to move them
- **Move highlighting** — valid destinations are highlighted when dragging a piece
- **Last move indicator** — the previous move is shown in blue after each turn

## Tech Stack

- **Python 3.10+**
- **Pygame** — rendering, event handling, and the game loop

## Getting Started

### Prerequisites

```bash
pip install pygame
```

### Running the game

```bash
cd Sjakk_v2
python main.py
```

> **Note:** The image paths in `Piece.py` are currently relative to a `Python/` directory. If you run from inside `Sjakk_v2/`, update the path in `Piece.py` `set_texture()` to:
> ```python
> self.texture = os.path.join(f'images/imgs-{size}px/{self.color}_{self.name}.png')
> ```

## Project Structure

```
Sjakk_v2/
├── main.py        # Entry point — game loop and event handling
├── game.py        # Rendering logic (board, pieces, highlights)
├── board.py       # Board state, move execution, and move generation
├── Piece.py       # Piece classes (Pawn, Knight, Bishop, Rook, Queen, King)
├── square.py      # Square class representing each cell on the board
├── move.py        # Move class representing a move from one square to another
├── dragger.py     # Drag-and-drop state and rendering
├── const.py       # Board dimensions and display constants
└── images/
    ├── imgs-80px/   # Piece sprites (used on board)
    └── imgs-128px/  # Piece sprites (used while dragging)
```

## How to Play

1. White always moves first.
2. Click and hold a piece to pick it up — valid moves are highlighted in red.
3. Release the piece on a highlighted square to make the move.
4. Turns alternate between white and black.
5. Pawns reaching the opposite back rank are automatically promoted to queens.
