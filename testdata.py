
import pymongo
import uuid
from datetime import datetime, timezone
from archiver import *
import archiver

questions = [
    Question(
        content="What is the capital of France?",
        options=["Paris", "London", "Berlin", "Madrid"],
        answer="Paris",
        subject="Geography",
        difficulty_rating=1
    ),
    Question(
        content="Solve for x: 2x + 5 = 13",
        options=["x = 4", "x = 3", "x = 5", "x = 6"],
        answer="x = 4",
        subject="Mathematics",
        difficulty_rating=2
    ),
    Question(
        content="Which of the following is an ionic compound?",
        options=["NaCl", "CH4", "C6H12O6", "CO2"],
        answer="NaCl",
        subject="Chemistry",
        difficulty_rating=3
    ),
    Question(
        content="What is the correct HTML tag for the largest heading?",
        options=["<h1>", "<heading>", "<h6>", "<head>"],
        answer="<h1>",
        subject="Computer Science",
        difficulty_rating=1
    ),
    Question(
        content="Identify the function graphed below:",
        options=["y = x²", "y = x³", "y = sin(x)", "y = log(x)"],
        answer="y = sin(x)",
        subject="Mathematics",
        difficulty_rating=4
    ),
    Question(
        content="Which organelle is known as the 'powerhouse of the cell'?",
        options=["Mitochondria", "Nucleus", "Ribosome", "Golgi apparatus"],
        answer="Mitochondria",
        subject="Biology",
        difficulty_rating=2
    ),
    Question(
        content="Which of these elements has the highest atomic number?",
        options=["Gold", "Silver", "Lead", "Iron"],
        answer="Lead",
        subject="Chemistry",
        difficulty_rating=3
    ),
    Question(
        content="Identify the Shakespeare play from this quote: 'To be, or not to be, that is the question'",
        options=["Hamlet", "Macbeth", "Romeo and Juliet", "King Lear"],
        answer="Hamlet",
        subject="Literature",
        difficulty_rating=2
    )
]
# archiver.add_question(questions)

# print(archiver.search_questions())

print(archiver.get_test_options(get_subjects=True))