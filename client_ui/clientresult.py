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


def create_results_grid(filename: str = ""):
    """
    Create and display a results grid for any exam data file.
    Shows all candidate data columns up to scol, plus computed columns.
    
    Args:
        filename (str): The name of the Excel file to load
    """
    if not filename:
        st.error("No file specified!")
        return
        
    parent_dir = os.getcwd().replace("testresults", "").replace("\\","/")
    filepath = f"{parent_dir}/responselists/{filename}"
    
    try:
        # Load Excel file
        df = pd.read_excel(filepath)
        
        # Clean up Excel data
        for col in df.columns:
            if df[col].dtype == object:  # only clean string columns
                df[col] = df[col].apply(lambda x: x.rstrip("'") if isinstance(x, str) else x)
        
        # Parse filename to get test parameters
        parts = filename.split(".")[0].split("-")
        try:
            qnum = int(parts[-1])  # Number of questions
            scol = int(parts[-2])  # Starting column for answers
        except (IndexError, ValueError):
            st.warning("Filename format doesn't match expected pattern. Using default values.")
            # Find score column and estimate number of questions
            if "Score" in df.columns:
                qnum = int(df["Score"].max())
            else:
                qnum = 10  # default fallback
            scol = len(df.columns) // 2  # default fallback - assume answers are in second half
        
        # Ensure Score column exists or add it if needed
        score_col_name = None
        for col in df.columns:
            if "score" in str(col).lower():
                score_col_name = col
                break
        
        if score_col_name is not None:
            if score_col_name != "Score":
                df = df.rename(columns={score_col_name: "Score"})
            df["Score"] = pd.to_numeric(df["Score"], errors='coerce')
        else:
            st.warning("No Score column found in the data")
            
        # Calculate the number of answered questions for each candidate
        answeredcol = []
        for j in range(len(df)):
            candprog = 0
            # Get answer columns starting from scol
            for i in range(qnum):
                if scol + i - 1 < len(df.columns):
                    if pd.notna(df.iloc[j, scol + i - 1]) and str(df.iloc[j, scol + i - 1]) != "":
                        candprog += 1
            answeredcol.append(candprog)
            
        # Add Answered column near the beginning
        df.insert(2, "Answered", answeredcol)
        
        # Add Score Percent if Score exists
        if "Score" in df.columns:
            score_idx = df.columns.get_loc("Score")
            df.insert(score_idx + 1, "Score Percent", df["Score"])
        
        # Ensure UUID column exists
        if "UUID" not in df.columns:
            # Try to find a suitable ID column
            id_cols = [col for col in df.columns if 'id' in str(col).lower() or 'uuid' in str(col).lower()]
            if id_cols:
                df = df.rename(columns={id_cols[0]: "UUID"})
            else:
                # Create a UUID column at the end
                df["UUID"] = [f"candidate_{i}" for i in range(len(df))]
                
        # Ensure UUID contains the full URL
        df["UUID"] = df["UUID"].apply(lambda uuid: 
            f"https://stu.globalknowledgetech.com:9181/?uuid={uuid}" 
            if not str(uuid).startswith("http") else uuid)
        
        # Get all candidate data columns up to scol
        candidate_columns = list(df.columns[:scol-1])
        
        # Ensure our special columns are included
        display_columns = []
        if "Answered" in df.columns and "Answered" not in candidate_columns:
            display_columns.append("Answered")
        
        # Add all candidate columns
        display_columns.extend(candidate_columns)
        
        # Add Score and Score Percent if they exist but aren't already in candidate_columns
        if "Score" in df.columns and "Score" not in candidate_columns:
            display_columns.append("Score")
        if "Score Percent" in df.columns and "Score Percent" not in candidate_columns:
            display_columns.append("Score Percent")
        
        # Add UUID at the end if not already in candidate_columns
        if "UUID" in df.columns and "UUID" not in candidate_columns:
            display_columns.append("UUID")
        
        # Remove any duplicates while preserving order
        display_columns = list(dict.fromkeys(display_columns))
        
        # Configure special columns for display
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
        
        # Add Score Percent progress column if it exists
        if "Score Percent" in display_columns:
            column_config["Score Percent"] = st.column_config.ProgressColumn(
                "Score Percent",
                help="Total Score Percent",
                format="%f",
                min_value=0,
                max_value=qnum
            )
            
        # Exclude special columns from filtering
        excluded_from_filter = ["Score Percent", "UUID"]
        
        # Display the dataframe with all candidate columns
        st.dataframe(
            filter_dataframe(df[display_columns], excluded_columns=excluded_from_filter),
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