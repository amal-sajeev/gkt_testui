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
    st.write(st.session_state.test)

#Client input
clientbox, clientbutton = st.columns([0.9,0.1],vertical_alignment="bottom")
with clientbox:
    st.session_state.test.client = st.text_input("Client for this Examination:")
with clientbutton:
    st.button("Refresh")

#Title Input
st.session_state.test.title = st.text_input("Title for this Examination:")

#Select Subjects
subjects = st.multiselect("Select Subjects", archiver.get_test_options(get_subjects=True))
subpointarr = {}
for i in subjects:
    subpointarr[i] = st.number_input(f"Points for {i} questions")

#Select Questions based on selected subjects
all_q = archiver.search_questions(subjects=subjects)
select_q = []
selected, qdat = st.columns(2)
with qdat:
    for i in all_q:
        if st.button(i["content"], key = i["_id"]):
                st.session_state.test.questions[i["_id"]] = subpointarr[i["subject"]]
with selected:
    for i in select_q:
        st.write(i["content"])