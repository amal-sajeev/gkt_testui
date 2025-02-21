import streamlit as st
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import archiver
from archiver import *

def create_searchable_container_list():
    
    containers_data = []
    
    #Retrieve data from the excel sheet filenames.
    tests = archiver.search_tests()
    test_dat = []

    for test in tests:
        test_dat.append({
            "id": test["_id"],
            "title": test["title"],
            "pop": test["submissions"],
            "perc": round((len([i for i in test["submittedid"].values() if int(i)>(test["total_score"]*0.6)])/test["submissions"])*100,2) if test["submissions"]>0 else "NO SUBMISSIONS YET",
            "date": test["publish_date"].replace(tzinfo=timezone.utc).astimezone(tz=None).strftime("%m/%d/%Y, %H:%M:%S"),
            "url": f"https://stu.globalknowledgetech.com:1918?test={test["title"]}xlsx"
        })

    # Page title
    st.title("Test Hub")

    # Search bar
    search_term = st.text_input("Search", "")

    # Filter containers based on search term
    filtered_containers = [
        container for container in test_dat
        if search_term.lower() in container["title"].lower() or search_term.lower() in container["date"].lower()
    ]

    # Custom CSS for vertical centering
    st.markdown("""
        <style>
        .vertical-center {
            display: flex;
            align-items: center;
            height: 150px;
        }
        </style>
    """, unsafe_allow_html=True)

    # Display filtered containers
    for container in filtered_containers:
        with st.container():
            # Using custom HTML/CSS for layout
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown(f"### {container['title']}")
                st.markdown(f"##### Number of responders: {container['pop']}")
                st.markdown(f"##### Pass percent: {container['perc']}")
                st.markdown(f"##### Date: {container["date"]}")
            
            with col2:
                # Wrap the button in a vertically centered div
                st.markdown(f"""
                    <div class="vertical-center">
                        <a href="{container['url']}" target="_blank" 
                           style="display: inline-block; padding: 0.5rem 1rem; 
                                  background-color: #0066cc; color: white; 
                                  text-decoration: none; border-radius: 4px; 
                                  text-align: center; width: 100%;">
                            View Results
                        </a>
                    </div>
                """, unsafe_allow_html=True)
            # Add a separator between containers
            st.divider()

if __name__ == "__main__":
    st.set_page_config(page_title="List of tests", layout="wide")
    create_searchable_container_list()