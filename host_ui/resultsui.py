import streamlit as st
import os

def create_searchable_container_list():
    
    containers_data = []
    
    parent_dir = os.getcwd().replace("\\alltests", "")

    #Retrieve data from the excel sheet filenames.
    qfiles = os.listdir(f"{parent_dir}/questionlists")
    tnames = [name.split("xlsx")[0] for name in qfiles]
    test_dat = []

    for tname in tnames:
        i=tname.split("-")
        i[2] = i[2].replace("_",".")
        i[3] = i[3].replace("_","/")
        test_dat.append({
            "title": i[0],
            "pop": i[1],
            "perc": i[2].replace("_","."),
            "date": i[3].replace("_","/"),
            "url": f"https://stu.globalknowledgetech.com:1918?test={tname}xlsx"
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