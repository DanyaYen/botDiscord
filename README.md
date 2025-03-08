# botDiscord

First discord bot for fun.

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Introduction
`botDiscord` is a Discord bot created for fun using Python. It includes various commands and features to enhance your Discord server experience.

## Features
- Responds to user commands with predefined messages.
- Moderation commands to manage the server.
- Fun commands to entertain users.
- Customizable settings and commands.

## Installation
To install and run the bot, follow these steps:

1. Clone the repository:
    ```bash
    git clone https://github.com/DanyaYen/botDiscord.git
    cd botDiscord
    ```

2. Create a virtual environment and activate it:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Create a `.env` file in the root directory and add your Discord bot token:
    ```env
    DISCORD_TOKEN=your_discord_bot_token_here
    ```

5. Run the bot:
    ```bash
    python bot.py
    ```

## Usage
Once the bot is running, you can invite it to your Discord server and use the following commands:

- `!hello` - The bot will greet you.
- `!moderate` - Moderation commands for managing the server.
- `!fun` - Fun commands to entertain users.

Feel free to explore and modify the bot's code to add more features and commands.

## Contributing
Contributions are welcome! If you have any ideas, suggestions, or improvements, feel free to open an issue or submit a pull request.

1. Fork the repository.
2. Create a new branch:
    ```bash
    git checkout -b feature/your-feature-name
    ```
3. Make your changes and commit them:
    ```bash
    git commit -m 'Add some feature'
    ```
4. Push to the branch:
    ```bash
    git push origin feature/your-feature-name
    ```
5. Open a pull request.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
