import pymongo as pym
from datetime import datetime, timezone
from pydantic import BaseModel, Field
import uuid
from typing import Union, List

mongoclient = pym.MongoClient("mongodb://datamaster:B8znzNgx2559BzWF1EJw@localhost:27017/")

db = mongoclient["examio"]


class Info(BaseModel):
    id : str = Field(str(uuid.uuid4()), description = 'The ID of the Question', alias="_id")
    field_name: str = Field(description="The name of the info field.")
    item_type: str = Field(
        "text", description="The type of input this field should accept.")


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
    subjectid: str = Field(
        description="The id of the subject that this question belongs to. Don't bother enterting this manually, this is just in place to make the code simpler.")
    subject_name: str = Field(
        description="The subject that the question belongs under. This is so that the data is readable during export.")
    difficulty_rating: int = Field(
        "1", description="The difficulty rating of the question for easier selection. Should be between 1 and 5")


class Test(BaseModel):

    id : str = Field(str(uuid.uuid4()), description = 'The ID of the Test', alias="_id")
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
    id : str = Field(str(uuid.uuid4()), description = 'The ID of the Test Response', alias="_id")
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
        question (Question, optional): One question to add. Defaults to None.
        question_list (List[Question], optional): List of questions to add. Defaults to None.
    """

    if type(question) == Question:
        
        if len(find_by_content(question))==0:
            id = db["questions"].insert_one(question.model_dump(by_alias=True))
            return(id.inserted_id)
        else:
            return("Question already present!")
    else:
        contentlist = [i.content for i in question]
        results = find_by_content(contentlist)
        
        if len(results)>0:
            for i in results:
                qfilter = ([question[j] for j in range(len(question)) if i["content"]==question[j].content])
                question.remove(qfilter[0])
        id=[]
        for i in question:
            t = db["questions"].insert_one(i.model_dump(by_alias=True))
            id.append(t.inserted_id)
        return(id)

def find_by_content(content: Union[str,List[str]]):
    """Find the ID of a question by the content of the question.

    Args:
        content (str): The content of the question.
    Returns:
        str: ID there is only one question with the content.
        List: List of IDs of questions that match the content.
    """
    contentlist = []
    contentlist.extend(content)
    results = db["questions"].find({"content":{"$in":contentlist}})

    return(list(results))


def update_question(qid: str, new : Question):
    """Updates a question based on ID.

    Args:
        qid (str): ID of the question to replace.
        new (Question): The new Question content
    """

    db["questions"].find_one_and_replace({"id": qid}, new.model_dump())
    return("Updated")

def delete_questions(qid: Union[str, List[str]] = None, content: str = None, subject: str = None):

    """Delete a question from the collection

    Args:
        qid (Union[str, List[str]]): Either a question id or a list of question ids to delete
    """
    temp = []
    if qid:
        if type(qid) == str:
            temp.append(qid)
        else:
            temp.extend(qid)

        return(db["questions"].delete_many({"_id":{"$in":temp}}))
    elif content:
        count = db["questions"].count_documents({"content":content})
        db["questions"].delete_many({"content":content})
        return(f"Deleted {count} {"question" if count==1 else "questions"}")
    elif subject:
        count = db["questions"].count_documents({"subject_name": subject})
        db["questions"].delete_many({"subject_name": subject})
