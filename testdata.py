# from archiver import *
# import archiver

# newq = Question(
#     content = "hahahehe",
#     options = ["hehe","hoohoo","haha"],
#     answer = "haha",
#     subjectid = "hehe",
#     subject_name = "hahaha",
#     difficulty_rating = 2
# )

# print(newq.model_dump())
# archiver.add_question(newq)\

import pymongo
import uuid
from datetime import datetime, timezone
# Info objects (for candidate personal information)
info_objects = [
    {
        "_id": str(uuid.uuid4()),
        "field_name": "Email address",
        "item_type": "text"
    },
    {
        "_id": str(uuid.uuid4()),
        "field_name": "Name",
        "item_type": "text"
    },
    {
        "_id": str(uuid.uuid4()),
        "field_name": "College Name",
        "item_type": "text"
    },
    {
        "_id": str(uuid.uuid4()),
        "field_name": "Location",
        "item_type": "text"
    },
    {
        "_id": str(uuid.uuid4()),
        "field_name": "Class 10 Graduation Percentage",
        "item_type": "text"
    },
    {
        "_id": str(uuid.uuid4()),
        "field_name": "Class 12 Graduation Percentage",
        "item_type": "text"
    },
    {
        "_id": str(uuid.uuid4()),
        "field_name": "Graduation type",
        "item_type": "text"
    },
    {
        "_id": str(uuid.uuid4()),
        "field_name": "Graduation Percentage",
        "item_type": "text"
    },
    {
        "_id": str(uuid.uuid4()),
        "field_name": "Year of Graduation",
        "item_type": "text"
    },
    {
        "_id": str(uuid.uuid4()),
        "field_name": "Do you have any backlog subjects?",
        "item_type": "text"
    },
    {
        "_id": str(uuid.uuid4()),
        "field_name": "Date of Birth",
        "item_type": "text"
    },
    {
        "_id": str(uuid.uuid4()),
        "field_name": "Phone",
        "item_type": "text"
    },
    {
        "_id": str(uuid.uuid4()),
        "field_name": "Work Experience (in years)",
        "item_type": "text"
    }
]

# Question objects (from the math/logical reasoning questions)
aptitude_questions = [
    {
        "_id": str(uuid.uuid4()),
        "content": "P, Q and R are three cities. The ratio of average temperature between P and Q is 11: 12 and that between P and R is 9: 8. What is the ratio between the average temperature of Q and R?",
        "images": [],
        "options": ["24:25", "27:22", "22:27", "25:24"],
        "answer": "27:22",
        "subjectid": str(uuid.uuid4()),
        "subject_name": "Quantitative Aptitude",
        "difficulty_rating": 3
    },
    {
        "_id": str(uuid.uuid4()),
        "content": "A person is planning to go on a weekend trip. He can drive 8 hours a day. The average speed he can drive forward at is 40 kmph, however, due to traffic on Sundays, the average speed on the return journey would only be 30 kmph. How far would his selected picnic spot be?",
        "images": [],
        "options": ["120 km", "140 km", "160 km", "180 km"],
        "answer": "120 km",
        "subjectid": str(uuid.uuid4()),
        "subject_name": "Quantitative Aptitude",
        "difficulty_rating": 2
    },
    {
        "_id": str(uuid.uuid4()),
        "content": "The incomes of A & B are in the ratio 3:2 and their expenditures in the ratio 5:3. If each of them save ₹1000, what would A's income be?",
        "images": [],
        "options": ["₹5000", "₹6000", "₹7500", "₹9000"],
        "answer": "₹6000",
        "subjectid": str(uuid.uuid4()),
        "subject_name": "Quantitative Aptitude",
        "difficulty_rating": 3
    },
    {
        "_id": str(uuid.uuid4()),
        "content": "The age of a person is twice the sum of the ages of his two sons, and five years ago his age was thrice the sum of their ages. Find his present age.",
        "images": [],
        "options": ["40 years", "45 years", "50 years", "55 years"],
        "answer": "50 years",
        "subjectid": str(uuid.uuid4()),
        "subject_name": "Quantitative Aptitude",
        "difficulty_rating": 3
    },
    {
        "_id": str(uuid.uuid4()),
        "content": "A number between 10 and 100 is five times the sum of its digits. If 9 is added to it, the digits are reversed. Find the number.",
        "images": [],
        "options": ["27", "36", "45", "54"],
        "answer": "45",
        "subjectid": str(uuid.uuid4()),
        "subject_name": "Quantitative Aptitude",
        "difficulty_rating": 4
    }
]

# More questions for logical reasoning
logical_questions = [
    {
        "_id": str(uuid.uuid4()),
        "content": "A monkey starts climbing up a tree 20ft. tall. Each hour, it hops 3ft. and slips back 2ft. How much time would it take the monkey to reach the top?",
        "images": [],
        "options": ["12 hours", "18 hours", "20 hours", "24 hours"],
        "answer": "18 hours",
        "subjectid": str(uuid.uuid4()),
        "subject_name": "Logical Reasoning",
        "difficulty_rating": 2
    },
    {
        "_id": str(uuid.uuid4()),
        "content": "What number comes next in the following series? 56, 54, 40, 48, 44, …",
        "images": [],
        "options": ["30", "36", "42", "50"],
        "answer": "42",
        "subjectid": str(uuid.uuid4()),
        "subject_name": "Logical Reasoning",
        "difficulty_rating": 3
    },
    {
        "_id": str(uuid.uuid4()),
        "content": "The hour hand of a clock points toward west when the time is 3 o' clock. Then, what would be the direction of the minute hand when time is 6:45?",
        "images": [],
        "options": ["North", "East", "South", "West"],
        "answer": "East",
        "subjectid": str(uuid.uuid4()),
        "subject_name": "Logical Reasoning",
        "difficulty_rating": 3
    }
]

# Combine all questions
all_questions = aptitude_questions + logical_questions

# Generate Test object
quantitative_subject_id = aptitude_questions[0]["subjectid"]
logical_subject_id = logical_questions[0]["subjectid"]

test_object = {
    "_id": str(uuid.uuid4()),
    "title": "Aptitude and Reasoning Assessment Test",
    "client": "Tech Recruitment Company",
    "subjects": [
        {
            "subjectid": quantitative_subject_id,
            "subject_name": "Quantitative Aptitude",
            "subject_total": 50
        },
        {
            "subjectid": logical_subject_id,
            "subject_name": "Logical Reasoning",
            "subject_total": 30
        }
    ],
    "publish_date": datetime.now(tz=timezone.utc),
    "total_score": 80,
    "submissions": 1,
    "submittedid": ["candidate123"],
    "questions": {question["_id"]: 10 for question in all_questions},
    "negative_multiplier": 0.25
}

# Generate Results object based on the candidate's answers from spreadsheet
info_responses = [
    {"infoid": info_objects[0]["_id"], "response": "test1@gmail.com"},
    {"infoid": info_objects[1]["_id"], "response": "test1"},
    {"infoid": info_objects[2]["_id"], "response": "test"},
    {"infoid": info_objects[3]["_id"], "response": "test"},
    {"infoid": info_objects[4]["_id"], "response": "test"},
    {"infoid": info_objects[5]["_id"], "response": "test"},
    {"infoid": info_objects[6]["_id"], "response": "test"},
    {"infoid": info_objects[7]["_id"], "response": "test"},
    {"infoid": info_objects[8]["_id"], "response": "test"},
    {"infoid": info_objects[9]["_id"], "response": "No"},
    {"infoid": info_objects[10]["_id"], "response": "29/01/2025"},
    {"infoid": info_objects[11]["_id"], "response": "test"},
    {"infoid": info_objects[12]["_id"], "response": "test"}
]

# Map candidate's answers to questions
results_responses = {}
for i, question in enumerate(all_questions):
    # Simulating answers from the spreadsheet data for the questions
    if i == 0:
        results_responses[question["_id"]] = "27:22"
    elif i == 1:
        results_responses[question["_id"]] = "120 km"
    elif i == 2:
        results_responses[question["_id"]] = "₹6000"
    elif i == 3:
        results_responses[question["_id"]] = "50 years"
    elif i == 4:
        results_responses[question["_id"]] = "45"
    elif i == 5:
        results_responses[question["_id"]] = "18 hours"
    elif i == 6:
        results_responses[question["_id"]] = "42"
    elif i == 7:
        results_responses[question["_id"]] = "East"

# Calculate scores based on responses
aptitude_score = sum(10 for q in aptitude_questions if results_responses.get(q["_id"]) == q["answer"])
logical_score = sum(10 for q in logical_questions if results_responses.get(q["_id"]) == q["answer"])

response_object = {
    "_id": str(uuid.uuid4()),
    "test_ID": test_object["_id"],
    "submission_date": datetime.now(tz=timezone.utc),
    "subject_scores": [
        {
            "subjectid": quantitative_subject_id,
            "subject_name": "Quantitative Aptitude",
            "subject_score": aptitude_score
        },
        {
            "subjectid": logical_subject_id,
            "subject_name": "Logical Reasoning",
            "subject_score": logical_score
        }
    ],
    "info": info_responses,
    "results": results_responses
}

mongoclient = pymongo.MongoClient("mongodb://datamaster:B8znzNgx2559BzWF1EJw@localhost:27017/")
db = mongoclient["examio"]

db.info.insert_many(info_objects)
db.questions.insert_many(all_questions)
db.tests.insert_one(test_object)
db.results.insert_one(response_object)