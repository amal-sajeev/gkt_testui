import streamlit as st
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import archiver
from archiver import *
st.title("Create Test")

#Declare all values in session sate to preserve input states.
if "test" not in st.session_state:
    st.session_state.test = Test()

with st.sidebar:
    st.button("Refresh", help="If the changes in the form don't reflect on the data below, click this button!")
    st.write(st.session_state.test)

#Client input

st.session_state.test.client = st.text_input("Client for this Examination:")

#Title Input
st.session_state.test.title = st.text_input("Title for this Examination:")

#Select Subjects
subjects = st.multiselect("Select Subjects", archiver.get_test_options(get_subjects=True))
subpointarr = {}
select_q = []
all_q = archiver.search_questions(subjects=subjects)

def update_points_on_point_change(subpointarr):
    sel_q = [i for i in all_q if i["_id"] in st.session_state.test.questions.keys()]
    if len(sel_q)>0:
        for i in sel_q:
            if i["subject"] in subpointarr.keys():
                st.session_state.test.questions[i["_id"]] = subpointarr[i["subject"]]

if len(subjects)>0:
    #Select point values for each subject
    for sub, col in zip(subjects,st.columns(len(subjects))):
        with col:
            st.write(f"{sub} point value.")
            subpointarr[sub] = st.number_input(f"Enter value", value = 1, min_value=1, key = sub)
            update_points_on_point_change(subpointarr)



#To align the text in the question buttons to the left.
st.markdown("""
<style>
.stButton button {
    text-align: left;
    justify-content: flex-start;
}
</style>
""", unsafe_allow_html=True)

#Select Questions based on selected subjects

selected, qdat = st.columns(2)
with qdat:
    with st.container(key="selectdisplay", border = True, height = 450):
        for i in all_q:
            if st.button(i["content"], key = i["_id"], type = "tertiary"):
                    st.session_state.test.questions[i["_id"]] = subpointarr[i["subject"]]
                    st.rerun()
with selected:
    with st.container(key="questiondisplay", border = True, height = 450):
        sel_q = [i for i in all_q if i["_id"] in st.session_state.test.questions.keys()]
        for i in sel_q:
            if st.button(i["content"], key = "2"+i["_id"], type = "tertiary"):
                del st.session_state.test.questions[i["_id"]]
                st.rerun()

if len(st.session_state.test.questions)>0:
    st.session_state.test.total_score = sum([st.session_state.test.questions[i] for i in st.session_state.test.questions.keys()])
    totalscore, negmult = st.columns(2)
    #Total Score Custom scoreboard display
    with totalscore:
        # Create a container for scores with custom styling
        with st.container(key="totscore", border=True):
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
                    <span style='font-size: 48px; font-weight: bold; margin: 0px; color: white;'>
                        {st.session_state.test.total_score}
                    
                </div>
                """,
                unsafe_allow_html=True
            )
            st.markdown("</div>", unsafe_allow_html=True)

    with negmult:
        enablenegmult = st.checkbox("Enable Negative Multiplier?")
        if enablenegmult:
            st.session_state.test.negative_multiplier = round(st.number_input(f"Enter value", value = 0.00, min_value=0.00, step=0.01, key = negmult),2)

#To align the text in the submit buttons to the center.
st.markdown("""
<style>
.stButton button {
    text-align: left;
    justify-content: flex-start;
}
</style>
""", unsafe_allow_html=True)

if st.button("Create Test", use_container_width=True, key = "premptsubmit", type="primary"):
    st.error("Please confirm the details before submitting. If you're sure, click the button below.")
    if st.button("Yes, create the test."):
        archiver.create_test(st.session_state.test)