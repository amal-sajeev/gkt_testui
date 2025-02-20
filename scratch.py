# import archiver

# print(archiver.find_by_content(["A monkey starts climbing up a tree 20ft. tall. Each hour, it hops 3ft. and slips back 2ft. How much time would it take the monkey to reach the top?","What number comes next in the following series? 56, 54, 40, 48, 44, …"]))


from archiver import *
import archiver

newq = [Question(
    content = "hahahehe",
    options = ["hehe","hoohoo","haha"],
    answer = "haha",
    subjectid = "hehe",
    subject_name = "hahaha",
    difficulty_rating = 2
),
Question(
    content = "hahaheho",
    options = ["hehe","hoohoo","haha"],
    answer = "haha",
    subjectid = "hehe",
    subject_name = "hahaha",
    difficulty_rating = 2
)
]

newq2 = Question(
    content = "HEHAHO",
    options = ["hehe","hoohoo","haha"],
    answer = "haha",
    subjectid = "hehe",
    subject_name = "hahaha",
    difficulty_rating = 2
)

# print(newq)

# print(archiver.add_question(newq))

# qind = [i["_id"] for i in archiver.find_by_content([i.content for i in newq])]
# print(qind)
# print(archiver.delete_questions(qind))

print(update_question("49087195-2a4d-4a9e-ae9f-bcf08f257ce9", newq2))

#ID CRUD TEST

newinf = [Info(
    field_name = "Visitor Status",
    item_type = "text",
    field_description = "Are you allowed to be a visitor?"
),
Info(
    field_name = "Visitor ID",
    item_type = "text",
    field_description = "Your visitor ID code."
)
]



# print(archiver.info_by_name("Email address"))
# print(archiver.add_info_field(newinf))