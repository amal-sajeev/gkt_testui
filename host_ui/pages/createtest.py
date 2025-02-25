import streamlit as st
import base64
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

all_q = archiver.search_questions()

def update_points_on_point_change(subpointarr):
    sel_q = [i for i in all_q if i["_id"] in st.session_state.test.questions.keys()]
    if len(sel_q)>0:
        for i in sel_q:
            if i["subject"] in subpointarr.keys():
                st.session_state.test.questions[i["_id"]] = subpointarr[i["subject"]]
                for j in subjects:
                    st.session_state.test.subjects[j] = subpointarr[i["subject"]]*len([q for q in sel_q if q["subject"] == j])
        delarr = []
        for x in st.session_state.test.subjects.keys():
            if x not in subjects:
                delarr.append(x)
        for x in delarr:
            del st.session_state.test.subjects[x]
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

@st.dialog("Add a Question", width="large")
def add_question():
    new_q = Question()
    
    new_q.content = st.text_area("Enter the Question:", key="qcont",placeholder="You can surround words with **, **like this** for bold, and *, like *this* for italics.")
    
    images = st.file_uploader("Upload images **required** for the question",type=["png","jpg"],accept_multiple_files=True)
    for i in images:
        new_q.images.append( base64.b64encode(i.getvalue()).decode() )
    option_num = st.number_input("Enter the number of options for the question.", min_value=2, max_value=6,value=2)
    
    new_q.options = [i+1 for i in range(option_num)]
    for i in range(option_num):
        new_q.options[i] = st.text_input(f"Option {i+1}")
    
    new_q.answer = st.multiselect("Choose the answer(s) to the question.", new_q.options)

    new_q.subject = st.text_input("Subject that the question belongs to. Ensure it is spelled and punctuated correctly.")

    new_q.difficulty_rating = st.number_input("Difficulty rating for the question(Optional)", min_value = 1, max_value= 5)

    if st.button("Create Question","adddq"):
        qid = archiver.add_question(new_q)
        st.write(qid)
            # st.rerun()

#Select Questions based on selected subjects
select_q = {}
selected, qdat = st.columns(2)
with qdat:
    with st.container(key="selectdisplay", border = True, height = 450):
        for i in all_q:
            if i["subject"] in subjects:
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
    if st.button("Add a Question", key="addq", type="primary"):
        add_question()

st.session_state.test.subject_multipliers=subpointarr

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

st.warning("Please confirm the details before submitting. If you're sure, click the button below.")

if st.button("Create Test", use_container_width=True, key = "premptsubmit", type="primary"):
    tid=None
    try:
        tid = archiver.create_test(st.session_state.test)
    except Exception as e:
        st.toast(f"Failed to create test!\n\nError: {e}")
    if tid:
        st.toast(f"Created test successfully!\n\nTest ID: {tid}")