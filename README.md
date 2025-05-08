# 🎙️ audioChess

**audioChess** is a voice-controlled chess game built with Python. It allows players to engage in a classic game of chess using voice commands, enhancing accessibility and providing a hands-free gaming experience.

## 🧩 Features

* **Voice Command Integration**: Play chess using voice inputs, making the game accessible for users with disabilities or those seeking a hands-free experience.
* **Python-Based Implementation**: Leverages Python for game logic and voice recognition functionalities.
* **Modular Code Structure**: Organized codebase with separate modules for constants, additional functions, and the main application logic.

## 📁 Project Structure

```
audioChess/
├── assets/
│   └── images/           # Contains image assets for the game
├── additions.py          # Additional helper functions
├── constants.py          # Constant values used across the application
├── main.py               # Main application file to run the game
└── README.md             # Project documentation
```

## 🚀 Getting Started

### Prerequisites

* Python 3.13 installed on your system
* Required Python libraries:

  * `speech_recognition`
  * `pygame`

You can install the necessary libraries using pip:

```bash
pip install speechrecognition pygame numpy scipy sounddevice
pip install openai-whisper
```

### Running the Game

1. Clone the repository:

   ```bash
   git clone https://github.com/relan1997/audioChess.git
   cd audioChess
   ```

2. Run the main application:

   ```bash
   python main.py
   ```


## 🎮 How to Play

* Use standard chess notations to move pieces. For example, say " select E2" then in order to move the piece at E2 to E4 give this command after the previous one "select E4" to move the chess piece.
* You can even ask for suggestions by the voice command "Suggest move" and the system will provide you with the best possible move by using the Mini-Max algorithm (alpha-beta prunning).
* The game will provide audio feedback for each move such as "White's turn", "Black's turn", "Error parsing the command try again", "Move Suggested" .
* If you want to forfeit the game then either press the "Forfeit" button or say the voice command "End Game".

## 🤝 Contributing

Contributions are welcome! If you'd like to enhance the game's features or fix bugs, please fork the repository and submit a pull request.

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.


