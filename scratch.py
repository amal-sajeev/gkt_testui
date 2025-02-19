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


print(newq)

# print(archiver.add_question(newq))

qind = [i["_id"] for i in archiver.find_by_content([i.content for i in newq])]
print(qind)
print(archiver.delete_questions(qind))
