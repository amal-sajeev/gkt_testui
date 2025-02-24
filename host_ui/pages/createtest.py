import streamlit as st
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import archiver
from archiver import *
st.title("Create Test")

#Declare all values in session sate to preserve input states.
if client not in st.session_state:
    st.session_state.client = ""

st.subheader(f"Client: {st.session_state.client}")
st.session_state.client = st.client("Client for this Examination:")
