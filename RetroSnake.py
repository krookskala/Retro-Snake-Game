import logging
import random

import pymongo
from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO, emit
from gevent import sleep
from gevent.pywsgi import WSGIServer
from geventwebsocket.handler import WebSocketHandler
from pymongo import MongoClient

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['EXPLAIN_TEMPLATE_LOADING'] = True
socketio = SocketIO(app)
logging.basicConfig(level=logging.DEBUG)
client = MongoClient("mongodb://localhost:27017/")
db = client.snake_game
leaderboard_collection = db.leaderboard


class Snake:
    def __init__(self, grid_width=20, grid_height=20):
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.reset_game()

    def reset_game(self):
        self.body = [(self.grid_width // 2, self.grid_height // 2)]
        self.direction = 'STOP'
        self.score = 0
        self.game_over = False
        self.speed = 1
        self.game_started = False
        self.game_paused = False

    def move(self, bait):
        if self.game_paused or not self.game_started:
            return

        head_x, head_y = self.body[0]
        move_delta = {
            'UP': (0, -1),
            'DOWN': (0, 1),
            'LEFT': (-1, 0),
            'RIGHT': (1, 0)
        }
        dx, dy = move_delta[self.direction]
        new_head = ((head_x + dx) % self.grid_width, (head_y + dy) % self.grid_height)

        # Wrap around logic
        if new_head[0] < 0:
            new_head = (self.grid_width - 1, new_head[1])
        if new_head[0] >= self.grid_width:
            new_head = (0, new_head[1])
        if new_head[1] < 0:
            new_head = (new_head[0], self.grid_height - 1)
        if new_head[1] >= self.grid_height:
            new_head = (new_head[0], 0)

        if new_head in self.body[1:]:
            self.game_over = True
            emit('game_over', {'score': self.score}, broadcast=True)
            return

        self.body.insert(0, new_head)

        if new_head == bait.position:
            self.score += 1
            self.speed += 0.1
            bait.refresh_position(self.body)
            emit('bait_eaten', broadcast=True)
        else:
            self.body.pop()  # Remove the tail piece of the snake unless new bait is eaten

    def set_direction(self, new_direction):
        opposite_directions = {
            'UP': 'DOWN',
            'DOWN': 'UP',
            'LEFT': 'RIGHT',
            'RIGHT': 'LEFT'
        }
        if new_direction != opposite_directions.get(self.direction) and not self.game_paused:
            self.direction = new_direction

    def to_dict(self):
        return {
            'body': self.body,
            'direction': self.direction,
            'score': self.score,
            'game_over': self.game_over,
            'game_paused': self.game_paused,
            'game_started': self.game_started,
            'speed': self.speed,
            'grid_width': self.grid_width,
            'grid_height': self.grid_height
        }

class Bait:
    def __init__(self, snake_body, grid_width=20, grid_height=20):
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.position = self.randomize_position(snake_body)

    def randomize_position(self, snake_body):
        possible_positions = [(x, y) for x in range(self.grid_width) for y in range(self.grid_height) if
                              (x, y) not in snake_body]
        if not possible_positions:
            raise Exception("No available positions to place the bait")
        self.position = random.choice(possible_positions)
        return self.position

    def refresh_position(self, snake_body):
        self.randomize_position(snake_body)

    def to_dict(self):
        return {
            'position': self.position,
            'grid_width': self.grid_width,
            'grid_height': self.grid_height
        }


@app.route('/')
def index():
    return render_template('menu.html')


def show_leaderboard():
    try:
        leaderboard = get_leaderboard_data()
        return jsonify(leaderboard)
    except pymongo.errors.ServerSelectionTimeoutError as err:
        return jsonify({"error": f"Cannot connect to database: {err}"}), 500
    except Exception as e:
        return jsonify({"error": f"An internal error occurred: {e}"}), 500


@app.route('/game', methods=['GET'])
def game_page():
    grid_width = request.args.get('gridWidth', default=20, type=int)
    grid_height = request.args.get('gridHeight', default=20, type=int)
    return render_template('index.html', grid_width=grid_width, grid_height=grid_height)


@socketio.on('pause_game')
def handle_pause_game():
    snake.game_paused = True


@socketio.on('resume_game')
def handle_resume_game():
    snake.game_paused = False


@socketio.on('start_game')
def handle_start_game(data):
    global snake, bait
    grid_width = data.get('gridWidth', 20)
    grid_height = data.get('gridHeight', 20)
    snake = Snake(grid_width=grid_width, grid_height=grid_height)
    bait = Bait(snake.body, grid_width=grid_width, grid_height=grid_height)
    snake.game_started = True
    emit('game_started')


@socketio.on('move')
def handle_move(data):
    global snake, bait
    snake_data = data['snake']
    bait_data = data['bait']
    snake = Snake.from_dict(snake_data)
    bait = Bait.from_dict(bait_data)
    snake.move(bait)
    if snake.game_over:
        save_score(data.get('name', 'Anonymous'), snake.score)
        leaderboard = get_leaderboard_data()
        emit('game_over', {'score': snake.score, 'leaderboard': leaderboard})
        snake.reset_game(bait)
    else:
        emit('game_state', {'snake': snake.body, 'bait': bait.position, 'score': snake.score, 'speed': snake.speed})

def save_score(name, score):
    try:
        leaderboard_collection.insert_one({"name": name, "score": score})
        print("Score saved successfully")
    except Exception as e:
        print(f"Failed to save score: {e}")

def get_leaderboard_data():
    try:
        leaderboard_entries = leaderboard_collection.find().sort("score", pymongo.DESCENDING).limit(10)
        return list(leaderboard_entries)
    except Exception as e:
        print(f"Failed to retrieve leaderboard data: {e}")
        return []

@app.route('/api/leaderboard', methods=['GET'])
def api_leaderboard():
    leaderboard = get_leaderboard_data()
    return jsonify(leaderboard)


@socketio.on('update_game')
def handle_update(data):
    global snake, bait
    if snake.game_over:
        return
    snake.move(bait)
    emit('game_state', {'snake': snake.body, 'bait': bait.position, 'score': snake.score, 'speed': snake.speed})
    if snake.game_over:
        save_score(data.get('name'), snake.score)
        leaderboard = get_leaderboard_data()
        sleep(0.1)
        emit('game_over', {'score': snake.score, 'leaderboard': leaderboard})
        snake.reset_game(bait)


@socketio.on('change_direction')
def handle_change_direction(data):
    if 'direction' in data:
        snake.set_direction(data['direction'])
        emit('direction_changed', {'new_direction': snake.direction})


def save_score(name, score):
    leaderboard_collection.insert_one({"name": name, "score": score})


@app.route('/api/leaderboard', methods=['GET'])
def get_leaderboard_data():
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 5, type=int)
    skip = (page - 1) * limit
    leaderboard_entries = leaderboard_collection.find().sort("score", pymongo.DESCENDING).skip(skip).limit(limit)
    return [{'name': entry['name'], 'score': entry['score']} for entry in leaderboard_entries]


@app.route('/leaderboard', methods=['GET'])
def leaderboard_page():
    return render_template('leaderboard.html')


if __name__ == "__main__":
    socketio.run(app, debug=True)
    http_server = WSGIServer(('0.0.0.0', 5000), app, handler_class=WebSocketHandler)
    http_server.serve_forever()