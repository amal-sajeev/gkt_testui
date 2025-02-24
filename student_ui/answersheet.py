import pandas as pd
import streamlit as st
import os
import sys
from streamlit_extras.stylable_container import stylable_container
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import archiver

rid = st.query_params["rid"]
response = archiver.get_responses(rid)
if type(response) == list:
    response = response[0]

#Read questions from question database
questions = archiver.question_by_id(response["results"].keys())

#Get test details from test database
test = archiver.test_by_id(response["test_ID"])[0]

#Read responses from response object
answers = response["results"]
candidateinfo = response["info"]

#Candidate Info Display, prioritize based on field status.
infodat = archiver.info_by_id(candidateinfo.keys())

importantinfo = {}
laterinfo = {}

for i in infodat:
    if i["priority"] == True:
        importantinfo[i["field_name"]] = candidateinfo[i["_id"]]
    else:
        laterinfo[i["field_name"]] = candidateinfo[i["_id"]]

st.title("Candidate Response")

# Create two columns - one for candidate info, one for scores
col1, col2 = st.columns([2, 1])

# Candidate info in left column
with col1:
    with st.container(key="Candidate info", border=True):
        for i in importantinfo.keys():
            st.subheader(f"{i} : {importantinfo[i]}")
        with st.expander("More details..."):
            for i in laterinfo.keys():
                st.write(f"{i} : {laterinfo[i]}")

# Scores in right column
with col2:
    # Calculate total score and percentage
    total_score = sum(response["subject_scores"].values())
    total_possible = test["total_score"]
    total_percentage = (total_score / total_possible) * 100
    total_color = "#88E788" if total_percentage >= 60 else "#E73121"
    
    # Create a container for scores with custom styling
    with st.container(key="Scores", border=True):
        # Use custom CSS to style the container
        st.markdown(
            """
            <style>
            [data-testid="stVerticalBlock"] > [style*="flex-direction: column;"] > [data-testid="stVerticalBlock"] {
                border: 1px solid #ddd;
                border-radius: 5px;
                padding: 10px;
                background-color: white;
                height: 100%;
            }
            </style>
            """,
            unsafe_allow_html=True
        )
        
        # Total score section
        st.markdown(
            f"""
            <div style='text-align: center; padding: 0px 0px;'>
                <p style='font-size: 24px; margin-bottom: 0px;'>Total Score</p>
                <span style='font-size: 48px; font-weight: bold; margin: 0px; color: {total_color};'>
                    {total_score}
                <span style='color: white; font-size: 35px;'> / {total_possible}</span>
                
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # Horizontal line separator
        st.markdown("<hr style='margin: 0px; padding: 0px;'>", unsafe_allow_html=True)
        
        # Individual subject scores
        st.markdown("<div style='padding: 0px 0px;'>", unsafe_allow_html=True)
        for subject, score in response["subject_scores"].items():
            # Calculate percentage for this subject
            possible_score = test["subjects"][subject]
            percentage = (score / possible_score) * 100
            subject_color = "#88E788" if percentage >= 60 else "#E73121"
            
            st.markdown(
                f"""
                <div style='display: flex; justify-content: space-between; padding: 1px 0px;'>
                    <span>{subject}</span>
                    <div>
                        <span style='font-weight: bold; color: {subject_color};'>{score}</span>
                        <span style='color: gray; font-size: 12px;'> /{possible_score}</span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
        st.markdown("</div>", unsafe_allow_html=True)

questdict = {i["_id"]:i for i in questions}

#Displaying all questions from a test, seperated by subject.
for subject, tab in zip(test["subjects"].keys(),st.tabs(test["subjects"].keys())):
    with tab:
        with st.container(key = subject):
            n=1
            for i in test["questions"].keys():
                if questdict[i]["subject"] == subject:
                    number,question = st.columns([7,93], vertical_alignment="center")
                    with number:
                        st.markdown(f"##### <div style='text-align: right'>[{n}]</div>", unsafe_allow_html=True)
                    with question:
                            with st.container(key = f"con{questdict[i]['_id']}", border = True):  
                                
                                st.write(questdict[i]['content'])

                                for j in questdict[i]["options"]:
                                    #Correct answer
                                    if str(j) == str(response["results"][i]):
                                        if str(j) == str(questdict[i]["answer"]):
                                            with stylable_container(
                                                key = f"qulo{questdict[i]['_id']}",
                                                css_styles = """
                                                {
                                                    border: 1px solid green
                                                }
                                                """,
                                            ):
                                                st.write(f":white_check_mark:    {j}")
                                    #Wrong Answer
                                        else:
                                            with stylable_container(
                                                key = f"corr{questdict[i]['_id']}",
                                                css_styles = """
                                                {
                                                    border: 1px solid red
                                                }
                                                """,
                                            ):
                                                st.write(f":x:    {j}")
                                    #No Answer
                                    else:
                                        if str(j) == str(questdict[i]["answer"]):
                                            st.write(f":white_check_mark:    {j}")
                                        else:
                                            st.write(f":radio_button:    {j}")
                    n += 1