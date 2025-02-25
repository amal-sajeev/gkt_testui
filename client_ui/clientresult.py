import streamlit as st
import os
from typing import List
import pandas as pd
from pandas.api.types import (
    is_categorical_dtype,
    is_datetime64_any_dtype,
    is_numeric_dtype,
    is_object_dtype,
)
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import archiver
from archiver import *
from pprint import pprint

def filter_dataframe(df: pd.DataFrame, excluded_columns: List[str] = []) -> pd.DataFrame:
    """
    Adds a UI on top of a dataframe to let viewers filter columns

    Args:
        df (pd.DataFrame): Original dataframe
        excluded_columns (List[str]): Columns to exclude from filtering

    Returns:
        pd.DataFrame: Filtered dataframe
    """
    modify = st.checkbox("Add filters")

    if not modify:
        return df

    df = df.copy()

    # Try to convert datetimes into a standard format (datetime, no timezone)
    for col in df.columns:
        if is_object_dtype(df[col]):
            try:
                df[col] = pd.to_datetime(df[col], format='%Y_%m_%d')
            except Exception:
                pass

        if is_datetime64_any_dtype(df[col]):
            df[col] = df[col].dt.tz_localize(None)

    modification_container = st.container()

    with modification_container:
        to_filter_columns = st.multiselect("Filter dataframe on", [i for i in df.columns if i not in excluded_columns])
        for column in to_filter_columns:
            left, right = st.columns((1, 20))
            # Treat columns with < 10 unique values as categorical
            if isinstance(df[column], pd.CategoricalDtype):
                user_cat_input = right.multiselect(
                    f"Values for {column}",
                    df[column].unique(),
                    default=list(df[column].unique()),
                )
                df = df[df[column].isin(user_cat_input)]
            elif is_numeric_dtype(df[column]):
                _min = float(df[column].min())
                _max = float(df[column].max())
                step = (_max - _min) / 100
                user_num_input = right.slider(
                    f"Values for {column}",
                    min_value=_min,
                    max_value=_max,
                    value=(_min, _max),
                    step=step,
                )
                df = df[df[column].between(*user_num_input)]
            elif is_datetime64_any_dtype(df[column]):
                user_date_input = right.date_input(
                    f"Values for {column}",
                    value=(
                        df[column].min(),
                        df[column].max(),
                    ),
                )
                if len(user_date_input) == 2:
                    user_date_input = tuple(map(pd.to_datetime, user_date_input))
                    start_date, end_date = user_date_input
                    df = df.loc[df[column].between(start_date, end_date)]
            else:
                user_text_input = right.text_input(
                    f"Part or all of {column}",
                )
                if user_text_input:
                    df = df[df[column].astype(str).str.contains(user_text_input)]

    return df


def create_results_grid(testid: str = ""):
    """
    Create and display a results grid for any exam data file.
    Shows all candidate data columns up to scol, p4lus computed columns.
    
    Args:
        testid (str): The name of the Excel file to load
    """
    
    test= archiver.test_by_id(tid=testid)[0]
    responses = archiver.get_responses(tid=test["_id"])
    info_priorities = {i["_id"]:i["priority"] for i in archiver.info_by_id(test["infofields"].keys())}
    
    try:
        
        records = []
        
        
        for response in responses:
            pprint(response)
            record={}
            for i in test["infofields"].keys():
                if info_priorities[i] == True:
                    record[test["infofields"][i]]= response["info"][i]
            record["Completion"] = len(response["results"].keys())/len(test["questions"])
            record["Subject Distribution"] = []
            for i in response["subject_scores"].keys():
                record[i] = response["subject_scores"][i]
                record["Subject Distribution"].append(record[i])
            record["Score"] = sum(record["Subject Distribution"])
            record["UUID"] = f"https://stu.globalknowledgetech.com:9181/?rid={response["_id"]}"
            records.append(record)
        
        df = pd.DataFrame(records)

        column_config = {
            "UUID": st.column_config.LinkColumn("Answer Sheet", display_text="Answer Sheet"),
            "Answered": st.column_config.ProgressColumn(
                "Test Progress",
                help="Number of Questions answered",
                format="%d",
                min_value=0,
                max_value=qnum
            )
        }

        # Display the dataframe with all candidate columns
        st.dataframe(
            filter_dataframe(df),
            column_config=column_config,
            use_container_width=True
        )
        
    except Exception as e:
        st.error(f"Error processing file: {str(e)}")
        st.exception(e)


if __name__ == "__main__":
    st.set_page_config(page_title="Exam Results", layout="wide")
    
    if "test" in st.query_params:
        st.title("Exam Results")
        create_results_grid(st.query_params["test"])
    else:
        st.title("Exam Results Viewer")
        st.subheader("Please access with a specific test parameter")
        st.write("##### You need a valid test URL. Here's a friendly dog while you wait:")
        try:
            st.image("dog.png", caption="Please use a valid test URL!")
        except:
            st.write("I couldn't find the dog image, but please use a valid test URL!")