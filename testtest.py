from datetime import datetime, timezone
from typing import Dict, List
import uuid
from archiver import *
import archiver

from datetime import datetime, timezone
from typing import Dict, List
import uuid

# Info Fields remain the same as they were appropriate
info_fields = [
    Info(
        
        field_name="Full Name",
        item_type="text",
        field_description="Enter your full name as it appears on official documents",
        priority=True
    ),
    Info(
        
        field_name="Employee ID",
        item_type="text",
        field_description="Enter your company employee ID",
        priority=True
    ),
    Info(
        
        field_name="Department",
        item_type="text",
        field_description="Enter your current department",
        priority=False
    ),
    Info(
        
        field_name="Years of Experience",
        item_type="text",
        field_description="Enter your total years of professional experience",
        priority=False
    ),
    Info(
        
        field_name="Contact Email",
        item_type="text",
        field_description="Enter your work email address",
        priority=True
    )
]

# Expanded question set with multiple questions per subject
questions = [
    # Software Design Questions
    Question(
        id="sd1",
        content="What is the primary purpose of dependency injection?",
        images=[],
        options=[
            "To reduce code coupling",
            "To increase application speed",
            "To minimize memory usage",
            "To enhance UI design"
        ],
        answer="To reduce code coupling",
        subject="Software Design",
        difficulty_rating=3
    ),
    Question(
        id="sd2",
        content="Which SOLID principle deals with class inheritance?",
        images=[],
        options=[
            "Single Responsibility",
            "Liskov Substitution",
            "Interface Segregation",
            "Dependency Inversion"
        ],
        answer="Liskov Substitution",
        subject="Software Design",
        difficulty_rating=4
    ),
    Question(
        id="sd3",
        content="What pattern is best for implementing undo functionality?",
        images=[],
        options=[
            "Observer Pattern",
            "Command Pattern",
            "Factory Pattern",
            "Singleton Pattern"
        ],
        answer="Command Pattern",
        subject="Software Design",
        difficulty_rating=3
    ),
    
    # Data Structures Questions
    Question(
        id="ds1",
        content="Which data structure would be most efficient for implementing a cache?",
        images=[],
        options=[
            "Linked List",
            "Hash Table",
            "Binary Tree",
            "Stack"
        ],
        answer="Hash Table",
        subject="Data Structures",
        difficulty_rating=4
    ),
    Question(
        id="ds2",
        content="What is the space complexity of a balanced binary search tree?",
        images=[],
        options=[
            "O(1)",
            "O(n)",
            "O(log n)",
            "O(n log n)"
        ],
        answer="O(n)",
        subject="Data Structures",
        difficulty_rating=3
    ),
    Question(
        id="ds3",
        content="Which data structure is best for implementing a priority queue?",
        images=[],
        options=[
            "Array",
            "Linked List",
            "Heap",
            "Stack"
        ],
        answer="Heap",
        subject="Data Structures",
        difficulty_rating=4
    ),
    
    # Algorithms Questions
    Question(
        id="alg1",
        content="What is the time complexity of quicksort in the average case?",
        images=[],
        options=[
            "O(n)",
            "O(n log n)",
            "O(n²)",
            "O(log n)"
        ],
        answer="O(n log n)",
        subject="Algorithms",
        difficulty_rating=4
    ),
    Question(
        id="alg2",
        content="Which algorithm is most efficient for finding the shortest path in an unweighted graph?",
        images=[],
        options=[
            "Depth-First Search",
            "Breadth-First Search",
            "Dijkstra's Algorithm",
            "A* Search"
        ],
        answer="Breadth-First Search",
        subject="Algorithms",
        difficulty_rating=3
    ),
    Question(
        id="alg3",
        content="What is the best algorithm for finding the minimum spanning tree?",
        images=[],
        options=[
            "Quicksort",
            "Kruskal's Algorithm",
            "Binary Search",
            "Insertion Sort"
        ],
        answer="Kruskal's Algorithm",
        subject="Algorithms",
        difficulty_rating=4
    ),
    
    # Database Questions
    Question(
        id="db1",
        content="Which SQL join type returns all records from both tables?",
        images=[],
        options=[
            "INNER JOIN",
            "LEFT JOIN",
            "RIGHT JOIN",
            "FULL OUTER JOIN"
        ],
        answer="FULL OUTER JOIN",
        subject="Databases",
        difficulty_rating=2
    ),
    Question(
        id="db2",
        content="What is the purpose of database normalization?",
        images=[],
        options=[
            "Increase data redundancy",
            "Reduce data integrity",
            "Eliminate data redundancy",
            "Slow down queries"
        ],
        answer="Eliminate data redundancy",
        subject="Databases",
        difficulty_rating=3
    ),
    Question(
        id="db3",
        content="Which index type is best for exact match queries?",
        images=[],
        options=[
            "B-tree",
            "Hash",
            "Bitmap",
            "GiST"
        ],
        answer="Hash",
        subject="Databases",
        difficulty_rating=4
    ),
    
    # DevOps Questions
    Question(
        id="devops1",
        content="What is the main benefit of using containers in deployment?",
        images=[],
        options=[
            "Application isolation",
            "Faster code execution",
            "Better UI rendering",
            "Improved database performance"
        ],
        answer="Application isolation",
        subject="DevOps",
        difficulty_rating=3
    ),
    Question(
        id="devops2",
        content="Which tool is best for container orchestration?",
        images=[],
        options=[
            "Docker",
            "Kubernetes",
            "Git",
            "Maven"
        ],
        answer="Kubernetes",
        subject="DevOps",
        difficulty_rating=4
    ),
    Question(
        id="devops3",
        content="What is the purpose of blue-green deployment?",
        images=[],
        options=[
            "Visual design",
            "Zero-downtime deployment",
            "Code testing",
            "Database backup"
        ],
        answer="Zero-downtime deployment",
        subject="DevOps",
        difficulty_rating=3
    )
]

# Tests with multiple questions per subject
tests = [
    Test(
        id="test1",
        title="Software Engineering Assessment - Junior Level",
        client="TechCorp",
        subjects={
            "Software Design": 30,
            "Data Structures": 30,
            "Algorithms": 40
        },
        total_score=100,
        submissions=3,
        submittedid={
            "user1": 75,
            "user2": 85,
            "user3": 68
        },
        infofields={
            info_fields[0].id: "Full Name",
            info_fields[1].id: "Employee ID",
            info_fields[4].id: "Contact Email"
        },
        questions={
            questions[0].id: 15, questions[1].id: 15,
            questions[3].id: 15, questions[4].id: 15,
            questions[6].id: 20, questions[7].id: 20
        },
        negative_multiplier=0.25
    ),
    Test(
        id="test2",
        title="Backend Developer Evaluation",
        client="DataSys",
        subjects={
            "Databases": 40,
            "DevOps": 30,
            "Software Design": 30
        },
        total_score=100,
        submissions=2,
        submittedid={
            "user4": 85,
            "user5": 92
        },
        infofields={
            info_fields[0].id: "Full Name",
            info_fields[2].id: "Department",
            info_fields[3].id: "Years of Experience"
        },
        questions={
            questions[9].id: 20, questions[10].id: 20,
            "devops1": 15, "devops2": 15,
            questions[0].id: 15, questions[1].id: 15
        },
        negative_multiplier=0
    ),
    Test(
        id="test3",
        title="Full Stack Developer Assessment",
        client="WebTech",
        subjects={
            "Software Design": 25,
            "Databases": 25,
            "DevOps": 25,
            "Algorithms": 25
        },
        total_score=100,
        submissions=2,
        submittedid={
            "user6": 76,
            "user7": 88
        },
        infofields={
            info_fields[0].id: "Full Name",
            info_fields[1].id: "Employee ID",
            info_fields[2].id: "Department",
            info_fields[3].id: "Years of Experience",
            info_fields[4].id: "Contact Email"
        },
        questions={
            questions[0].id: 12.5, questions[1].id: 12.5,
            questions[9].id: 12.5, questions[10].id: 12.5,
            "devops1": 12.5, "devops2": 12.5,
            questions[6].id: 12.5, questions[7].id: 12.5
        },
        negative_multiplier=0.1
    ),
    Test(
        id="test4",
        title="Algorithm Specialist Evaluation",
        client="AlgoTech",
        subjects={
            "Algorithms": 60,
            "Data Structures": 40
        },
        total_score=100,
        submissions=2,
        submittedid={
            "user8": 95,
            "user9": 82
        },
        infofields={
            info_fields[0].id: "Full Name",
            info_fields[3].id: "Years of Experience",
            info_fields[4].id: "Contact Email"
        },
        questions={
            questions[6].id: 20, questions[7].id: 20, questions[8].id: 20,
            questions[3].id: 20, questions[4].id: 20
        },
        negative_multiplier=0.2
    ),
    Test(
        id="test5",
        title="DevOps Engineer Assessment",
        client="CloudSys",
        subjects={
            "DevOps": 60,
            "Databases": 40
        },
        total_score=100,
        submissions=2,
        submittedid={
            "user10": 89,
            "user11": 94
        },
        infofields={
            info_fields[0].id: "Full Name",
            info_fields[1].id: "Employee ID",
            info_fields[2].id: "Department"
        },
        questions={
            "devops1": 20, "devops2": 20, "devops3": 20,
            questions[9].id: 20, questions[10].id: 20
        },
        negative_multiplier=0
    )
]

# Responses with multiple questions answered per subject
responses = [
    Response(
        id="resp1",
        test_ID=tests[0].id,
        client="TechCorp",
        subject_scores={
            "Software Design": 25,
            "Data Structures": 30,
            "Algorithms": 20
        },
        info={
            info_fields[0].id: "John Doe",
            info_fields[1].id: "TC001",
            info_fields[4].id: "john.doe@techcorp.com"
        },
        results={
            questions[0].id: "To reduce code coupling",
            questions[1].id: "Liskov Substitution",
            questions[3].id: "Hash Table",
            questions[4].id: "O(n)",
            questions[6].id: "O(n log n)",
            questions[7].id: "Depth-First Search"
        }
    ),
    Response(
        id="resp2",
        test_ID=tests[1].id,
        client="DataSys",
        subject_scores={
            "Databases": 35,
            "DevOps": 30,
            "Software Design": 20
        },
        info={
            info_fields[0].id: "Jane Smith",
            info_fields[2].id: "Backend Development",
            info_fields[3].id: "5"
        },
        results={
            questions[9].id: "FULL OUTER JOIN",
            questions[10].id: "Eliminate data redundancy",
            "devops1": "Application isolation",
            "devops2": "Kubernetes",
            questions[0].id: "To reduce code coupling",
            questions[1].id: "Interface Segregation"
        }
    ),
    Response(
        id="resp3",
        test_ID=tests[2].id,
        client="WebTech",
        subject_scores={
            "Software Design": 25,
            "Databases": 25,
            "DevOps": 12.5,
            "Algorithms": 25
        },
        info={
            info_fields[0].id: "Mike Johnson",
            info_fields[1].id: "WT123",
            info_fields[2].id: "Full Stack",
            info_fields[3].id: "3",
            info_fields[4].id: "mike.j@webtech.com"
        },
        results={
            questions[0].id: "To reduce code coupling",
            questions[1].id: "Liskov Substitution",
            questions[9].id: "FULL OUTER JOIN",
            questions[10].id: "Eliminate data redundancy",
            "devops1": "Application isolation",
            "devops2": "Docker",
            questions[6].id: "O(n log n)",
            questions[7].id: "Breadth-First Search"
        }
    ),
    Response(
        id="resp4",
        test_ID=tests[3].id,
        client="AlgoTech",
        subject_scores={
            "Algorithms": 60,
            "Data Structures": 35
        },
        info={
            info_fields[0].id: "Sarah Wilson",
            info_fields[3].id: "7",
            info_fields[4].id: "sarah.w@algotech.com"
        },
        results={
            questions[6].id: "O(n log n)",
            questions[7].id: "Breadth-First Search",
            questions[8].id: "Kruskal's Algorithm",
            questions[3].id: "Hash Table",
            questions[4].id: "O(n)"
        }
    ),
    Response(
        id="resp5",
        test_ID=tests[4].id,
        client="CloudSys",
        subject_scores={
            "DevOps": 60,
            "Databases": 40
        },
        info={
            info_fields[0].id: "Alex Brown",
            info_fields[1].id: "CS456",
            info_fields[2].id: "Cloud Infrastructure"
        },
        results={
            "devops1": "Application isolation",
            "devops2": "Kubernetes",
            "devops3": "Zero-downtime deployment",
            questions[9].id: "FULL OUTER JOIN",
            questions[10].id: "Eliminate data redundancy"
        }
    )
]

print(archiver.add_info_field(info_fields))
print(archiver.add_question(questions))
for i in tests:
    print(archiver.create_test(i))
for i in responses:
    print(archiver.add_response(i))