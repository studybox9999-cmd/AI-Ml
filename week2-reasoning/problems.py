"""
Week 2 Lab - Benchmark problem set.
10-word problems of increasing difficulty.
Each has a known integer answer.
"""

PROBLEMS = [

    # === Easy (3) ===
    {
        "id": "P01",
        "difficulty": "easy",
        "question": "A juggler has 16 balls. Half are golf balls, and half of the golf balls are blue. How many blue golf balls does the juggler have?",
        "answer": 4,
    },

    {
        "id": "P02",
        "difficulty": "easy",
        "question": "Sarah read 12 pages on Monday, twice as many on Tuesday, and 5 fewer than Tuesday's count on Wednesday. How many pages did she read in total?",
        "answer": 55,
    },

    {
        "id": "P03",
        "difficulty": "easy",
        "question": "A box has 30 chocolates. Maya eats 1/5 of them, then her brother eats half of what's left. How many chocolates remain?",
        "answer": 12,
    },


    # === Medium (4) ===
    {
        "id": "P04",
        "difficulty": "medium",
        "question": "A bakery sells muffins for $2 each and croissants for $3 each. On Tuesday, they sold 18 muffins and 24 croissants. They donated 20% of the day's revenue to charity. How many dollars did they donate?",
        "answer": 22,
    },

    {
        "id": "P05",
        "difficulty": "medium",
        "question": "A train leaves Station A at 9:00 AM traveling 60 mph. Another train leaves Station B at 10:00 AM traveling 80 mph toward Station A. The stations are 320 miles apart. At what time (hour, in 24-hour format) do the trains meet?",
        "answer": 12,
    },

    {
        "id": "P06",
        "difficulty": "medium",
        "question": "If a rectangular garden's length is 3 meters more than twice its width, and the perimeter is 36 meters, what is the width in meters?",
        "answer": 5,
    },

    {
        "id": "P07",
        "difficulty": "medium",
        "question": "Tom has 3 times as many marbles as Jerry. After Tom gives Jerry 12 marbles, they have the same number. How many marbles did Tom originally have?",
        "answer": 36,
    },


    # === Hard (3) ===
    {
        "id": "P08",
        "difficulty": "hard",
        "question": "In a classroom, the ratio of boys to girls is 3:5. If 6 more boys joined and 4 girls left, the new ratio would be 4:5. How many boys were in the classroom originally?",
        "answer": 18,
    },

    {
        "id": "P09",
        "difficulty": "hard",
        "question": "A mother is currently 4 times her daughter's age. In 6 years, she will be only 2.5 times her daughter's age. How old is the daughter now?",
        "answer": 6,
    },

    {
        "id": "P10",
        "difficulty": "hard",
        "question": "Five friends — A, B, C, D, E — are sitting in a row. A is not next to B. C is between A and D. E is at one end. D is not at an end. The seat positions (1=leftmost, 5=rightmost) of A, B, C, D, E are unique. What is the position of A?",
        "answer": 1,
    },
]


def get_problems():
    return PROBLEMS