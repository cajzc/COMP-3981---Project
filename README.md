# COMP-3981---Project


![Abalone Board](https://upload.wikimedia.org/wikipedia/commons/thumb/7/7c/Abalone_board.jpg/320px-Abalone_board.jpg)

An intelligent game-playing agent for the board game *Abalone*, implementing adversarial search strategies with performance optimizations.

---

## Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Heuristic Design](#heuristic-design)
- [Performance Enhancements](#performance-enhancements)
- [Team Contributions](#team-contributions)
- [License](#license)

---

## Features
- **Core Algorithms**:
  - Minimax with Alpha-Beta Pruning
  - Randomized first move for Black player
- **Heuristic Evaluation**:
  - Distance-to-center optimization
  - Marble cluster coherence analysis
  - Danger detection for vulnerable marbles
  - Opponent formation disruption scoring
- **Performance Optimizations**:
  - Transposition tables for state caching
  - Move ordering (Killer Heuristic)
- **Integration**:
  - Compatible with standard Abalone board configurations
  - Supports `.input`/`.output` file formats for game states

---

## Installation

### Prerequisites
- Python 3.12+
- `pip` package manager

### Steps
1. Clone repository:
   ```bash
   https://github.com/cajzc/COMP-3981---Project.git