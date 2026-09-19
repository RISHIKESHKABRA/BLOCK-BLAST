# BLOCK-BLAST

# 🕹️ Python Block Blast Game

A desktop implementation of the popular mobile **Block Blast** puzzle game built entirely in Python using the native **Tkinter** library. 

This project features a clean, responsive layout featuring standard 8x8 grid dynamics, score counters, dynamic block generation trays, and auto-checking mechanics for row and column clears.

---

## ✨ Features

- **8x8 Grid Mechanics:** Authentic grid-matching play area mimicking standard block puzzle designs.
- **Dynamic Block Generation:** Automatically populates three distinct block shapes when the tray is emptied.
- **Smart Clearance Engine:** Blasts rows and columns simultaneously with real-time combo score additions.
- **Embedded End-Game Check:** Calculates potential remaining placement slots to trigger a game-over sequence automatically.
- **Zero Heavy Dependencies:** Written completely in standard Python with standard cross-platform libraries.

---

## 🚀 Getting Started

### Prerequisites

You only need **Python 3.x** installed on your system. No external package installations (`pip`) are required.

### Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/block-blast-game.git
   ```
2. Navigate into the directory:
   ```bash
   cd block-blast-game
   ```

### Running the Game

Launch the application using Python:
```bash
python main.py
```

---

## 🎮 How to Play

1. **Select:** Click on one of the three generated shapes in the bottom tray.
2. **Target:** Click anywhere inside the main 8x8 grid. The block's top-left corner anchors onto your cursor's grid target.
3. **Blast:** Complete full vertical columns or horizontal rows to clear blocks out and stack up score points.
4. **Win Condition:** Keep clearing tiles! The game ends when none of the remaining tray shapes can fit into the empty space grid configurations.

---

## 🛠️ File Architecture

```text
├── main.py          # Entry point containing core Tkinter application logic
├── LICENSE          # MIT Open Source License
└── README.md        # Project overview and usage guidelines
```

---

## 📜 License

Distributed under the MIT License. See `LICENSE` for details.
