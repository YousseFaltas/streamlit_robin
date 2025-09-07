import streamlit as st
import time
import requests 

FASTAPI_URL =  ""

st.set_page_config(page_title="Robin - AI Chatbot", page_icon="🤖")

st.title("Welcome to Robin 🤖")
st.markdown("Your Data Science & AI Partner")

# Initialize session state variables
if "messages" not in st.session_state:
    st.session_state.messages = []
if "processing" not in st.session_state:
    st.session_state.processing = False

# backgroundColor="#76dfd1ff"

st.markdown("""
<style>

</style>
""", unsafe_allow_html=True)

# Function to simulate a response
def response(prompt):
    """
    Sends a prompt to the FastAPI backend and gets the response.
    """
    payload = {
        "message": prompt,
        "identifier": "x"  # Using a fixed identifier as requested
    }
    try:
        # Send a POST request to the FastAPI endpoint
        api_response = requests.post(FASTAPI_URL, json=payload)
        
        # Check for a successful response
        if api_response.status_code == 200:
            response_data = api_response.json()
            return response_data.get("answer", "Sorry, I couldn't get a valid response.")
        else:
            # Handle non-200 responses
            error_detail = api_response.json().get('detail', 'Unknown error')
            return f"Error from server: {error_detail}"

    except requests.exceptions.RequestException as e:
        # Handle connection errors
        st.error(f"Could not connect to the FastAPI server at {FASTAPI_URL}. Please ensure it is running.")
        return "Sorry, I'm having trouble connecting to my brain right now."
    
with st.chat_message("assistant"):
    message_placeholder = st.empty()
    assistant_response = "Hi , how can i help you today?"
    message_placeholder.markdown(assistant_response)

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle new user input
if prompt := st.chat_input("How can we help you?", disabled=st.session_state.processing, key="chat_input"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    st.session_state.processing = True
    st.rerun()

# Generate and display bot response if processing
if st.session_state.processing:
    last_prompt = st.session_state.messages[-1]["content"]
    
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        assistant_response = response(last_prompt)
        
        for chunk in assistant_response.split():
            full_response += chunk + " "
            time.sleep(0.05)
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
        
    st.session_state.messages.append({"role": "assistant", "content": full_response})
    
    st.session_state.processing = False
    st.rerun()