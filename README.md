#  Adaptive Math Learning System

An intelligent learning platform that dynamically adjusts math puzzle difficulty based on real-time student performance for children aged 5-10.

## Features

- **Dynamic puzzle generation** with emoji-based visual problems
- **Adaptive difficulty** using rule-based or ML algorithms
- **Performance tracking** (correctness, response time, streaks)
- **Kid-friendly interface** with encouraging feedback
- **Session summaries** with recommendations

## Tech Stack

- Python 3.8+
- Streamlit (UI)
- scikit-learn (ML)
- pandas, numpy (Data)

## Installation

```bash
# Clone repository
git clone https://github.com/chandrakanth172/math-adaptive-prototype.git
cd math-adaptive-prototype

# Install dependencies
pip install -r requirements.txt

# Run application
streamlit run src/main.py
```

## Project Structure

```
math-adaptive-prototype/
├── README.md
├── requirements.txt
└── src/
    ├── main.py                # Entry point
    ├── puzzle_generator.py    # Puzzle generation
    ├── tracker.py             # Performance tracking
    └── adaptive_engine.py     # Adaptive logic
```

## How It Works

The system adapts difficulty using two methods: Users Choice

**Rule-Based**: 3 correct in a row → level up, 2 wrong in a row → level down  
**ML-Based**: Decision tree using accuracy, response time, and streaks

## Usage

1. Enter your name
2. Select any one method "Rule based" or "ML based"
3. Select starting difficulty (Easy/Medium/Hard)
4. Answer math questions
5. Get real-time adaptive difficulty adjustments
6. View performance summary and recommendations


## Author

**Chandrakanth Bavoju**  
