import pymongo as pym
from datetime import datetime, timezone
from pydantic import BaseModel, Field
import uuid
from typing import Union, List

mongoclient = pym.MongoClient("mongodb://datamaster:B8znzNgx2559BzWF1EJw@localhost:27017/")

db = mongoclient["examio"]


class Info(BaseModel):
    id : str = Field(default_factory=lambda: str(uuid.uuid4()), description = 'The ID of the Question', alias="_id")
    field_name: str = Field(description="The name of the info field.")
    item_type: str = Field(
        "text", description="The type of input this field should accept.")
    field_description: str = Field("", description = "The description shown for each info field.")


class Question(BaseModel):
    id : str = Field(default_factory=lambda: str(uuid.uuid4()), description = 'The ID of the Question', alias="_id")
    content: str = Field(
        description="The text content of the question. The images go in the question_images parameter.")
    images: List[str] = Field(
        [], description="The image content of the question. Accepts a list of Base64 strings of the images. Even if it's a single image, pass it in an array, it's simpler.")
    options: List = Field(
        [], description="The options for the question. Options can be images if you specify the type.  ")
    answer: str = Field(
        description="The correct answer to the question, should be exactly the same as the respective option.")
    subject_name: str = Field(
        description="The subject that the question belongs under. This is so that the data is readable during export.")
    difficulty_rating: int = Field(
        "1", description="The difficulty rating of the question for easier selection. Should be between 1 and 5")


class Test(BaseModel):

    id : str = Field(default_factory=lambda: str(uuid.uuid4()), description = 'The ID of the Test', alias="_id")
    title: str = Field("", description="The title of this test.")
    client: str = Field(
        "", description="The client for whom this test was made for.")
    subjects: List = Field(description="The subjects of the questions in this test. Each subject is a dictionary with the keys subjectid, subject_name, and subject_total, where subject_total is the total score of all the questions of the subject in the test.")
    publish_date: datetime = datetime.now(tz=timezone.utc)
    total_score: int = Field(0, description="The total score of the test.")
    submissions: int = Field(
        0, description="The number of submissions to the test")
    submittedid: List = Field(
        [], description="List with IDs of all the people who submitted responses.")
    questions: dict = Field(
        [], description="A list of questions in the test. Each question should be a dictionary with keys questionid and value, the value being the point value.")
    negative_multiplier: float = Field(
        0, description="Optional negative multiplier. If set to anything, the total points will be subtracted from if the question is wrong.")


class Response(BaseModel):
    id : str = Field(default_factory=lambda: str(uuid.uuid4()), description = 'The ID of the Test Response', alias="_id")
    test_ID: str = Field(
        description="The ID of the test this response was for.")
    submission_date: datetime = Field(datetime.now(
        tz=timezone.utc), description="The date time at which the response was submitted.")
    subject_scores: List = Field(
        [], description="The scores for each questions in each subject. Each entry in the list should be a dictionary with keys subjectid, subject_name, and subject_score")
    
    info: List = Field(
        [], description="The responses to info questions. The list should consist of dictionary objects with keys infoid and response.")
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

# def get_questions(subject: Union[str, List[str]] =None, difficulty_rating: Union[str])

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
       count = (db["questions"].delete_many({"subject_name": subject})).deleted_count
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

def create_test(test = Test):
    return((db["tests"].insert_one(test.model_dump(by_alias=True))).inserted_id)

def update_test(tid :str, new: Test):
    return(db["tests"].find_one_and_replace({"_id":tid},new.model_dump()))

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

