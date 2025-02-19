import pandas as pd
import streamlit as st
import os

from streamlit_extras.stylable_container import stylable_container

link = os.getcwd().replace("answersheets", "").replace("\\","/")

filename = st.query_params["data"]

#Read questions from excel sheet
qdf = pd.read_excel(f"{link}/questionlists/{filename}")
qdf = qdf.map(lambda x: x.rstrip("'") if isinstance(x, str) else x)

#Read response from excel sheet
adf = pd.read_excel(f"{link}/responselists/{filename}", index_col="UUID")
adf = adf.loc[st.query_params["uuid"]]
adf = adf.map(lambda x: x.rstrip("'") if isinstance(x, str) else x)

scol = int(filename.split(".")[0].split("-")[-2])

questions = []

st.subheader(adf["Name"])
with st.container(border = True):
    st.write(f"##### Score: {adf['Score']}")
    st.write(f"**Roll number**: {adf['Roll number']}")
    st.write(f"**E-mail**: {adf['Email address']}")
    st.write(f"**Phone Number**: {adf['Phone']}")

for i in range(len(qdf.iloc[:,0])):
    questions.append(
        {
            "_id" : i,
            "question_content" : qdf.loc[i, "Question_content"],
            "question_options": {
                "a":  qdf.loc[i, "a"],
                "b":  qdf.loc[i, "b"],
                "c":  qdf.loc[i, "c"],
                "d":  qdf.loc[i, "d"]
            },
            "response" : adf.iloc[scol-1+i],
            "answer" : qdf.loc[i, "Answers"]
        }
    )

with st.container(border = True):
    n=1
    for i in questions:
        
        number,question = st.columns([7,93], vertical_alignment="center")
        with number:
            st.markdown(f"##### <div style='text-align: right'>[{n}]</div>", unsafe_allow_html=True)
        with question:
                    
            with st.container(key = f"con{i['_id']}", border = True):  
                
                st.write(i['question_content'])

                for j in i["question_options"].values():
                    #Correct answer
                    if str(j) == str(i["response"]):
                        if str(j) == str(i["answer"]):
                            with stylable_container(
                                key = f"corr{i['_id']}",
                                css_styles = """
                                {
                                    border: 1px solid green
                                }
                                """,
                            ):
                                st.write(f":white_check_mark:    {j}")
                        else:
                            with stylable_container(
                                key = f"corr{i['_id']}",
                                css_styles = """
                                {
                                    border: 1px solid red
                                }
                                """,
                            ):
                                st.write(f":x:    {j}")
                    else:
                        if str(j) == str(i["answer"]):
                            st.write(f":white_check_mark:    {j}")
                        else:
                            st.write(f":radio_button:    {j}")
            n += 1