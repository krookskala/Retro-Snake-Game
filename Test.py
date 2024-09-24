import unittest
from unittest.mock import patch, MagicMock
from flask import json, template_rendered
from contextlib import contextmanager
from RetroSnake import app, socketio, Snake, Bait


# @contextmanager
# def captured_templates(app):
#     recorded = []
#
#     def record(sender, template, context, **extra):
#         recorded.append((template, context))
#
#     template_rendered.connect(record, app)
#     try:
#         yield recorded
#     finally:
#         template_rendered.disconnect(record, app)


class Test(unittest.TestCase):
    def setUp(self):
        super(Test, self).setUp()
        app.config['TESTING'] = True
        self.client = socketio.test_client(app)
        self.client.connect()
        self.snake = Snake()
        self.bait = Bait(self.snake.body)
        assert self.snake.to_dict() is not None

    def test_snake_initial_position(self):
        self.assertEqual(self.snake.body, [(10, 10)])

    def test_snake_moves_correctly(self):
        self.snake.set_direction('RIGHT')
        self.snake.move(self.bait)
        self.assertEqual(self.snake.body[0], (10, 10))

    # def test_snake_eats_bait(self):
    #     self.snake.body = [(9, 10)]
    #     self.bait.position = (10, 10)
    #     self.snake.set_direction('RIGHT')
    #     initial_score = self.snake.score
    #     self.client.emit('move', {'snake': self.snake.to_dict(), 'bait': self.bait.to_dict()})
    #     received = self.client.get_received()
    #     self.assertTrue(any(msg['name'] == 'bait_eaten' for msg in received))
    #     self.assertTrue(self.snake.score > initial_score)
    #     self.assertEqual(self.snake.body[0], self.bait.position)
    #
    # def test_snake_collision_with_wall(self):
    #     self.snake.body = [(0, 0)]
    #     self.snake.set_direction('LEFT')
    #     self.client.emit('move', {'snake': self.snake.to_dict(), 'bait': self.bait.to_dict()})
    #     received = self.client.get_received()
    #     self.assertTrue(any(msg['name'] == 'collision' and msg['args'][0]['type'] == 'boundary' for msg in received))
    #
    # def test_snake_collision_with_self(self):
    #     print(self.snake.to_dict())
    #     self.snake.body = [(10, 10), (10, 11), (10, 12)]
    #     self.snake.set_direction('DOWN')
    #     self.client.emit('move', {'snake': self.snake.to_dict(), 'bait': self.bait.to_dict()})
    #     received = self.client.get_received()
    #     self.assertTrue(any(msg['name'] == 'collision' for msg in received))

    @patch('RetroSnake.emit')
    def test_emit_game_over_on_collision(self, mock_emit):
        self.snake.body = [(0, 0)]
        self.snake.set_direction('LEFT')
        self.snake.move(self.bait)
        mock_emit.assert_called_with('collision', {'type': 'boundary'})


class TestBait(unittest.TestCase):
    def setUp(self):
        self.snake = Snake()
        self.bait = Bait(self.snake.body)

    def test_bait_initial_placement(self):
        self.assertNotIn(self.bait.position, self.snake.body)

    def test_bait_reposition(self):
        initial_position = self.bait.position
        self.bait.refresh_position(self.snake.body)
        self.assertNotEqual(self.bait.position, initial_position)
        self.assertNotIn(self.bait.position, self.snake.body)


# class FlaskAppTestCase(unittest.TestCase):
#     def setUp(self):
#         self.app = app.test_client()
#
#     def test_home_page(self):
#         with captured_templates(app) as templates:
#             response = self.app.get('/')
#             self.assertEqual(response.status_code, 200)
#             self.assertEqual(templates[0][0].name, 'menu.html')
#
#     def test_game_page(self):
#         with captured_templates(app) as templates:
#             response = self.app.get('/game')
#             self.assertEqual(response.status_code, 200)
#             self.assertEqual(templates[0][0].name, 'index.html')
#             self.assertIn('grid_width', templates[0][1])
#             self.assertIn('grid_height', templates[0][1])
#
#     def test_leaderboard_page(self):
#         with captured_templates(app) as templates:
#             response = self.app.get('/leaderboard')
#             self.assertEqual(response.status_code, 200)
#             self.assertEqual(templates[0][0].name, 'leaderboard.html')


class TestSocketIO(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = socketio.test_client(app)

    def test_game_start_event(self):
        self.client.emit('start_game', {'gridWidth': 20, 'gridHeight': 20})
        received = self.client.get_received()
        self.assertTrue(any(msg['name'] == 'game_started' for msg in received))

    def test_change_direction(self):
        self.client.emit('start_game', {'gridWidth': 20, 'gridHeight': 20})
        self.client.emit('change_direction', {'direction': 'UP'})
        received = self.client.get_received()
        print(received)
        self.assertTrue(any(msg['name'] == 'direction_changed' for msg in received))
        self.assertTrue(
            any(msg['args'][0]['new_direction'] == 'UP' for msg in received if 'args' in msg and len(msg['args']) > 0))

    def test_game_pause_and_resume(self):
        self.client.emit('pause_game')
        self.client.emit('resume_game')


if __name__ == '__main__':
    unittest.main()
