# Snake Game - Interactive Dash Application

An interactive Snake game built with Plotly Dash, demonstrating the framework's capability for creating real-time interactive applications.

## Features

- **Interactive Gameplay**: Control the snake using arrow keys or WASD
- **Real-time Updates**: Smooth game updates using Dash callbacks and intervals
- **Visual Grid**: Clean, modern game board rendered with Plotly
- **Score Tracking**: Keep track of your score as you eat food
- **Game Controls**: Start, reset, and restart the game at any time

## How to Run

1. Make sure you have the required dependencies installed:
```bash
pip install dash plotly
```

2. Run the game:
```bash
python snake_game.py
```

3. Open your browser and navigate to `http://127.0.0.1:8050/`

## How to Play

1. Click the **"Start Game"** button to begin
2. Use the **Arrow Keys** or **WASD** keys to control the snake:
   - Up Arrow / W: Move up
   - Down Arrow / S: Move down
   - Left Arrow / A: Move left
   - Right Arrow / D: Move right
3. Eat the red food to grow your snake and increase your score (+10 points per food)
4. Avoid hitting the walls or your own body
5. Click **"Reset Game"** to start a new game

## Game Rules

- The snake starts with 3 segments
- Each food eaten makes the snake grow by 1 segment
- The game ends if the snake hits a wall or itself
- Score increases by 10 points for each food eaten

## Technical Details

This game demonstrates several Dash features:
- **Dash callbacks**: For handling user interactions and game logic
- **Clientside callbacks**: For responsive keyboard input handling
- **dcc.Interval**: For game loop updates
- **dcc.Store**: For maintaining game state
- **Plotly figures**: For rendering the game board

The game updates at 150ms intervals, providing smooth gameplay while being responsive to user input.

## Customization

You can modify the following constants in `snake_game.py`:

- `GRID_SIZE`: Size of the game grid (default: 20x20)
- `CELL_SIZE`: Size of each cell in pixels (default: 20)
- `UPDATE_INTERVAL`: Game update speed in milliseconds (default: 150 - decrease for faster gameplay)

Enjoy playing!
