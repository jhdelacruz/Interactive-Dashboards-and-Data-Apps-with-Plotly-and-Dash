import dash
from dash import dcc, html, Input, Output, State
import plotly.graph_objects as go
import random
from collections import deque

# Initialize the Dash app
app = dash.Dash(__name__)

# Game constants
GRID_SIZE = 20
CELL_SIZE = 20
UPDATE_INTERVAL = 150  # milliseconds

# Initialize game state
def init_game_state():
    return {
        'snake': deque([[10, 10], [10, 11], [10, 12]]),  # Initial snake position
        'direction': 'right',
        'next_direction': 'right',
        'food': [random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1)],
        'score': 0,
        'game_over': False,
        'game_started': False
    }

game_state = init_game_state()

# App layout
app.layout = html.Div([
    html.Div([
        html.H1('Snake Game', style={'textAlign': 'center', 'color': '#2c3e50', 'marginBottom': '10px'}),
        html.Div([
            html.Div([
                html.H3('Score: ', style={'display': 'inline', 'marginRight': '10px'}),
                html.Span(id='score-display', children='0', style={'fontSize': '24px', 'fontWeight': 'bold', 'color': '#27ae60'})
            ], style={'textAlign': 'center', 'marginBottom': '10px'}),
            html.Div([
                html.Button('Start Game', id='start-button', n_clicks=0,
                           style={'padding': '10px 20px', 'fontSize': '16px', 'marginRight': '10px',
                                  'backgroundColor': '#27ae60', 'color': 'white', 'border': 'none',
                                  'borderRadius': '5px', 'cursor': 'pointer'}),
                html.Button('Reset Game', id='reset-button', n_clicks=0,
                           style={'padding': '10px 20px', 'fontSize': '16px',
                                  'backgroundColor': '#e74c3c', 'color': 'white', 'border': 'none',
                                  'borderRadius': '5px', 'cursor': 'pointer'})
            ], style={'textAlign': 'center', 'marginBottom': '20px'}),
        ]),
        dcc.Graph(id='game-board', style={'width': f'{GRID_SIZE * CELL_SIZE + 100}px', 'margin': '0 auto'}),
        html.Div(id='game-status', style={'textAlign': 'center', 'fontSize': '20px', 'marginTop': '20px', 'fontWeight': 'bold'}),
        html.Div([
            html.H4('Controls:', style={'marginBottom': '10px'}),
            html.P('Arrow Keys or WASD to move'),
            html.P('Start Game button to begin'),
            html.P('Eat the red food to grow and score points!'),
        ], style={'textAlign': 'center', 'marginTop': '20px', 'color': '#7f8c8d'}),
    ], style={'maxWidth': '800px', 'margin': '0 auto', 'padding': '20px'}),

    dcc.Interval(id='game-interval', interval=UPDATE_INTERVAL, n_intervals=0, disabled=True),
    dcc.Store(id='game-state-store', data=game_state),

    # JavaScript for keyboard input
    html.Div(id='keypress-event', style={'display': 'none'}),
    html.Script('''
        document.addEventListener('keydown', function(event) {
            const keyMap = {
                'ArrowUp': 'up', 'ArrowDown': 'down', 'ArrowLeft': 'left', 'ArrowRight': 'right',
                'w': 'up', 's': 'down', 'a': 'left', 'd': 'right',
                'W': 'up', 'S': 'down', 'A': 'left', 'D': 'right'
            };
            if (keyMap[event.key]) {
                event.preventDefault();
                window.dash_clientside = window.dash_clientside || {};
                window.dash_clientside.keypress = keyMap[event.key];
            }
        });
    '''),
], style={'fontFamily': 'Arial, sans-serif', 'backgroundColor': '#ecf0f1', 'minHeight': '100vh', 'padding': '20px'})

# Callback to start the game
@app.callback(
    Output('game-interval', 'disabled'),
    Output('game-state-store', 'data', allow_duplicate=True),
    Input('start-button', 'n_clicks'),
    State('game-state-store', 'data'),
    prevent_initial_call=True
)
def start_game(n_clicks, state):
    if n_clicks > 0:
        state['game_started'] = True
        state['game_over'] = False
        return False, state
    return True, state

# Callback to reset the game
@app.callback(
    Output('game-state-store', 'data', allow_duplicate=True),
    Output('game-interval', 'disabled', allow_duplicate=True),
    Input('reset-button', 'n_clicks'),
    prevent_initial_call=True
)
def reset_game(n_clicks):
    new_state = init_game_state()
    return new_state, True

# Main game loop callback
@app.callback(
    Output('game-board', 'figure'),
    Output('score-display', 'children'),
    Output('game-status', 'children'),
    Output('game-state-store', 'data', allow_duplicate=True),
    Input('game-interval', 'n_intervals'),
    State('game-state-store', 'data'),
    prevent_initial_call=True
)
def update_game(n_intervals, state):
    if not state['game_started'] or state['game_over']:
        return create_board(state), state['score'], get_status_message(state), state

    # Update direction
    state['direction'] = state['next_direction']

    # Calculate new head position
    snake = deque(state['snake'])
    head = list(snake[-1])

    if state['direction'] == 'up':
        head[1] -= 1
    elif state['direction'] == 'down':
        head[1] += 1
    elif state['direction'] == 'left':
        head[0] -= 1
    elif state['direction'] == 'right':
        head[0] += 1

    # Check wall collision
    if head[0] < 0 or head[0] >= GRID_SIZE or head[1] < 0 or head[1] >= GRID_SIZE:
        state['game_over'] = True
        return create_board(state), state['score'], get_status_message(state), state

    # Check self collision
    if head in list(snake):
        state['game_over'] = True
        return create_board(state), state['score'], get_status_message(state), state

    # Add new head
    snake.append(head)

    # Check food collision
    if head == state['food']:
        state['score'] += 10
        # Generate new food position
        while True:
            new_food = [random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1)]
            if new_food not in list(snake):
                state['food'] = new_food
                break
    else:
        # Remove tail if no food eaten
        snake.popleft()

    state['snake'] = list(snake)

    return create_board(state), state['score'], get_status_message(state), state

# Callback for keyboard input (simplified version)
# Note: For full keyboard support, you'd need clientside callbacks or dash-extensions
# This is a simplified version for demonstration

def create_board(state):
    """Create the game board visualization"""
    # Create grid
    shapes = []

    # Draw grid lines
    for i in range(GRID_SIZE + 1):
        shapes.append({
            'type': 'line',
            'x0': i, 'y0': 0, 'x1': i, 'y1': GRID_SIZE,
            'line': {'color': '#bdc3c7', 'width': 1}
        })
        shapes.append({
            'type': 'line',
            'x0': 0, 'y0': i, 'x1': GRID_SIZE, 'y1': i,
            'line': {'color': '#bdc3c7', 'width': 1}
        })

    # Draw snake
    snake_x = []
    snake_y = []
    for segment in state['snake']:
        snake_x.append(segment[0] + 0.5)
        snake_y.append(segment[1] + 0.5)

    # Draw food
    food_x = [state['food'][0] + 0.5]
    food_y = [state['food'][1] + 0.5]

    # Create figure
    fig = go.Figure()

    # Add snake
    fig.add_trace(go.Scatter(
        x=snake_x, y=snake_y,
        mode='markers',
        marker=dict(size=CELL_SIZE, color='#27ae60', symbol='square'),
        name='Snake',
        hoverinfo='skip'
    ))

    # Add snake head (different color)
    if len(snake_x) > 0:
        fig.add_trace(go.Scatter(
            x=[snake_x[-1]], y=[snake_y[-1]],
            mode='markers',
            marker=dict(size=CELL_SIZE, color='#229954', symbol='square'),
            name='Head',
            hoverinfo='skip'
        ))

    # Add food
    fig.add_trace(go.Scatter(
        x=food_x, y=food_y,
        mode='markers',
        marker=dict(size=CELL_SIZE, color='#e74c3c', symbol='square'),
        name='Food',
        hoverinfo='skip'
    ))

    # Update layout
    fig.update_layout(
        shapes=shapes,
        xaxis=dict(range=[-0.5, GRID_SIZE + 0.5], showticklabels=False, showgrid=False, zeroline=False),
        yaxis=dict(range=[-0.5, GRID_SIZE + 0.5], showticklabels=False, showgrid=False, zeroline=False),
        width=GRID_SIZE * CELL_SIZE + 100,
        height=GRID_SIZE * CELL_SIZE + 100,
        plot_bgcolor='#ecf0f1',
        paper_bgcolor='#ecf0f1',
        showlegend=False,
        margin=dict(l=20, r=20, t=20, b=20),
        yaxis_scaleanchor="x",
    )

    return fig

def get_status_message(state):
    """Get the current game status message"""
    if state['game_over']:
        return html.Span('Game Over! Press Reset to play again.', style={'color': '#e74c3c'})
    elif state['game_started']:
        return html.Span('Playing... Use arrow keys to move!', style={'color': '#27ae60'})
    else:
        return html.Span('Press Start Game to begin!', style={'color': '#3498db'})

# Add clientside callback for keyboard handling
app.clientside_callback(
    """
    function(n_intervals, state) {
        if (window.dash_clientside && window.dash_clientside.keypress) {
            const newDir = window.dash_clientside.keypress;
            const currentDir = state.direction;

            // Prevent reversing direction
            const opposites = {
                'up': 'down', 'down': 'up',
                'left': 'right', 'right': 'left'
            };

            if (opposites[newDir] !== currentDir) {
                state.next_direction = newDir;
            }

            window.dash_clientside.keypress = null;
        }
        return state;
    }
    """,
    Output('game-state-store', 'data', allow_duplicate=True),
    Input('game-interval', 'n_intervals'),
    State('game-state-store', 'data'),
    prevent_initial_call=True
)

if __name__ == '__main__':
    app.run_server(debug=True)
