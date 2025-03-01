# Speed: Card Game

![Speed Preview](https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExY3gwdTNnbDZuZm5qYXk0eWNwY2E3dGYyaTI4Y3ZmdTRyY3Z5ZGc4dCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/qdd2ZDXolHG7G1BEqP/giphy.gif)

## Overview
Speed is a fast-paced two-player card game where players must quickly play cards in sequence onto central piles. This implementation of Speed is built using **Python**, **Pygame**, and **52CardEngine**.

## Features
- **Single-player mode** against an AI opponent.
- **Graphical User Interface (GUI)** using Pygame and ThorPy.
- **Deck management and card interactions** powered by 52CardEngine.
- **Smooth animations** and game logic for a dynamic experience.

## Installation

### Prerequisites
Ensure you have **Python 3.8+** installed on your system.

### Install Dependencies
Run the following command to install required dependencies:
```sh
pip install -r requirements.txt
```
## Running the Game
To start the game, run:
```sh
python main.py
```

## How to Play
1. The game starts with both players receiving **20 cards** each.
2. Players can place a card on the central piles if it is **one rank higher or lower** than the top card.
3. If no legal moves are available, both players draw a new card from their decks.
4. The first player to play all their cards **wins**.

## Controls
- **Click** on a card in your hand to attempt a move.
- The AI opponent will also play moves automatically.
- The game automatically progresses if both players are stuck.

## Game Structure
The game consists of three main classes:
- **Menu**: Handles the main menu UI using ThorPy.
- **Speed**: Implements the game logic and interactions.
- **Control**: Manages state transitions and the game loop.