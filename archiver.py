import pymongo as pym
from datetime import datetime, timezone
from pydantic import BaseModel, Field
import uuid
from typing import Union, List, Optional, Any, Dict

mongoclient = pym.MongoClient("mongodb://datamaster:B8znzNgx2559BzWF1EJw@localhost:27017/")

db = mongoclient["examio"]


class Info(BaseModel):
    id : str = Field(default_factory=lambda: str(uuid.uuid4()), description = 'The ID of the Question', alias="_id")
    field_name: str = Field(description="The name of the info field.")
    item_type: str = Field(
        "text", description="The type of input this field should accept.")
    field_description: str = Field("", description = "The description shown for each info field.")
    priority: bool = Field(False, description = "Whether this info field should be shown in the results page.")


class Question(BaseModel):
    id : str = Field(default_factory=lambda: str(uuid.uuid4()), description = 'The ID of the Question', alias="_id")
    content: str = Field("",
        description="The text content of the question. The images go in the question_images parameter.")
    images: List[str] = Field(
        [], description="The image content of the question. Accepts a list of Base64 strings of the images. Even if it's a single image, pass it in an array, it's simpler.")
    options: List = Field(
        [], description="The options for the question. Options can only be text, if they need to be images, insert the options as one image with the other images.")
    answer: List[str] = Field([],
        description="The correct answers to the question, should be exactly the same values as the respective options.")
    subject: str = Field("",
        description="The subject that the question belongs under. This is so that the data is readable during export.")
    difficulty_rating: int = Field(
        "1", description="The difficulty rating of the question for easier selection. Should be between 1 and 5")


class Test(BaseModel):

    id : str = Field(default_factory=lambda: str(uuid.uuid4()), description = 'The ID of the Test', alias="_id")
    title: str = Field("", description="The title of this test.")
    client: str = Field(
        "", description="The client for whom this test was made for.")
    subjects:  Dict = Field(
        {}, description="The scores for each questions in each subject. Keys should be subjects, and value should be the total possible score of all the questions of the subject in the test.")
    publish_date: datetime = datetime.now(tz=timezone.utc)
    total_score: int = Field(0, description="The total score of the test.")
    submissions: int = Field(
        0, description="The number of submissions to the test")
    submittedid: Dict = Field(
        {}, description=" Keys are IDs of all the people who submitted responses, values will be their respective scores.")
    infofields: dict = Field({}, description = "A list of info fields that the candidate has to enter in the test. Should be a dictionary with key being info field ID and the value being the respective info field's field_name.")
    questions: dict = Field(
        {}, description="A list of questions in the test. Each question should be a dictionary with keys questionid and value, the value being the point value.")
    negative_multiplier: float = Field(
        0, description="Optional negative multiplier. If set to anything, the total points will be subtracted from if the question is wrong.")
    

class Response(BaseModel):
    id : str = Field(default_factory=lambda: str(uuid.uuid4()), description = 'The ID of the Test Response', alias="_id")
    test_ID: str = Field(
        description="The ID of the test this response was for.")
    submission_date: datetime = Field(datetime.now(
        tz=timezone.utc), description="The date time at which the response was submitted.")
    subject_scores: Dict = Field(
        {}, description="The scores for each questions in each subject. Keys should be subjects, and value should be subject_score")
    client: str = Field(description="The client that the responder is under.")
    info: Dict = Field(
        {}, description="The responses to info questions. The dictionary should consist of keys infoid and value info.")
    results: dict = Field(
        {}, description="The response to the test questions. This should be a dictionary with the keys questionids and the values being the option responded with.")


# CRUD for Question Banks
def add_question(question: Union[Question, List[Question]]):
    """Add a question to the questions collection. Pass either one question object or a list of question objects.

    Args:
        question (Question, List[Question]): Question or List of Question objects to add.
    """

    if type(question) == Question:
        
        if len(question_by_content(question.content))==0:
            id = db["questions"].insert_one(question.model_dump(by_alias=True))
            return(id.inserted_id)
        else:
            return("Question already present!")
    else:
        contentlist = [i.content for i in question]
        results = question_by_content(contentlist)
        
        if len(results)>0:
            exclude_content = {item["content"] for item in results}
            question = [q for q in question if q.content not in exclude_content]
        id = []
        for i in question:
            t = db["questions"].insert_one(i.model_dump(by_alias=True))
            id.append(t.inserted_id)
        return(id)

def question_by_content(content: Union[str,List[str]]):
    """Find the ID of a question by the content of the question.

    Args:
        content (str,List[str]]): The content of the question/questions.
    Returns:
        str: ID there is only one question with the content.
        List: List of IDs of questions that match the content.
    """
    contentlist = []
    if type(content)==str:
        contentlist.append(content)
    else:
        contentlist.extend(content)
    results = db["questions"].find({"content":{"$in":contentlist}})

    return(list(results))

def question_by_id(qid: Union[str,List[str]]):
    """Find the ID of a question by the content of the question.

    Args:
        qid (str,List[str]]): The id of the question or list of ids.
    Returns:
        List[Dict]: List of questions in dictionary format.
    """
    qidlist = []
    if type(qid)==str:
        qidlist.append(qid)
    else:
        qidlist.extend(qid)
    results = db["questions"].find({"_id":{"$in":qidlist}})

    return(list(results))

#Search for questions
def search_questions(subjects : Union[str, List[str]] = None, difficulty: Union[int, List[int]] = None):
    filterstring = {}
    if subjects != None:
        filterstring["subject"] = {"$in":[]}
        if type(subjects) == str:
            filterstring["subject"]["$in"].append(subjects)
        else:
            filterstring["subject"]["$in"].extend(subjects)
    if difficulty != None:
        filterstring["difficulty_rating"] = {"$in":[]}
        if type(difficulty) == str:
            filterstring["difficulty_rating"]["$in"].append(subjects)
        else:
            filterstring["difficulty_rating"]["$in"].extend(subjects)
    result = db["questions"].find(filterstring)
    return(list(result))

def update_question(qid: str, new : Question):
    """Updates a question based on ID.

    Args:
        qid (str): ID of the question to replace.
        new (Question): The new Question content

    Returns:
        Dictionary: The question prior to update.
        None : If the ID is invalid.
    """
    return(db["questions"].find_one_and_replace({"_id": qid}, new.model_dump()))

def delete_questions(qid: Union[str, List[str]] = None, content: str = None, subject: str = None):

    """Delete a question from the collection based on id, content, or subject

    Args:
        qid (Union[str, List[str]]): Either a question id or a list of question ids to delete
    """
    temp = []
    if qid:
        if type(qid) == str:
            temp.append(qid)
        else:
            temp.extend(qid)

        return((db["questions"].delete_many({"_id":{"$in":temp}})).deleted_count)
    elif content:
        count = (db["questions"].delete_many({"content":content})).deleted_count
        
        return(f"Deleted {count} {"question" if count==1 else "questions"}")
    elif subject:
       count = (db["questions"].delete_many({"subject": subject})).deleted_count
       return(f"Deleted {count} {"question" if count==1 else "questions"}")


#CRUD for info

def info_by_name(name: Union[str,List[str]]):
    """Find the ID of an info field by the title of the info field.

    Args:
        name (str): The content of the question.
    Returns:
        List: List of IDs of info fields that match the content.
    """
    namelist = []
    if type(name) == str:
        namelist.append(name)
    else:
        namelist.extend(name)
    results = db["info"].find({"field_name":{"$in":namelist}})

    return(list(results))

def add_info_field(info: Union[Info, List[Info]]):
    """Add an info field  to the info field collection. Pass either one info object or a list of info objects.

    Args:
        info (Info, List[Info]): Info Fields to add. Defaults to None.
    Returns:
        str: ID only one Info object is passed
        List: List of ID strings in multiple Info objects are passed.
    """

    if type(info) == Info:
        
        if len(info_by_name(info.field_name))==0:
            id = db["info"].insert_one(info.model_dump(by_alias=True))
            return(id.inserted_id)
        else:
            #"Info Field already present!"
            return(0)
    else:
        namelist = [i.field_name for i in info]
        results = info_by_name(namelist)
        
        if len(results)>0:
            excludefields = [i["field_name"] for i in results]
            info = [i for i in info if i.field_name not in excludefields]
            for i in results:
                temp = ([info[j] for j in range(len(info)) if i["field_name"]!=info[j].field_name])
                info=temp
        id=[]
        for i in info:
            t = db["info"].insert_one(i.model_dump(by_alias=True))
            id.append(t.inserted_id)
        return(id)

def info_by_id(iid: Union[str,List[str]]):
    """Find the ID of an info field by the name of the info field.

    Args:
        iid (str,List[str]]): The id of the info field or list of info fields.
    Returns:
        List: List of Info objects.
    """
    iidlist = []
    if type(iid)==str:
        iidlist.append(iid)
    else:
        iidlist.extend(iid)
    
    results = db["info"].find({"_id":{"$in":iidlist}})
    return(list(results))

def info_update(iid: str, new: Info):
    """Updates an info field by ID.

    Args:
        iid (str): ID of the info field to update.
    Returns:
        Dictionary: Old field
        None: If ID is invalid.
    """
    return(db["info"].find_one_and_replace({"_id": iid}, new.model_dump()))

def info_delete(iid:Union[str,List[str]] = None, field_name:Union[str, List[str]] = None):

    if iid:
        if type(iid)==str:
            return(db['info'].delete_one({"_id": iid}))
        else:
            return(db["info"].delete_many({"_id": {"$in":iid}}))
    else:
        if type(field_name) == str:
            return(db["info"].delete_many({"field_name": field_name}))
        else:
            return(db["info"].delete_many({"field_name": {"$in":field_name}}))

def get_priority(iid:Union[str,List[str]]=None):
    
    iidlist = []
    if type(iid)==str:
        iidlist.append(iid)
    else:
        iidlist.extend(iid)

    prioritydict = {}
    infolist = db["info"].find({"info":{"$in":iidlist}})
    for i in list(infolist):
        prioritydict[i["_id"]] = i["priority"]
    return(prioritydict)    

# CRUD for Tests

def test_by_name(name: Union[str,List[str]]):
    """Find tests of one name.

    Args:
        name (str): The title of the test.
    Returns:
        List: List of Test objects that match the name.
    """
    namelist = []
    if type(name) == str:
        namelist.append(name)
    else:
        namelist.extend(name)
    results = db["tests"].find({"title":{"$in":namelist}})
    return(list(results))

def test_by_id(tid:Union[str,List[str]]):

    tidlist = []
    if type(tid)==str:
        tidlist.append(tid)
    else:
        tidlist.extend(tid)
    return(list(db["tests"].find({"_id":{"$in":tidlist}})))

#Search for tests
def search_tests(
    subjects: Optional[Union[str, List[str]]] = None,
    client: Optional[Union[str, List[str]]] = None,
    title: Optional[str] = None,
    start_date: Optional[Union[str, datetime]] = None,
    end_date: Optional[Union[str, datetime]] = None
) -> List[Dict[str, Any]]:
    """
    Search tests in the exam database based on optional parameters.
    
    Args:
        subjects: Subject ID(s) to filter by. Can be a single string or list of strings.
        client: Client name(s) to filter by. Can be a single string or list of strings.
        title: Test title to filter by (partial match)
        start_date: Start date for publish_date range (inclusive)
                   Can be string in format 'YYYY-MM-DD' or datetime object
        end_date: End date for publish_date range (inclusive)
                 Can be string in format 'YYYY-MM-DD' or datetime object
    
    Returns:
        List of test documents matching the criteria
    """
    # Connect to MongoDB
    collection = db["tests"]
    
    # Build the query
    query = {}
    
    # Add subject filter if provided
    if subjects:
        # Convert single string to list if needed
        if isinstance(subjects, str):
            subjects = [subjects]
        # Filter tests that have any of the specified subject IDs
        query["subjects.subjectId"] = {"$in": subjects}
    
    # Add client filter if provided
    if client:
        # Convert single string to list if needed
        if isinstance(client, str):
            client = [client]
        # If only one client, use exact match
        if len(client) == 1:
            query["client"] = client[0]
        # If multiple clients, use $in operator
        else:
            query["client"] = {"$in": client}
    
    # Add title filter if provided (using regex for partial match)
    if title:
        query["title"] = {"$regex": title, "$options": "i"}  # case-insensitive
    
    # Add date range filter if provided
    if start_date or end_date:
        date_query = {}
        
        # Convert string dates to datetime if needed
        if start_date and isinstance(start_date, str):
            start_date = datetime.fromisoformat(start_date)
        if end_date and isinstance(end_date, str):
            end_date = datetime.fromisoformat(end_date)
        
        # Add start_date to query
        if start_date:
            date_query["$gte"] = start_date
        
        # Add end_date to query
        if end_date:
            date_query["$lte"] = end_date
        
        # Add date query to main query
        if date_query:
            query["publish_date"] = date_query
    
    # Execute the query and return results
    results = list(collection.find(query))
    return results

from pymongo import MongoClient
from typing import List, Dict, Union, Optional, Any

def get_test_options(get_clients:bool = False, get_subjects: bool = False
) -> Dict[str, List[Union[str, Dict[str, str]]]]:
    """
    Retrieves lists of unique clients or subjects from the tests collection.
    
    Args:
        get_clients: If True, retrieves a list of unique client names
        get_subjects: If True, retrieves a list of unique subject objects
    
    Returns:
        Either a list of clients or a list of subjects
    """
    collection = db["tests"]
    
    # Retrieve unique clients if requested
    if get_clients:
        # Use distinct to get unique client names
        clients = collection.distinct("client")
        return( sorted(clients) ) # Sort alphabetically
    
    # Retrieve unique subjects if requested
    if get_subjects:
        
        subjects = set()

        cursor = collection.find()
        for i in cursor:
            subjects.update(i["subjects"].keys())
        
        return(subjects)

def create_test(test = Test):
    return((db["tests"].insert_one(test.model_dump(by_alias=True))).inserted_id)

def update_test(tid :str, new: Test):
    return(db["tests"].find_one_and_replace({"_id":tid},new.model_dump()))

def add_submission(testid: int, responseid: str, score:float):
    test = test_by_id(tid)
    test["submissionsid"][responseid] = score
    test["submissions"] += 1
    return(update_test(tid,test))

def test_delete(tid:Union[str,List[str]] = None, title:Union[str, List[str]] = None, client:Union[str, List[str]] = None):

    if tid:
        if type(tid)==str:
            return(db['tests'].delete_one({"_id": tid}).deleted_count)
        else:
            return(db["tests"].delete_many({"_id": {"$in":tid}}).deleted_count)
    elif title:
        if type(tid)==str:
            return(db['tests'].delete_one({"_id": iid}).deleted_count)
        else:
            return(db["tests"].delete_many({"_id": {"$in":iid}}).deleted_count)
    else:
        if type(field_name) == str:
            return(db["info"].delete_many({"field_name": field_name}).deleted_count)
        else:
            return(db["info"].delete_many({"field_name": {"$in":field_name}}).deleted_count)

import pandas as pd

def convert_responses_to_dataframe(test_data: Dict):
    """
    Convert a single MongoDB document into a structured DataFrame.
    
    Args:
        test_data (Dict): A single document from MongoDB collection
        
    Returns:
        pd.DataFrame: Structured DataFrame with assessment data
    """
    # Initialize list to store data for DataFrame
    records = []
    
    # Extract all question IDs from the document to batch the lookup
    all_question_ids = []
    if "questions" in test_data and isinstance(test_data["questions"], dict):
        all_question_ids = list(test_data["questions"].keys())
    
    # Batch fetch all question details in a single call
    questions_details = {}
    if all_question_ids:
        fetched_questions = question_by_id(all_question_ids)
        questions_details = {q["_id"]: q for q in fetched_questions}
    
    # Get document metadata
    client_id = test_data.get("client", "")
    assessment_id = test_data.get("_id", "")
    title = test_data.get("title", "")
    total_score = test_data.get("total_score", 0)
    publish_date = test_data.get("publish_date", "")
    
    # Get submission details
    submissions = test_data.get("submissions", 0)
    submitted_ids = []
    submitted_scores = []
    
    if isinstance(test_data.get("submittedid"), dict):
        for sub_id, score in test_data["submittedid"].items():
            submitted_ids.append(sub_id)
            submitted_scores.append(score)
    
    # Process each question in the document
    if isinstance(test_data.get("questions"), dict):
        for q_id, q_score in test_data["questions"].items():
            q_details = questions_details.get(q_id, {})
            q_text = q_details.get("text", "")
            q_options = q_details.get("options", [])
            q_correct_answer = q_details.get("correct_answer", "")
            
            record = {
                "assessment_id": assessment_id,
                "title": title,
                "client_id": client_id,
                "publish_date": publish_date,
                "total_score": total_score,
                "submissions": submissions,
                "question_id": q_id,
                "question_text": q_text,
                "question_options": q_options,
                "question_correct_answer": q_correct_answer,
                "question_score": q_score,
                "submitted_ids": submitted_ids,
                "submitted_scores": submitted_scores,
                "negative_multiplier": test_data.get("negative_multiplier", 0)
            }
            records.append(record)
    
    # Create DataFrame from records
    df = pd.DataFrame(records)
    return df

#CRUD for Responses

def get_responses(rid: Union[str,List[str]] = None, tid: Union[str,List[str]] = None ):

    if rid:
        ridlist = []
        if type(rid)==str:
            ridlist.append(rid)
        else:
            ridlist.extend(rid)

        return(list(db["responses"].find({"_id":{"$in":ridlist}})))
    
    if tid:
        tidlist = []
        if type(tid)==str:
            tidlist.append(tid)
        else:
            tidlist.extend(tid)

        return(list(db["responses"].find({"test_ID":{"$in":tidlist}})))

#Search for questions
def search_responses(
    client: Optional[str] = None,
    start_date: Optional[Union[str, datetime]] = None,
    end_date: Optional[Union[str, datetime]] = None
) -> List[Dict[str, Any]]:
    """
    Search responses in the exam database based on optional parameters.
    
    Args:
        client: Client name to filter by
        test_id: Test ID to filter by
        start_date: Start date for submission_date range (inclusive)
                   Can be string in format 'YYYY-MM-DD' or datetime object
        end_date: End date for submission_date range (inclusive)
                 Can be string in format 'YYYY-MM-DD' or datetime object
    
    Returns:
        List of response documents matching the criteria.
    """
    # Connect to MongoDB
    collection = db["responses"]
    query = {}
    
    # Add client filter if provided
    if client:
        query["client"] = client
    # Add testid filter if provided
    if test_id:
        query["test_ID"] = test_id
    
    # Add date range filter if provided
    if start_date or end_date:
        date_query = {}
        
        # Convert string dates to datetime if needed
        if start_date and isinstance(start_date, str):
            start_date = datetime.fromisoformat(start_date)
        if end_date and isinstance(end_date, str):
            end_date = datetime.fromisoformat(end_date)
        # Add start_date to query
        if start_date:
            date_query["$gte"] = start_date
        # Add end_date to query
        if end_date:
            date_query["$lte"] = end_date
        # Add date query to main query
        if date_query:
            query["submission_date"] = date_query
    
    # Execute the query and return results
    results = list(collection.find(query))    
    return results

def add_response(response:Response):
    return((db["responses"].insert_one(response.model_dump(by_alias=True))).inserted_id)

def delete_responses(rid: Union[str,List[str]] = None, tid: Union[str,List[str]] = None ):

    if rid:
        ridlist = []
        if type(rid)==str:
            ridlist.append(rid)
        else:
            ridlist.extend(rid)

        return(db["responses"].delete_many({"_id":{"$in":ridlist}}).deleted_count)

    if tid:
        tidlist = []
        if type(tid)==str:
            ridlist.append(tid)
        else:
            ridlist.extend(tid)

        return(db["responses"].delete_many({"test_ID":{"$in":tidlist}}).deleted_count)