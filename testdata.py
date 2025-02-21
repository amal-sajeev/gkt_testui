
import pymongo
import uuid
from datetime import datetime, timezone
from archiver import *
import archiver
import pandas

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

import uuid
from datetime import datetime, timezone
from pydantic import BaseModel, Field
from typing import Dict

# Assuming the Test class is already defined

# Create Test objects with submission data
# Test Objects

test1 = Test(
    title="Algebra Basics",
    client="School A",
    subjects={"Math": 100},
    total_score=100,
    submissions=10,
    submittedid={
        str(uuid.uuid4()): 95,
        str(uuid.uuid4()): 80,
        str(uuid.uuid4()): 45,  # Fail
        str(uuid.uuid4()): 60,
        str(uuid.uuid4()): 50,  # Fail
        str(uuid.uuid4()): 30,  # Fail
        str(uuid.uuid4()): 85,
        str(uuid.uuid4()): 90,
        str(uuid.uuid4()): 55,  # Fail
        str(uuid.uuid4()): 100
    },
    questions={"Q1": 10, "Q2": 20, "Q3": 30, "Q4": 40}
)

test2 = Test(
    title="Physics Principles",
    client="School B",
    subjects={"Science": 120},
    total_score=120,
    submissions=12,
    submittedid={
        str(uuid.uuid4()): 110,
        str(uuid.uuid4()): 75,
        str(uuid.uuid4()): 50,  # Fail
        str(uuid.uuid4()): 40,  # Fail
        str(uuid.uuid4()): 80,
        str(uuid.uuid4()): 55,  # Fail
        str(uuid.uuid4()): 90,
        str(uuid.uuid4()): 60,
        str(uuid.uuid4()): 100,
        str(uuid.uuid4()): 115,
        str(uuid.uuid4()): 45,  # Fail
        str(uuid.uuid4()): 30   # Fail
    },
    questions={"Q1": 30, "Q2": 30, "Q3": 30, "Q4": 30}
)

test3 = Test(
    title="World History",
    client="School C",
    subjects={"History": 90},
    total_score=90,
    submissions=10,
    submittedid={
        str(uuid.uuid4()): 88,
        str(uuid.uuid4()): 60,
        str(uuid.uuid4()): 50,  # Fail
        str(uuid.uuid4()): 35,  # Fail
        str(uuid.uuid4()): 72,
        str(uuid.uuid4()): 45,  # Fail
        str(uuid.uuid4()): 70,
        str(uuid.uuid4()): 55,  # Fail
        str(uuid.uuid4()): 40,  # Fail
        str(uuid.uuid4()): 85
    },
    questions={"Q1": 30, "Q2": 30, "Q3": 30}
)

test4 = Test(
    title="English Literature",
    client="School D",
    subjects={"English": 150},
    total_score=150,
    submissions=11,
    submittedid={
        str(uuid.uuid4()): 120,
        str(uuid.uuid4()): 130,
        str(uuid.uuid4()): 90,  # Fail
        str(uuid.uuid4()): 45,  # Fail
        str(uuid.uuid4()): 60,
        str(uuid.uuid4()): 135,
        str(uuid.uuid4()): 50,  # Fail
        str(uuid.uuid4()): 75,
        str(uuid.uuid4()): 115,
        str(uuid.uuid4()): 80,  # Fail
        str(uuid.uuid4()): 100
    },
    questions={"Q1": 50, "Q2": 50, "Q3": 50}
)

test5 = Test(
    title="Basic Programming",
    client="School E",
    subjects={"Computer Science": 200},
    total_score=200,
    submissions=15,
    submittedid={
        str(uuid.uuid4()): 180,
        str(uuid.uuid4()): 95,  # Fail
        str(uuid.uuid4()): 190,
        str(uuid.uuid4()): 170,
        str(uuid.uuid4()): 50,  # Fail
        str(uuid.uuid4()): 110,
        str(uuid.uuid4()): 120,
        str(uuid.uuid4()): 105,
        str(uuid.uuid4()): 60,  # Fail
        str(uuid.uuid4()): 130,
        str(uuid.uuid4()): 140,
        str(uuid.uuid4()): 85,  # Fail
        str(uuid.uuid4()): 45,  # Fail
        str(uuid.uuid4()): 90,  # Fail
        str(uuid.uuid4()): 195
    },
    questions={"Q1": 100, "Q2": 50, "Q3": 50}
)

# Additional 10 test objects follow the same structure:

test6 = Test(
    title="Chemistry Essentials",
    client="School F",
    subjects={"Science": 100},
    total_score=100,
    submissions=10,
    submittedid={
        str(uuid.uuid4()): 95,
        str(uuid.uuid4()): 60,
        str(uuid.uuid4()): 55,  # Fail
        str(uuid.uuid4()): 45,  # Fail
        str(uuid.uuid4()): 80,
        str(uuid.uuid4()): 70,
        str(uuid.uuid4()): 50,  # Fail
        str(uuid.uuid4()): 85,
        str(uuid.uuid4()): 40,  # Fail
        str(uuid.uuid4()): 90
    },
    questions={"Q1": 20, "Q2": 30, "Q3": 50}
)

test7 = Test(
    title="Philosophy 101",
    client="School G",
    subjects={"Philosophy": 70},
    total_score=70,
    submissions=12,
    submittedid={
        str(uuid.uuid4()): 65,
        str(uuid.uuid4()): 40,  # Fail
        str(uuid.uuid4()): 35,  # Fail
        str(uuid.uuid4()): 55,
        str(uuid.uuid4()): 50,  # Fail
        str(uuid.uuid4()): 45,  # Fail
        str(uuid.uuid4()): 70,
        str(uuid.uuid4()): 68,
        str(uuid.uuid4()): 30,  # Fail
        str(uuid.uuid4()): 60,
        str(uuid.uuid4()): 25,  # Fail
        str(uuid.uuid4()): 70
    },
    questions={"Q1": 20, "Q2": 20, "Q3": 30}
)

test8 = Test(
    title="Statistics Basics",
    client="School H",
    subjects={"Math": 110},
    total_score=110,
    submissions=11,
    submittedid={
        str(uuid.uuid4()): 90,
        str(uuid.uuid4()): 50,  # Fail
        str(uuid.uuid4()): 45,  # Fail
        str(uuid.uuid4()): 105,
        str(uuid.uuid4()): 70,
        str(uuid.uuid4()): 40,  # Fail
        str(uuid.uuid4()): 100,
        str(uuid.uuid4()): 55,  # Fail
        str(uuid.uuid4()): 85,
        str(uuid.uuid4()): 110,
        str(uuid.uuid4()): 30   # Fail
    },
    questions={"Q1": 30, "Q2": 30, "Q3": 50}
)

test9 = Test(
    title="Biology Foundations",
    client="School I",
    subjects={"Science": 130},
    total_score=130,
    submissions=10,
    submittedid={
        str(uuid.uuid4()): 125,
        str(uuid.uuid4()): 80,
        str(uuid.uuid4()): 50,  # Fail
        str(uuid.uuid4()): 65,
        str(uuid.uuid4()): 60,
        str(uuid.uuid4()): 55,  # Fail
        str(uuid.uuid4()): 100,
        str(uuid.uuid4()): 120,
        str(uuid.uuid4()): 45,  # Fail
        str(uuid.uuid4()): 70
    },
    questions={"Q1": 50, "Q2": 30, "Q3": 50}
)

test10 = Test(
    title="Economics Principles",
    client="School J",
    subjects={"Economics": 90},
    total_score=90,
    submissions=12,
    submittedid={
        str(uuid.uuid4()): 85,
        str(uuid.uuid4()): 40,  # Fail
        str(uuid.uuid4()): 55,  # Fail
        str(uuid.uuid4()): 65,
        str(uuid.uuid4()): 70,
        str(uuid.uuid4()): 45,  # Fail
        str(uuid.uuid4()): 50,  # Fail
        str(uuid.uuid4()): 90,
        str(uuid.uuid4()): 60,
        str(uuid.uuid4()): 30,  # Fail
        str(uuid.uuid4()): 75,
        str(uuid.uuid4()): 20   # Fail
    },
    questions={"Q1": 30, "Q2": 30, "Q3": 30}
)

# Put them in a list
tests = [test1, test2, test3, test4, test5, test6, test7, test8, test9, test10]


# print(archiver.get_test_options(get_subjects=True))
# for i in tests:
#     print(archiver.create_test(i))
# print(archiver.test_by_id("02a00d5e-9bb2-4600-a856-bc54e05865d9"))
