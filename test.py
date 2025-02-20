from archiver import *

#INFO CRUD TESTS

print("===========================================\n COMMENCING INFO FIELD CRUD TESTS \n=========================================== ")
# Create an info field
info = Info(field_name="Test Field", item_type="text", field_description="A test field")
inserted_id = add_info_field(info)
print(f"Inserted ID: {inserted_id}")

# Retrieve info by name
retrieved_info = info_by_name("Test Field")
print(f"Retrieved Info: {retrieved_info}")

# Retrieve info by ID
retrieved_by_id = info_by_id(inserted_id)
print(f"Retrieved by ID: {retrieved_by_id}")

# Update info field
updated_info = Info(field_name="Updated Field", item_type="number", field_description="Updated description")
update_result = info_update(inserted_id, updated_info)
print(f"Update Result: {update_result}")

# Delete info field by ID
delete_result = info_delete(iid=inserted_id)
print(f"Delete Result: {delete_result}")

# Create multiple info fields
info_list = [
    Info(field_name="Test Field 1", item_type="text", field_description="First test field"),
    Info(field_name="Test Field 2", item_type="number", field_description="Second test field")
]
inserted_ids = add_info_field(info_list)
print(f"Inserted IDs: {inserted_ids}")

# Retrieve info by multiple names
retrieved_info = info_by_name(["Test Field 1", "Test Field 2"])
print(f"Retrieved Info: {retrieved_info}")

# Retrieve info by multiple IDs
retrieved_by_ids = info_by_id(inserted_ids)
print(f"Retrieved by IDs: {retrieved_by_ids}")

# Update multiple info fields
updated_info_list = [
    Info(field_name="Updated Field 1", item_type="text", field_description="Updated first field"),
    Info(field_name="Updated Field 2", item_type="number", field_description="Updated second field")
]
update_results = [info_update(iid, updated_info) for iid, updated_info in zip(inserted_ids, updated_info_list)]
print(f"Update Results: {update_results}")

# Delete info fields by multiple IDs
delete_result = info_delete(iid=inserted_ids)
print(f"Delete Result: {delete_result}")


# QUESTION CRUD TESTS

print("===========================================\n COMMENCING QUESTION CRUD TESTS \n=========================================== ")

from archiver import (
    question_by_content, add_question, question_by_id, update_question, delete_questions, Question
)

# Test with a single question
question = Question(
    content="What is the capital of France?",
    images=[],
    options=["Paris", "London", "Berlin", "Madrid"],
    answer="Paris",
    subject="Geography",
    difficulty_rating=2
)
inserted_id = add_question(question)
print(f"Inserted ID: {inserted_id}")

# Retrieve question by content
retrieved_question = question_by_content("What is the capital of France?")
print(f"Retrieved Question: {retrieved_question}")

# Retrieve question by ID
retrieved_by_id = question_by_id(inserted_id)
print(f"Retrieved by ID: {retrieved_by_id}")

# Update question
updated_question = Question(
    content="What is the capital of Germany?",
    images=[],
    options=["Paris", "London", "Berlin", "Madrid"],
    answer="Berlin",
    subject="Geography",
    difficulty_rating=3
)
update_result = update_question(inserted_id, updated_question)
print(f"Update Result: {update_result}")

# Delete question by ID
delete_result = delete_questions(qid=inserted_id)
print(f"Delete Result: {delete_result}")

# Test with multiple questions
question_list = [
    Question(
        content="What is 2 + 2?",
        images=[],
        options=["3", "4", "5", "6"],
        answer="4",
        subject="Mathematics",
        difficulty_rating=1
    ),
    Question(
        content="Who wrote 'Hamlet'?",
        images=[],
        options=["Shakespeare", "Hemingway", "Twain", "Austen"],
        answer="Shakespeare",
        subject="Literature",
        difficulty_rating=3
    )
]
inserted_ids = add_question(question_list)
print(f"Inserted IDs: {inserted_ids}")

# Retrieve multiple questions by content
retrieved_questions = question_by_content(["What is 2 + 2?", "Who wrote 'Hamlet'?"])
print(f"Retrieved Questions: {retrieved_questions}")

# Retrieve multiple questions by IDs
retrieved_by_ids = question_by_id(inserted_ids)
print(f"Retrieved by IDs: {retrieved_by_ids}")

# Update multiple questions
updated_question_list = [
    Question(
        content="What is 3 + 3?",
        images=[],
        options=["5", "6", "7", "8"],
        answer="6",
        subject="Mathematics",
        difficulty_rating=2
    ),
    Question(
        content="Who wrote '1984'?",
        images=[],
        options=["Orwell", "Huxley", "Bradbury", "Kafka"],
        answer="Orwell",
        subject="Literature",
        difficulty_rating=4
    )
]
update_results = [update_question(qid, updated_question) for qid, updated_question in zip(inserted_ids, updated_question_list)]
print(f"Update Results: {update_results}")

# Delete multiple questions by IDs
delete_result = delete_questions(qid=inserted_ids)
print(f"Delete Result: {delete_result}")

print("===========================================\n COMMENCING TESTS CRUD TESTS \n=========================================== ")

import uuid
from datetime import datetime, timezone
from typing import List, Union
from pydantic import BaseModel, Field

def test_single_inputs():
    print("Testing functions with single inputs")
    
    single_test = Test(
        title="Math Test",
        client="School District A",
        subjects=[{"subjectid": "1", "subject": "Math", "subject_total": 100}],
        total_score=100,
        questions={"q1": 10, "q2": 20},
        negative_multiplier=0.5
    )
    
    test_id = create_test(single_test)
    print(f"Created Test ID: {test_id}")
    
    fetched_test = test_by_id(test_id)
    print(f"Fetched Test: {fetched_test}")
    
    fetched_by_name = test_by_name("Math Test")
    print(f"Fetched by Name: {fetched_by_name}")
    
    updated_test = Test(
        title="Updated Math Test",
        client="School District A",
        subjects=[{"subjectid": "1", "subject": "Math", "subject_total": 100}],
        total_score=100,
        questions={"q1": 10, "q2": 20},
        negative_multiplier=0.5
    )
    update_test(test_id, updated_test)
    print("Test updated")
    
    deleted_count = test_delete(tid=test_id)
    print(f"Deleted Test Count: {deleted_count}")

def test_list_inputs():
    print("Testing functions with list inputs")
    
    tests = [
        Test(title="Science Test", client="District B", subjects=[{"subjectid": "2", "subject": "Science", "subject_total": 90}], total_score=90, questions={"q3": 30, "q4": 15}, negative_multiplier=0.2),
        Test(title="History Test", client="District C", subjects=[{"subjectid": "3", "subject": "History", "subject_total": 80}], total_score=80, questions={"q5": 25, "q6": 10}, negative_multiplier=0.3)
    ]
    
    test_ids = [create_test(t) for t in tests]
    print(f"Created Test IDs: {test_ids}")
    
    fetched_tests = test_by_id(test_ids)
    print(f"Fetched Tests: {fetched_tests}")
    
    fetched_by_names = test_by_name(["Science Test", "History Test"])
    print(f"Fetched by Names: {fetched_by_names}")
    
    deleted_count = test_delete(tid=test_ids)
    print(f"Deleted Tests Count: {deleted_count}")

print("===========================================\n COMMENCING RESPONSE CRUD TESTS \n=========================================== ")

def test_response_single_inputs():
    print("Testing response functions with single inputs")
    
    single_response = Response(
        test_ID="test123",
        client="Client A",
        subject_scores=[{"subjectid": "1", "subject": "Math", "subject_score": 80}],
        info=[{"infoid": "info1", "response": "Some response"}],
        results={"q1": "A", "q2": "B"}
    )
    
    response_id = add_response(single_response)
    print(f"Created Response ID: {response_id}")
    
    fetched_response = get_responses(rid=response_id)
    print(f"Fetched Response: {fetched_response}")
    
    deleted_count = delete_responses(rid=response_id)
    print(f"Deleted Response Count: {deleted_count}")

def test_response_list_inputs():
    print("Testing response functions with list inputs")
    
    responses = [
        Response(test_ID="test123", client="Client B", subject_scores=[{"subjectid": "2", "subject": "Science", "subject_score": 75}], info=[{"infoid": "info2", "response": "Another response"}], results={"q3": "C", "q4": "D"}),
        Response(test_ID="test456", client="Client C", subject_scores=[{"subjectid": "3", "subject": "History", "subject_score": 85}], info=[{"infoid": "info3", "response": "Different response"}], results={"q5": "E", "q6": "F"})
    ]
    
    response_ids = [add_response(r) for r in responses]
    print(f"Created Response IDs: {response_ids}")
    
    fetched_responses = get_responses(rid=response_ids)
    print(f"Fetched Responses: {fetched_responses}")
    
    deleted_count = delete_responses(rid=response_ids)
    print(f"Deleted Responses Count: {deleted_count}")

if __name__ == "__main__":
    test_single_inputs()
    test_list_inputs()
    test_response_single_inputs()
    test_response_list_inputs()
