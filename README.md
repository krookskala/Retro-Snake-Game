
# Retro Snake Game

![1 2](https://github.com/user-attachments/assets/a072e339-9e74-4d4c-868f-c548792d6122)

![1 1](https://github.com/user-attachments/assets/3aedc0d0-b9af-4c31-9647-a87e68959f95)

![1 3](https://github.com/user-attachments/assets/e93fca2b-39e6-4549-8c2f-5417dffa6024)










Welcome to the Retro Snake Game, an advanced Flask-based web application that revitalizes the timeless classic with modern web technologies. This game not only challenges players to achieve high scores but also enhances the experience with real-time features, audio effects, and a dynamic leaderboard.
## Table of Contents

- [About the Project](#about-the-project)
- [Features](#features)
- [Getting Started](#getting-started)
- [Detailed File Descriptions](#usage)
- [Demo](#demo)
- [Contributing](#contributing)
- [Links](#links)
- [License](#license)
## Project Overview

The L-system used in this simulation involves a set of symbols and production rules to model the iterative growth of a fractal plant. The system starts with an initial "word" and iteratively replaces parts of that word according to the production rules to simulate plant growth visually.



## Features
**Enhanced Gameplay:**

- **Dynamic Obstacles:** As the snake grows, the game introduces new obstacles, increasing the complexity and requiring more strategic navigation.

- **Multiple Levels:** Players can progress through various levels, each with unique challenges and faster gameplay.

- **Audio Feedback:** Incorporate sounds for different game events such as eating food, game over, and other interactions to enrich the user experience.

**Real-Time Leaderboard:**

- **Global Competition:** Players from around the world can see their ranks in real-time, adding a competitive edge.

- **Session-Based Scores:** Scores are tracked throughout the gaming session, with high scores saved to a MongoDB database.

**User Interaction:**

- **Customizable Settings:** Users can adjust settings like sound on/off, game speed, and difficulty levels from within the game menu.

**Technologies Used:**

- **Flask** and **Flask-SocketIO** for backend development and real-time web socket communication

- **HTML5/CSS3** and **JavaScript** for a responsive and interactive frontend.

- **MongoDB** for storing user data and leaderboard scores.

- **Gevent** for efficient network concurrency.

**Audio Assets:**

- The game features several custom sound effects to enhance player engagement.

- **background.ogg:** Looped background music that sets the gameplay atmosphere.

- **eating.mp3** and **eat.ogg:** Sound effects played when the snake eats food, providing immediate auditory feedback to the player.

- **death.ogg:** Played upon game over, indicating the snake has collided with an obstacle or itself.


## Getting Started

**Installation Requirements**

Make sure Python and MongoDB are installed on your system. MongoDB is used for data persistence, storing user sessions and leaderboard information.

**Setup and Installation:**

1. **Clone the repository:**
```bash
 git clone https://github.com/krookskala/Retro-Snake-Game
```
2. **Navigate to the project directory and install dependencies:**
```bash
cd RetroSnake
pip install -r requirements.txt

```

3. **Environment Setup:**
- Configure MongoDB connection strings and other environment-specific variables in a **.env** file.

**Running the Game:**

1. **Start the server:**

```bash
python RetroSnake.py
```

2. Open a web browser and go to start playing the game.
```bash
 http://127.0.0.1:5000/ 
```
## Detailed File Descriptions
- **RetroSnake.py:** Main Flask application file containing routes and game logic.

- **requirements.txt:** Lists all the Python libraries required for the project.

- **static/:** Contains static assets like CSS, JavaScript, and images.

- **templates/:** HTML templates for rendering views.

- **sounds/:** Directory containing sound files used throughout the game.







## Demo


https://github.com/user-attachments/assets/46d9d32b-e85f-4062-bc1b-121bf5116194
## Contributing

Contributions are welcome!

If you find any issues or have ideas for improvements, feel free to open an issue or submit a pull request.

Please make sure to follow the project's code of conduct.

1. **Fork the repository**
2. **Create your feature branch (git checkout -b feature/YourFeature)**
3. **Commit your changes (git commit -am 'Add some feature')**
4. **Push to the branch (git push origin feature/YourFeature)**
5. **Open a pull request**


## Links

[![Gmail](https://img.shields.io/badge/ismailsariarslan7@gmail.com-D14836?style=for-the-badge&logo=gmail&logoColor=white)](ismailsariarslan7@gmail.com)

[![instagram](https://img.shields.io/badge/Instagram-E4405F?style=for-the-badge&logo=instagram&logoColor=white)](https://www.instagram.com/ismailsariarslan/)

[![linkedin](https://img.shields.io/badge/linkedin-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/ismailsariarslan/)
## License

The code in this repository is licensed under the [MIT License.](https://choosealicense.com/licenses/mit/)

