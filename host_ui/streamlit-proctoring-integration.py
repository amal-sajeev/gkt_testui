import streamlit as st
import json
from streamlit.components.v1 import html
import time

def inject_proctoring_js():
    """Inject JavaScript code for proctoring features"""
    return """
    <script>
        // Function to send messages to parent frame
        function sendToParent(type, data) {
            window.parent.postMessage({
                type: type,
                data: data,
                source: 'streamlit'
            }, '*');
        }

        // Monitor keyboard events
        document.addEventListener('keydown', function(e) {
            if ((e.ctrlKey || e.metaKey) && ['c', 'v', 'x'].includes(e.key)) {
                sendToParent('security_violation', {
                    action: 'keyboard_shortcut',
                    key: e.key
                });
                e.preventDefault();
            }
        });

        // Monitor copy/paste events
        document.addEventListener('copy', function(e) {
            sendToParent('security_violation', {
                action: 'copy_attempt'
            });
            e.preventDefault();
        });

        document.addEventListener('paste', function(e) {
            sendToParent('security_violation', {
                action: 'paste_attempt'
            });
            e.preventDefault();
        });

        // Monitor mouse events for activity tracking
        let lastActivity = Date.now();
        document.addEventListener('mousemove', function() {
            const now = Date.now();
            if (now - lastActivity > 5000) {  // Send update every 5 seconds
                sendToParent('user_activity', {
                    type: 'mouse_movement',
                    timestamp: now
                });
                lastActivity = now;
            }
        });

        // Send periodic heartbeat
        setInterval(function() {
            sendToParent('heartbeat', {
                timestamp: Date.now()
            });
        }, 5000);

        // Monitor tab visibility
        document.addEventListener('visibilitychange', function() {
            sendToParent('visibility_change', {
                isVisible: !document.hidden
            });
        });

        // Block right clicks
        document.addEventListener('contextmenu', function(e) {
            sendToParent('security_violation', {
                action: 'right_click_attempt'
            });
            e.preventDefault();
        });

        // Monitor window focus
        window.addEventListener('blur', function() {
            sendToParent('focus_change', {
                hasFocus: false
            });
        });

        window.addEventListener('focus', function() {
            sendToParent('focus_change', {
                hasFocus: true
            });
        });
    </script>
    """

def create_exam_app():
    st.set_page_config(
        page_title="Secure Exam Environment",
        page_icon="📝",
        layout="wide"
    )

    # Inject proctoring JavaScript
    st.markdown(inject_proctoring_js(), unsafe_allow_html=True)

    # Your exam content goes here
    st.title("Secure Exam")
    
    # Example exam content
    with st.form("exam_form"):
        st.write("Question 1")
        answer1 = st.text_area("Explain the concept of recursion:")
        
        st.write("Question 2")
        options = ["O(1)", "O(n)", "O(n²)", "O(log n)"]
        answer2 = st.radio("What is the time complexity of binary search?", options)
        
        submitted = st.form_submit_button("Submit Exam")
        if submitted:
            # Send submission event to parent
            html("""
                <script>
                window.parent.postMessage({
                    type: 'exam_submitted',
                    data: {
                        timestamp: Date.now()
                    },
                    source: 'streamlit'
                }, '*');
                </script>
            """)
            st.success("Exam submitted successfully!")

    # Add state management for violations
    if 'violations' not in st.session_state:
        st.session_state.violations = []

    # Hidden element to store violation data
    st.markdown("""
        <div id="violations" style="display: none;"></div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    create_exam_app()