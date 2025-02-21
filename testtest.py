import streamlit as st
import archiver
from archiver import *

import uuid
from datetime import datetime, timezone

import uuid
from datetime import datetime, timezone

# Info Fields
info_fields = [
    Info(field_name="Full Name", item_type="text", field_description="Enter your full name.", priority=True),
    Info(field_name="Email Address", item_type="email", field_description="Enter your email address.", priority=True),
    Info(field_name="Phone Number", item_type="text", field_description="Enter your contact number."),
    Info(field_name="Age", item_type="number", field_description="Enter your age."),
    Info(field_name="Gender", item_type="dropdown", field_description="Select your gender."),
    Info(field_name="Country", item_type="dropdown", field_description="Select your country."),
    Info(field_name="Occupation", item_type="text", field_description="Enter your occupation."),
    Info(field_name="Education Level", item_type="dropdown", field_description="Select your highest qualification."),
    Info(field_name="Preferred Language", item_type="dropdown", field_description="Select your preferred language."),
    Info(field_name="Feedback", item_type="textarea", field_description="Provide any feedback you have.")
]

# Questions
questions = [
    Question(content="What is the capital of France?", options=["Paris", "Berlin", "Madrid", "Rome"], answer="Paris", subject="Geography", difficulty_rating=2),
    Question(content="Solve: 5 + 7", options=["10", "11", "12", "13"], answer="12", subject="Mathematics", difficulty_rating=1),
    Question(content="Who wrote 'Hamlet'?", options=["Shakespeare", "Chaucer", "Dickens", "Austen"], answer="Shakespeare", subject="Literature", difficulty_rating=2),
    Question(content="What is the chemical symbol for water?", options=["O2", "H2O", "CO2", "NaCl"], answer="H2O", subject="Science", difficulty_rating=1),
    Question(content="Which planet is known as the Red Planet?", options=["Earth", "Mars", "Jupiter", "Saturn"], answer="Mars", subject="Astronomy", difficulty_rating=2),
    Question(content="In what year did World War II end?", options=["1942", "1945", "1948", "1950"], answer="1945", subject="History", difficulty_rating=3),
    Question(content="What is the square root of 64?", options=["6", "7", "8", "9"], answer="8", subject="Mathematics", difficulty_rating=1),
    Question(content="Who painted the Mona Lisa?", options=["Van Gogh", "Picasso", "Da Vinci", "Michelangelo"], answer="Da Vinci", subject="Art", difficulty_rating=2),
    Question(content="What gas do plants absorb from the atmosphere?", options=["Oxygen", "Hydrogen", "Carbon Dioxide", "Nitrogen"], answer="Carbon Dioxide", subject="Science", difficulty_rating=2),
    Question(content="Which ocean is the largest?", options=["Atlantic", "Pacific", "Indian", "Arctic"], answer="Pacific", subject="Geography", difficulty_rating=2)
]

# Tests
tests = [
    Test(
        title="General Knowledge Test 1",
        client="Client A",
        subjects={"Geography": 10, "Mathematics": 10, "Literature": 10},
        total_score=30,
        submissions=5,
        submittedid={},
        infofields={info.id: info.field_name for info in info_fields[:5]},
        questions={question.id: 3 for question in questions[:3]}
    ),
    Test(
        title="Science and History Test",
        client="Client B",
        subjects={"Science": 20, "History": 10},
        total_score=30,
        submissions=3,
        submittedid={},
        infofields={info.id: info.field_name for info in info_fields[2:7]},
        questions={question.id: 3 for question in questions[3:6]}
    ),
    Test(
        title="Advanced Mathematics Test",
        client="Client C",
        subjects={"Mathematics": 30},
        total_score=30,
        submissions=4,
        submittedid={},
        infofields={info.id: info.field_name for info in info_fields[1:6]},
        questions={question.id: 5 for question in questions[1:7]}
    ),
    Test(
        title="Art and Science Combo Test",
        client="Client D",
        subjects={"Art": 10, "Science": 20},
        total_score=30,
        submissions=4,
        submittedid={},
        infofields={info.id: info.field_name for info in info_fields[0:4]},
        questions={question.id: 3 for question in questions[7:10]}
    )
]

# Responses for General Knowledge Test 1
responses = [
    Response(
        test_ID=tests[0].id,
        client="Client A",
        subject_scores={"Geography": 8, "Mathematics": 9, "Literature": 7},
        info = {
            list(tests[0].infofields.keys())[0]:"John Doe",
            list(tests[0].infofields.keys())[1]:"john@example.com",
            list(tests[0].infofields.keys())[2]:"1234567890",
            list(tests[0].infofields.keys())[3]:"30",
            list(tests[0].infofields.keys())[4]:"Male"
        },
        results={question_id: "Paris" for question_id in tests[0].questions.keys()}
    ),
    Response(
        test_ID=tests[0].id,
        client="Client A",
        subject_scores={"Geography": 7, "Mathematics": 8, "Literature": 6},
        info = {
            list(tests[0].infofields.keys())[0]:"Jane Smith",
            list(tests[0].infofields.keys())[1]:"jane@example.com",
            list(tests[0].infofields.keys())[2]:"0987654321",
            list(tests[0].infofields.keys())[3]:"25",
            list(tests[0].infofields.keys())[4]:"Female"
        },
        results={question_id: "Berlin" for question_id in tests[0].questions.keys()}
    ),
    Response(
        test_ID=tests[0].id,
        client="Client A",
        subject_scores={"Geography": 9, "Mathematics": 10, "Literature": 8},
        info = {
            list(tests[0].infofields.keys())[0]:"Sam Green",
            list(tests[0].infofields.keys())[1]:"sam@example.com",
            list(tests[0].infofields.keys())[2]:"1122334455",
            list(tests[0].infofields.keys())[3]:"28",
            list(tests[0].infofields.keys())[4]:"Non-binary"
        },
        results={question_id: "Paris" for question_id in tests[0].questions.keys()}
    ),
    Response(
        test_ID=tests[0].id,
        client="Client A",
        subject_scores={"Geography": 6, "Mathematics": 7, "Literature": 5},
        info = {
            list(tests[0].infofields.keys())[0]:"Alex White",
            list(tests[0].infofields.keys())[1]:"alex@example.com",
            list(tests[0].infofields.keys())[2]:"5566778899",
            list(tests[0].infofields.keys())[3]:"22",
            list(tests[0].infofields.keys())[4]:"Female"
        },
        results={question_id: "Madrid" for question_id in tests[0].questions.keys()}
    )
]

responses += [
    Response(
        test_ID=tests[1].id,
        client="Client B",
        subject_scores={"Science": 18, "History": 9},
        info = {
            list(tests[1].infofields.keys())[0]:"Emily Brown",
            list(tests[1].infofields.keys())[1]:"emily@example.com",
            list(tests[1].infofields.keys())[2]:"6677889900",
            list(tests[1].infofields.keys())[3]:"35",
            list(tests[1].infofields.keys())[4]:"Female"
        },
        results={question_id: "H2O" for question_id in tests[1].questions.keys()}
    ),
    Response(
        test_ID=tests[1].id,
        client="Client B",
        subject_scores={"Science": 16, "History": 8},
        info = {
            list(tests[1].infofields.keys())[0]:"Mark Black",
            list(tests[1].infofields.keys())[1]:"mark@example.com",
            list(tests[1].infofields.keys())[2]:"4455667788",
            list(tests[1].infofields.keys())[3]:"40",
            list(tests[1].infofields.keys())[4]:"Male"
        },
        results={question_id: "CO2" for question_id in tests[1].questions.keys()}
    ),
    Response(
        test_ID=tests[1].id,
        client="Client B",
        subject_scores={"Science": 19, "History": 10},
        info = {
            list(tests[1].infofields.keys())[0]:"Sophia Grey",
            list(tests[1].infofields.keys())[1]:"sophia@example.com",
            list(tests[1].infofields.keys())[2]:"2233445566",
            list(tests[1].infofields.keys())[3]:"29",
            list(tests[1].infofields.keys())[4]:"Female"
        },
        results={question_id: "H2O" for question_id in tests[1].questions.keys()}
    ),
    Response(
        test_ID=tests[1].id,
        client="Client B",
        subject_scores={"Science": 14, "History": 7},
        info = {
            list(tests[1].infofields.keys())[0]:"Luke Grey",
            list(tests[1].infofields.keys())[1]:"luke@example.com",
            list(tests[1].infofields.keys())[2]:"9988776655",
            list(tests[1].infofields.keys())[3]:"32",
            list(tests[1].infofields.keys())[4]:"Male"
        },
        results={question_id: "O2" for question_id in tests[1].questions.keys()}
    )
]

responses += [
    Response(
        test_ID=tests[2].id,
        client="Client C",
        subject_scores={"Mathematics": 28},
        info = {
            list(tests[2].infofields.keys())[0]:"Oliver Green",
            list(tests[2].infofields.keys())[1]:"oliver@example.com",
            list(tests[2].infofields.keys())[2]:"3344556677",
            list(tests[2].infofields.keys())[3]:"27",
            list(tests[2].infofields.keys())[4]:"Male"
        },
        results={question_id: "12" for question_id in tests[2].questions.keys()}
    ),
    Response(
        test_ID=tests[2].id,
        client="Client C",
        subject_scores={"Mathematics": 25},
        info = {
            list(tests[2].infofields.keys())[0]:"Mia Red",
            list(tests[2].infofields.keys())[1]:"mia@example.com",
            list(tests[2].infofields.keys())[2]:"7766554433",
            list(tests[2].infofields.keys())[3]:"26",
            list(tests[2].infofields.keys())[4]:"Female"
        },
        results={question_id: "8" for question_id in tests[2].questions.keys()}
    ),
    Response(
        test_ID=tests[2].id,
        client="Client C",
        subject_scores={"Mathematics": 29},
        info = {
            list(tests[2].infofields.keys())[0]:"Ella Blue",
            list(tests[2].infofields.keys())[1]:"ella@example.com",
            list(tests[2].infofields.keys())[2]:"1122112211",
            list(tests[2].infofields.keys())[3]:"30",
            list(tests[2].infofields.keys())[4]:"Female"
        },
        results={question_id: "8" for question_id in tests[2].questions.keys()}
    ),
    Response(
        test_ID=tests[2].id,
        client="Client C",
        subject_scores={"Mathematics": 20},
        info = {
            list(tests[2].infofields.keys())[0]:"Noah Brown",
            list(tests[2].infofields.keys())[1]:"noah@example.com",
            list(tests[2].infofields.keys())[2]:"9988445566",
            list(tests[2].infofields.keys())[3]:"33",
            list(tests[2].infofields.keys())[4]:"Male"
        },
        results={question_id: "6" for question_id in tests[2].questions.keys()}
    )
]

responses += [
    Response(
        test_ID=tests[3].id,
        client="Client D",
        subject_scores={"Art": 9, "Science": 18},
        info = {
            list(tests[3].infofields.keys())[0]:"Lily White",
            list(tests[3].infofields.keys())[1]:"lily@example.com",
            list(tests[3].infofields.keys())[2]:"4433221100",
            list(tests[3].infofields.keys())[3]:"31"
        },
        results={question_id: "Da Vinci" for question_id in tests[3].questions.keys()}
    ),
    Response(
        test_ID=tests[3].id,
        client="Client D",
        subject_scores={"Art": 7, "Science": 15},
        info = {
            list(tests[3].infofields.keys())[0]:"Leo Silver",
            list(tests[3].infofields.keys())[1]:"leo@example.com",
            list(tests[3].infofields.keys())[2]:"2233114455",
            list(tests[3].infofields.keys())[3]:"29"
        },
        results={question_id: "Van Gogh" for question_id in tests[3].questions.keys()}
    ),
    Response(
        test_ID=tests[3].id,
        client="Client D",
        subject_scores={"Art": 8, "Science": 17},
        info = {
            list(tests[3].infofields.keys())[0]:"Grace Gold",
            list(tests[3].infofields.keys())[1]:"grace@example.com",
            list(tests[3].infofields.keys())[2]:"6655443322",
            list(tests[3].infofields.keys())[3]:"34"
        },
        results={question_id: "Da Vinci" for question_id in tests[3].questions.keys()}
    ),
    Response(
        test_ID=tests[3].id,
        client="Client D",
        subject_scores={"Art": 10, "Science": 19},
        info = {
            list(tests[3].infofields.keys())[0]:"Ivy Black",
            list(tests[3].infofields.keys())[1]:"ivy@example.com",
            list(tests[3].infofields.keys())[2]:"5566778899",
            list(tests[3].infofields.keys())[3]:"28"
        },
        results={question_id: "Da Vinci" for question_id in tests[3].questions.keys()}
    )
]


print(archiver.add_info_field(info_fields))
print(archiver.add_question(questions))
for i in tests:
    print(archiver.create_test(i))
for i in responses:
    print(archiver.add_response(i))